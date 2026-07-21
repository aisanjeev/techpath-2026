"""Read-only admin views over the mirrored roster, plus sync control.

There are deliberately no POST/PUT/DELETE routes for batches or students. The external
system owns that data; read-only is enforced by the absence of routes rather than by a
flag someone can forget to check. The single exception is ``program_id``, which is ours,
and it gets its own narrow endpoint so the invariant stays obvious.
"""
import json
import logging
from typing import Optional

from fastapi import APIRouter, Depends, Query
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.v1.dependencies import get_current_admin_user
from app.core.config import settings
from app.core.exceptions import NotFoundError
from app.crud.training import training_program_crud
from app.crud.training_roster import (
    sync_state_crud,
    training_batch_crud,
    training_student_crud,
)
from app.db.session import get_db
from app.models.user import User
from app.schemas.training_roster import (
    AssignTrainerRequest,
    LinkProgramRequest,
    SyncRunResponse,
    SyncStateResponse,
    SyncStatusResponse,
    TrainingBatchResponse,
    TrainingStudentResponse,
)
from app.services.roster.factory import get_roster_provider
from app.services.roster_sync_service import RosterSyncService
from app.services.secrets_loader import runtime_secrets

logger = logging.getLogger(__name__)

router = APIRouter()


def _batch_out(batch, program_title: Optional[str] = None) -> TrainingBatchResponse:
    schedule = None
    if batch.schedule_json:
        try:
            schedule = json.loads(batch.schedule_json)
        except (ValueError, TypeError):
            schedule = None
    return TrainingBatchResponse(
        id=batch.id,
        external_id=batch.external_id,
        name=batch.name,
        code=batch.code,
        program_id=batch.program_id,
        program_title=program_title,
        start_date=batch.start_date,
        end_date=batch.end_date,
        timezone=batch.timezone,
        schedule=schedule,
        status=batch.status,
        mode=batch.mode,
        location=batch.location,
        trainer_email=batch.trainer_email,
        trainer_name=batch.trainer_name,
        is_self_paced=batch.is_self_paced,
        student_count=batch.student_count,
        course_ref=batch.course_ref,
        synced_at=batch.synced_at,
        external_updated_at=batch.external_updated_at,
    )


@router.get("/batches")
async def list_batches(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    status_filter: Optional[str] = Query(None, alias="status"),
    trainer_email: Optional[str] = Query(None),
    search: Optional[str] = Query(None),
    db: AsyncSession = Depends(get_db),
    current_admin: User = Depends(get_current_admin_user),
) -> JSONResponse:
    batches, total = await training_batch_crud.search(
        db,
        skip=skip,
        limit=limit,
        status=status_filter,
        trainer_email=trainer_email,
        search=search,
    )
    data = [_batch_out(b).model_dump(mode="json") for b in batches]
    return JSONResponse(content=data, headers={"X-Total-Count": str(total)})


@router.get("/batches/{batch_id}", response_model=TrainingBatchResponse)
async def get_batch(
    batch_id: int,
    db: AsyncSession = Depends(get_db),
    current_admin: User = Depends(get_current_admin_user),
) -> TrainingBatchResponse:
    batch = await training_batch_crud.get(db, batch_id)
    if not batch:
        raise NotFoundError("Batch")

    program_title = None
    if batch.program_id:
        program = await training_program_crud.get(db, batch.program_id)
        program_title = program.title if program else None
    return _batch_out(batch, program_title)


@router.patch("/batches/{batch_id}/program", response_model=TrainingBatchResponse)
async def link_batch_program(
    batch_id: int,
    payload: LinkProgramRequest,
    db: AsyncSession = Depends(get_db),
    current_admin: User = Depends(get_current_admin_user),
) -> TrainingBatchResponse:
    """Link a batch to the training programme it will be taught from.

    This is the only writable field on a mirrored batch — it is ours, not the external
    system's, and the sync preserves it.
    """
    batch = await training_batch_crud.get(db, batch_id)
    if not batch:
        raise NotFoundError("Batch")

    program_title = None
    if payload.program_id is not None:
        program = await training_program_crud.get(db, payload.program_id)
        if not program:
            raise NotFoundError("Training programme")
        program_title = program.title

    batch.program_id = payload.program_id
    db.add(batch)
    await db.flush()
    await db.refresh(batch)
    return _batch_out(batch, program_title)


@router.patch("/batches/{batch_id}/trainer", response_model=TrainingBatchResponse)
async def assign_batch_trainer(
    batch_id: int,
    payload: AssignTrainerRequest,
    db: AsyncSession = Depends(get_db),
    current_admin: User = Depends(get_current_admin_user),
) -> TrainingBatchResponse:
    """Assign a trainer to a batch by email.

    Like program_id, trainer_email is operator-set when the external system
    doesn't provide it.  The sync preserves admin-set values when the external
    API returns null.
    """
    batch = await training_batch_crud.get(db, batch_id)
    if not batch:
        raise NotFoundError("Batch")

    batch.trainer_email = payload.trainer_email.strip().lower() if payload.trainer_email else None
    db.add(batch)
    await db.flush()
    await db.refresh(batch)

    program_title = None
    if batch.program_id:
        program = await training_program_crud.get(db, batch.program_id)
        program_title = program.title if program else None
    return _batch_out(batch, program_title)


@router.patch("/batches/{batch_id}/self-paced", response_model=TrainingBatchResponse)
async def toggle_batch_self_paced(
    batch_id: int,
    is_self_paced: bool = Query(...),
    db: AsyncSession = Depends(get_db),
    current_admin: User = Depends(get_current_admin_user),
) -> TrainingBatchResponse:
    batch = await training_batch_crud.get(db, batch_id)
    if not batch:
        raise NotFoundError("Batch")

    batch.is_self_paced = is_self_paced
    db.add(batch)
    await db.flush()
    await db.refresh(batch)

    program_title = None
    if batch.program_id:
        program = await training_program_crud.get(db, batch.program_id)
        program_title = program.title if program else None
    return _batch_out(batch, program_title)


@router.get("/batches/{batch_id}/students")
async def list_batch_students(
    batch_id: int,
    db: AsyncSession = Depends(get_db),
    current_admin: User = Depends(get_current_admin_user),
) -> JSONResponse:
    if not await training_batch_crud.get(db, batch_id):
        raise NotFoundError("Batch")

    students = await training_batch_crud.students(db, batch_id)
    data = [TrainingStudentResponse.model_validate(s).model_dump(mode="json") for s in students]
    return JSONResponse(content=data, headers={"X-Total-Count": str(len(data))})


@router.get("/students")
async def list_students(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    status_filter: Optional[str] = Query(None, alias="status"),
    batch_id: Optional[int] = Query(None),
    search: Optional[str] = Query(None),
    db: AsyncSession = Depends(get_db),
    current_admin: User = Depends(get_current_admin_user),
) -> JSONResponse:
    students, total = await training_student_crud.search(
        db, skip=skip, limit=limit, status=status_filter, batch_id=batch_id, search=search
    )
    data = [TrainingStudentResponse.model_validate(s).model_dump(mode="json") for s in students]
    return JSONResponse(content=data, headers={"X-Total-Count": str(total)})


@router.get("/students/{student_id}", response_model=TrainingStudentResponse)
async def get_student(
    student_id: int,
    db: AsyncSession = Depends(get_db),
    current_admin: User = Depends(get_current_admin_user),
) -> TrainingStudentResponse:
    student = await training_student_crud.get(db, student_id)
    if not student:
        raise NotFoundError("Student")
    return TrainingStudentResponse.model_validate(student)


@router.get("/sync/status", response_model=SyncStatusResponse)
async def sync_status(
    db: AsyncSession = Depends(get_db),
    current_admin: User = Depends(get_current_admin_user),
) -> SyncStatusResponse:
    """Provider, reachability and per-resource sync state.

    Makes integration day a config flip rather than a debugging session: point
    ROSTER_PROVIDER at http and this tells you immediately whether it worked.
    """
    provider_name = (runtime_secrets.get("ROSTER_PROVIDER") or settings.ROSTER_PROVIDER).lower()
    try:
        healthy = await get_roster_provider().health()
    except Exception as exc:  # noqa: BLE001 — status must report failure, not become one
        logger.warning("Roster provider health check errored: %s", exc)
        healthy = False

    states = await sync_state_crud.all_states(db)
    return SyncStatusResponse(
        provider=provider_name,
        healthy=healthy,
        resources=[SyncStateResponse.model_validate(s) for s in states],
    )


@router.post("/sync/{resource}", response_model=SyncRunResponse)
async def run_sync(
    resource: str,
    db: AsyncSession = Depends(get_db),
    current_admin: User = Depends(get_current_admin_user),
) -> SyncRunResponse:
    """Trigger a sync now. ``resource`` is one of: batches, students, all."""
    service = RosterSyncService(page_size=settings.ROSTER_SYNC_PAGE_SIZE)

    if resource == "batches":
        results = {"batches": (await service.sync_batches(db)).as_dict()}
    elif resource == "students":
        results = {"students": (await service.sync_students(db)).as_dict()}
    elif resource == "all":
        results = await service.sync_all(db)
    else:
        raise NotFoundError(f"Sync resource '{resource}'")

    failed = [r for r in results.values() if r.get("error")]
    return SyncRunResponse(success=not failed, results=results)
