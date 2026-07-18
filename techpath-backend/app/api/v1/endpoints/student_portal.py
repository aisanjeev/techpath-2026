"""Public student-portal endpoints — the post-session, Firebase-authenticated side.

Distinct from ``classroom.py``'s join-code flow (see that module's docstring): this is
a returning student coming back after class to view or download what a trainer has
published, proven by a real Google sign-in rather than a 6-digit code. Every route here
depends on ``get_current_student``, which is the entire access-control boundary — a
student only ever sees a session if they both attended it (a matched
``SessionParticipant`` row) and a trainer has since published it.
"""

import json
import logging
from datetime import datetime, timezone
from typing import List, Set

from fastapi import APIRouter, Depends, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.v1.dependencies import get_current_student
from app.core.constants import AssetType
from app.core.exceptions import NotFoundError, ValidationError
from app.crud.classroom import session_recording_crud
from app.crud.quiz_attempts import session_quiz_attempt_crud
from app.crud.training import asset_to_response, load_config, training_module_crud
from app.crud.training_roster import training_session_crud
from app.db.session import get_db
from app.models.training import LectureAsset
from app.models.training_roster import TrainingSession, TrainingStudent
from app.schemas.classroom import RecordingView
from app.schemas.student_portal import (
    QuizAttemptResult,
    QuizAttemptSubmission,
    QuizQuestionFeedback,
    StudentLoginResponse,
    StudentProgressItem,
    StudentProgressResponse,
    StudentSessionListResponse,
    StudentSessionMaterialsResponse,
    StudentSessionSummary,
)
from app.schemas.training import LectureAssetResponse
from app.services import quiz_grading


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
            # audience="student" strips quiz answer keys — see asset_to_response.
            assets = [
                await asset_to_response(db, link.asset, audience="student")
                for link in module.asset_links
            ]

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


# ---------------------------------------------------------------------------
# Graded quizzes
# ---------------------------------------------------------------------------


async def _session_assets(db: AsyncSession, session: TrainingSession) -> List[LectureAsset]:
    """The session's material in the order the portal pages through it.

    ``asset_links`` is ordered by ``display_order`` on the relationship, so positional
    index here is the same index the pager shows as "Page N of M". Gating depends on
    that alignment.
    """
    if not session.module_id:
        return []
    module = await training_module_crud.get_with_assets(db, session.module_id)
    if not module:
        return []
    return [link.asset for link in module.asset_links]


def _first_locked_index(assets: List[LectureAsset], passed_asset_ids: Set[int]) -> int:
    """Index of the first quiz the student hasn't passed, or len(assets) if none.

    An empty quiz (no questions) can never be "not passed" in a way that matters —
    grading treats 0/0 as a pass — but a student who has never opened one has no
    attempt row either, so it's skipped here explicitly rather than blocking on a
    quiz there is nothing to answer.
    """
    for i, asset in enumerate(assets):
        if asset.asset_type != AssetType.QUIZ.value:
            continue
        if asset.id in passed_asset_ids:
            continue
        if not quiz_grading.extract_questions(load_config(asset.config_json)):
            continue
        return i
    return len(assets)


@router.get("/sessions/{session_id}/progress", response_model=StudentProgressResponse)
async def get_session_progress(
    session_id: int,
    student: TrainingStudent = Depends(get_current_student),
    db: AsyncSession = Depends(get_db),
) -> StudentProgressResponse:
    """What this student has completed and what is still locked, for one session.

    Computed server-side because the client can't be trusted with it and doesn't know
    the pass mark. Returned as a per-item list rather than a bare index so the portal
    can show the whole map — a real LMS shows you where you are, not just a wall.
    """
    session = await training_session_crud.get_enrolled_published(db, session_id, student.id)
    if session is None:
        raise NotFoundError("Session")

    assets = await _session_assets(db, session)
    # One query for the whole session — the portal renders a page per asset and must
    # not fan out into a query per asset to decide what's locked.
    passed_ids = await session_quiz_attempt_crud.passed_asset_ids(db, student.id, session.id)
    summaries = await session_quiz_attempt_crud.summary_for_student(db, student.id, session.id)

    first_locked = _first_locked_index(assets, passed_ids)

    items: List[StudentProgressItem] = []
    for i, asset in enumerate(assets):
        is_quiz = asset.asset_type == AssetType.QUIZ.value
        summary = summaries.get(asset.id) if is_quiz else None
        items.append(
            StudentProgressItem(
                asset_id=asset.id,
                index=i,
                is_quiz=is_quiz,
                passed=(asset.id in passed_ids) if is_quiz else None,
                locked=i > first_locked,
                best_score=summary["best_score"] if summary else None,
                total_questions=summary["total_questions"] if summary else None,
                attempt_count=summary["attempt_count"] if summary else None,
            )
        )

    return StudentProgressResponse(
        session_id=session.id, first_locked_index=first_locked, items=items
    )


@router.post(
    "/sessions/{session_id}/assets/{asset_id}/quiz-attempts",
    response_model=QuizAttemptResult,
    status_code=status.HTTP_201_CREATED,
)
async def submit_quiz_attempt(
    session_id: int,
    asset_id: int,
    payload: QuizAttemptSubmission,
    student: TrainingStudent = Depends(get_current_student),
    db: AsyncSession = Depends(get_db),
) -> QuizAttemptResult:
    """Grade and record one attempt.

    Grading is server-side against the stored answer key; the request carries selected
    option indices and nothing else. The response is the only place a student ever
    receives ``correct_index`` and ``explanation``, and only for the attempt they just
    submitted — everywhere else they're stripped (see ``asset_to_response``).
    """
    session = await training_session_crud.get_enrolled_published(db, session_id, student.id)
    if session is None:
        raise NotFoundError("Session")

    assets = await _session_assets(db, session)
    asset = next((a for a in assets if a.id == asset_id), None)
    # Resolved from the session's own material rather than by id alone: a student must
    # not be able to grade themselves against a quiz from a session they never attended.
    if asset is None:
        raise NotFoundError("Lecture asset")
    if asset.asset_type != AssetType.QUIZ.value:
        raise ValidationError("That asset isn't a quiz")

    config = load_config(asset.config_json)
    try:
        questions = quiz_grading.extract_questions(config)
    except quiz_grading.QuizConfigError as exc:
        raise ValidationError(str(exc))

    try:
        answers = quiz_grading.validate_answers(questions, payload.answers)
    except ValueError as exc:
        raise ValidationError(str(exc))

    pass_mark = quiz_grading.pass_mark_for(config)
    score, total, passed = quiz_grading.grade(questions, answers, pass_mark)

    attempt_number = await session_quiz_attempt_crud.next_attempt_number(db, student.id, asset.id)
    try:
        attempt = await session_quiz_attempt_crud.create(
            db,
            obj_in={
                "student_id": student.id,
                "session_id": session.id,
                "asset_id": asset.id,
                "attempt_number": attempt_number,
                "answers_json": json.dumps(answers),
                "score": score,
                "total_questions": total,
                "passed": passed,
                "attempted_at": datetime.now(timezone.utc),
            },
        )
    except IntegrityError:
        # Lost the race on the unique (student, asset, attempt_number) constraint —
        # a double-clicked submit or a retried request. The other insert recorded the
        # attempt, so return it rather than surfacing a spurious error to the student.
        await db.rollback()
        existing = await session_quiz_attempt_crud.list_for_student_asset(db, student.id, asset.id)
        if not existing:
            raise
        attempt = existing[-1]
        score, total, passed = attempt.score, attempt.total_questions, attempt.passed
        answers = json.loads(attempt.answers_json)

    # Recomputed after the write so a passing attempt reports the unlock immediately,
    # sparing the portal a follow-up progress fetch just to reveal the next item.
    passed_ids = await session_quiz_attempt_crud.passed_asset_ids(db, student.id, session.id)
    asset_index = next(i for i, a in enumerate(assets) if a.id == asset.id)
    unlocked_next = _first_locked_index(assets, passed_ids) > asset_index

    return QuizAttemptResult(
        attempt_id=attempt.id,
        attempt_number=attempt.attempt_number,
        score=score,
        total_questions=total,
        percentage=round((score / total * 100) if total else 100.0, 1),
        passed=passed,
        pass_mark=pass_mark,
        attempted_at=attempt.attempted_at,
        unlocked_next=unlocked_next,
        questions=[
            QuizQuestionFeedback(**fb) for fb in quiz_grading.question_feedback(questions, answers)
        ],
    )
