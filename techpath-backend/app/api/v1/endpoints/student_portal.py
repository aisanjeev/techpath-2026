"""Public student-portal endpoints — the post-session, Firebase-authenticated side.

Distinct from ``classroom.py``'s join-code flow (see that module's docstring): this is
a returning student coming back after class to view or download what a trainer has
published, proven by a real Google sign-in rather than a 6-digit code. Every route here
depends on ``get_current_student``, which is the entire access-control boundary — a
student only ever sees a session if they both attended it (a matched
``SessionParticipant`` row) and a trainer has since published it.
"""
import logging
from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.v1.dependencies import get_current_student
from app.core.exceptions import NotFoundError
from app.crud.classroom import session_recording_crud
from app.crud.training import asset_to_response, training_module_crud
from app.crud.training_roster import training_session_crud
from app.db.session import get_db
from app.models.training_roster import TrainingStudent
from app.schemas.classroom import RecordingView
from app.schemas.student_portal import (
    StudentLoginResponse,
    StudentSessionListResponse,
    StudentSessionMaterialsResponse,
    StudentSessionSummary,
)
from app.schemas.training import LectureAssetResponse


logger = logging.getLogger(__name__)

router = APIRouter()


@router.post("/auth/login", response_model=StudentLoginResponse)
async def student_login(
    student: TrainingStudent = Depends(get_current_student),
) -> StudentLoginResponse:
    """Every portal route re-verifies the same way ``get_current_student`` does — this
    endpoint exists so the frontend has something to call right after the Google
    popup closes, to know sign-in resolved to a real roster student (as opposed to a
    401 it needs to show a "not on any roster" screen for) before routing onward."""
    return StudentLoginResponse(display_name=student.name, email=student.email)


@router.get("/sessions", response_model=StudentSessionListResponse)
async def list_my_sessions(
    student: TrainingStudent = Depends(get_current_student),
    db: AsyncSession = Depends(get_db),
) -> StudentSessionListResponse:
    sessions = await training_session_crud.list_published_for_student(db, student.id)
    summaries = []
    seen_modules = set()
    for s in sessions:
        # list_published_for_student's own query already filters to
        # materials_published_at IS NOT NULL — asserting rather than re-checking makes
        # that invariant explicit here instead of silently trusting the caller.
        assert s.materials_published_at is not None

        if s.module_id is not None:
            if s.module_id in seen_modules:
                continue
            seen_modules.add(s.module_id)

        summaries.append(
            StudentSessionSummary(
                session_id=s.id,
                title=s.title,
                batch_name=s.batch.name,
                module_title=s.module.title if s.module else None,
                session_date=s.started_at or s.scheduled_start,
                published_at=s.materials_published_at,
            )
        )
    return StudentSessionListResponse(sessions=summaries)


@router.get("/sessions/{session_id}/materials", response_model=StudentSessionMaterialsResponse)
async def get_session_materials(
    session_id: int,
    student: TrainingStudent = Depends(get_current_student),
    db: AsyncSession = Depends(get_db),
) -> StudentSessionMaterialsResponse:
    session = await training_session_crud.get_enrolled_published(db, session_id, student.id)
    if session is None:
        raise NotFoundError("Session")
    # get_enrolled_published's own query already filters to
    # materials_published_at IS NOT NULL for a hit.
    assert session.materials_published_at is not None

    assets: List[LectureAssetResponse] = []
    if session.module_id:
        module = await training_module_crud.get_with_assets(db, session.module_id)
        if module:
            assets = [await asset_to_response(db, link.asset) for link in module.asset_links]

    recording_row = await session_recording_crud.get_by_session(db, session.id)
    recording = RecordingView.model_validate(recording_row) if recording_row else None

    return StudentSessionMaterialsResponse(
        session_id=session.id,
        title=session.title,
        batch_name=session.batch.name,
        module_title=session.module.title if session.module else None,
        published_at=session.materials_published_at,
        assets=assets,
        recording=recording,
    )
