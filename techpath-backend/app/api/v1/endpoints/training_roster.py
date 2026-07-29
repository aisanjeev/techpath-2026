"""Read-only admin views over the mirrored roster, plus sync control.

There are deliberately no POST/PUT/DELETE routes for batches or students. The external
system owns that data; read-only is enforced by the absence of routes rather than by a
flag someone can forget to check. The single exception is ``program_id``, which is ours,
and it gets its own narrow endpoint so the invariant stays obvious.
"""
import json
import logging
from datetime import datetime, timezone
from typing import Optional

from fastapi import APIRouter, Depends, Query
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.v1.dependencies import get_current_admin_user
from app.core.config import settings
from app.core.constants import SessionStatus
from app.core.exceptions import NotFoundError, ValidationError
from app.crud.training import training_module_crud, training_program_crud
from app.crud.training_roster import (
    session_asset_release_crud,
    sync_state_crud,
    training_batch_crud,
    training_session_crud,
    training_student_crud,
)
from app.db.session import get_db
from app.models.training_roster import SessionAssetRelease
from app.models.user import User
from app.schemas.training_roster import (
    AssetReleaseItem,
    AssignTrainerRequest,
    LinkProgramRequest,
    SessionMaterialsStatusResponse,
    SyncRunResponse,
    SyncStateResponse,
    SyncStatusResponse,
    TrainingBatchResponse,
    TrainingSessionResponse,
    TrainingStudentResponse,
    BatchProgramSummary,
)
from app.services.roster.factory import get_roster_provider
from app.services.roster_sync_service import RosterSyncService
from app.services.secrets_loader import runtime_secrets

logger = logging.getLogger(__name__)

router = APIRouter()


def _batch_out(batch) -> TrainingBatchResponse:
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
        programs=[BatchProgramSummary(id=p.id, title=p.title) for p in batch.programs],
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

    return _batch_out(batch)


@router.patch("/batches/{batch_id}/program", response_model=TrainingBatchResponse)
async def link_batch_programs(
    batch_id: int,
    payload: LinkProgramRequest,
    db: AsyncSession = Depends(get_db),
    current_admin: User = Depends(get_current_admin_user),
) -> TrainingBatchResponse:
    """Link a batch to the training programmes it will be taught from.

    This is the only writable field on a mirrored batch — it is ours, not the external
    system's, and the sync preserves it.
    """
    batch = await training_batch_crud.get(db, batch_id)
    if not batch:
        raise NotFoundError("Batch")

    programs = []
    if payload.program_ids:
        for p_id in payload.program_ids:
            program = await training_program_crud.get(db, p_id)
            if not program:
                raise NotFoundError(f"Training programme {p_id}")
            programs.append(program)

    batch.programs = programs
    db.add(batch)
    await db.flush()
    await db.refresh(batch)
    return _batch_out(batch)


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

    return _batch_out(batch)


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

    return _batch_out(batch)


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


# ---------------------------------------------------------------------------
# Admin: per-asset session material management
# ---------------------------------------------------------------------------

def _session_out(session) -> TrainingSessionResponse:
    return TrainingSessionResponse(
        id=session.id,
        batch_id=session.batch_id,
        batch_name=session.batch.name if session.batch else None,
        module_id=session.module_id,
        module_title=session.module.title if session.module else None,
        title=session.title,
        scheduled_start=session.scheduled_start,
        scheduled_end=session.scheduled_end,
        status=session.status,
        join_code=session.join_code,
        started_at=session.started_at,
        ended_at=session.ended_at,
        keep_recording=session.keep_recording,
        questions_are_public=session.questions_are_public,
        materials_published_at=session.materials_published_at,
    )


async def _admin_materials_status(
    db: AsyncSession, session_id: int
) -> SessionMaterialsStatusResponse:
    from sqlalchemy import select as _select

    session = await training_session_crud.get_with_relations(db, session_id)
    released_ids = await session_asset_release_crud.get_released_ids(db, session_id)
    items: list[AssetReleaseItem] = []
    if session and session.module_id:
        module = await training_module_crud.get_with_assets(db, session.module_id)
        if module:
            for link in module.asset_links:
                release = None
                if link.asset_id in released_ids:
                    result = await db.execute(
                        _select(SessionAssetRelease).where(
                            SessionAssetRelease.session_id == session_id,
                            SessionAssetRelease.asset_id == link.asset_id,
                        )
                    )
                    release = result.scalar_one_or_none()
                items.append(
                    AssetReleaseItem(
                        asset_id=link.asset_id,
                        asset_title=link.asset.title,
                        asset_type=link.asset.asset_type,
                        is_released=link.asset_id in released_ids,
                        released_at=release.released_at if release else None,
                        released_by_user_id=release.released_by_user_id if release else None,
                        display_order=link.display_order,
                    )
                )
    return SessionMaterialsStatusResponse(session_id=session_id, assets=items)


async def _admin_sync_published_at(db: AsyncSession, session) -> None:
    count = await session_asset_release_crud.count(db, session.id)
    if count > 0 and session.materials_published_at is None:
        session.materials_published_at = datetime.now(timezone.utc)
        db.add(session)
        await db.flush()
    elif count == 0 and session.materials_published_at is not None:
        session.materials_published_at = None
        session.materials_published_by_user_id = None
        db.add(session)
        await db.flush()


@router.get(
    "/sessions/{session_id}/materials/status",
    response_model=SessionMaterialsStatusResponse,
)
async def admin_get_materials_status(
    session_id: int,
    db: AsyncSession = Depends(get_db),
    current_admin: User = Depends(get_current_admin_user),
) -> SessionMaterialsStatusResponse:
    """Per-asset release status for a session."""
    session = await training_session_crud.get_with_relations(db, session_id)
    if not session:
        raise NotFoundError("Session")
    return await _admin_materials_status(db, session_id)


@router.post(
    "/sessions/{session_id}/materials/assets/{asset_id}/release",
    response_model=SessionMaterialsStatusResponse,
)
async def admin_release_asset(
    session_id: int,
    asset_id: int,
    db: AsyncSession = Depends(get_db),
    current_admin: User = Depends(get_current_admin_user),
) -> SessionMaterialsStatusResponse:
    """Release a single asset so enrolled students can access it in the portal."""
    session = await training_session_crud.get_with_relations(db, session_id)
    if not session:
        raise NotFoundError("Session")
    if session.status != SessionStatus.ENDED.value:
        raise ValidationError("End the session before releasing materials")

    await session_asset_release_crud.release(db, session_id, asset_id, current_admin.id)
    await _admin_sync_published_at(db, session)
    return await _admin_materials_status(db, session_id)


@router.delete(
    "/sessions/{session_id}/materials/assets/{asset_id}/release",
    response_model=SessionMaterialsStatusResponse,
)
async def admin_unrelease_asset(
    session_id: int,
    asset_id: int,
    db: AsyncSession = Depends(get_db),
    current_admin: User = Depends(get_current_admin_user),
) -> SessionMaterialsStatusResponse:
    """Revoke a single asset's release."""
    session = await training_session_crud.get_with_relations(db, session_id)
    if not session:
        raise NotFoundError("Session")

    await session_asset_release_crud.unrelease(db, session_id, asset_id)
    await _admin_sync_published_at(db, session)
    return await _admin_materials_status(db, session_id)


@router.post(
    "/sessions/{session_id}/materials/publish",
    response_model=TrainingSessionResponse,
)
async def admin_publish_materials(
    session_id: int,
    db: AsyncSession = Depends(get_db),
    current_admin: User = Depends(get_current_admin_user),
) -> TrainingSessionResponse:
    """Release all assets for a session at once (admin shortcut)."""
    session = await training_session_crud.get_with_relations(db, session_id)
    if not session:
        raise NotFoundError("Session")
    if session.status != SessionStatus.ENDED.value:
        raise ValidationError("End the session before publishing its materials")

    if session.module_id:
        module = await training_module_crud.get_with_assets(db, session.module_id)
        if module:
            for link in module.asset_links:
                await session_asset_release_crud.release(
                    db, session_id, link.asset_id, current_admin.id
                )

    session.materials_published_at = datetime.now(timezone.utc)
    session.materials_published_by_user_id = current_admin.id
    db.add(session)
    await db.flush()

    session = await training_session_crud.get_with_relations(db, session_id)
    return _session_out(session)


@router.post(
    "/sessions/{session_id}/materials/unpublish",
    response_model=TrainingSessionResponse,
)
async def admin_unpublish_materials(
    session_id: int,
    db: AsyncSession = Depends(get_db),
    current_admin: User = Depends(get_current_admin_user),
) -> TrainingSessionResponse:
    """Revoke all asset releases for a session."""
    session = await training_session_crud.get_with_relations(db, session_id)
    if not session:
        raise NotFoundError("Session")

    await session_asset_release_crud.unrelease_all(db, session_id)
    session.materials_published_at = None
    session.materials_published_by_user_id = None
    db.add(session)
    await db.flush()

    session = await training_session_crud.get_with_relations(db, session_id)
    return _session_out(session)
