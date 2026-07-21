"""Public student-portal endpoints — Firebase-authenticated.

Two access modes:
1. **Session materials** (post-live-session): a student sees published sessions from
   batches they belong to. The trainer controls the publish gate.
2. **Self-paced courses**: a batch marked ``is_self_paced`` gives enrolled students
   direct access to all published modules in the linked programme, with no session
   required.

Both share ``get_current_student`` as the identity boundary.
"""

import json
import logging
from datetime import datetime, timezone
from typing import List, Set

from fastapi import APIRouter, Body, Depends, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.v1.dependencies import get_current_student
from app.core.constants import AssetStatus, AssetType
from app.core.exceptions import NotFoundError, ValidationError
from app.crud.classroom import session_recording_crud
from app.crud.quiz_attempts import session_quiz_attempt_crud
from app.crud.training import (
    asset_to_response,
    load_config,
    training_module_crud,
    training_program_crud,
)
from app.crud.training_roster import (
    student_module_progress_crud,
    training_session_crud,
)
from app.db.session import get_db
from app.models.training import LectureAsset, TrainingModule
from app.models.training_roster import TrainingSession, TrainingStudent
from app.schemas.classroom import RecordingView
from app.schemas.student_portal import (
    QuizAttemptResult,
    QuizAttemptSubmission,
    QuizQuestionFeedback,
    SelfPacedCourseDetailResponse,
    SelfPacedCourseListResponse,
    SelfPacedCourseSummary,
    SelfPacedModuleMaterialsResponse,
    SelfPacedModuleSummary,
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


# ---------------------------------------------------------------------------
# Self-paced courses
# ---------------------------------------------------------------------------


async def _module_assets(db: AsyncSession, module_id: int) -> List[LectureAsset]:
    module = await training_module_crud.get_with_assets(db, module_id)
    if not module:
        return []
    return [link.asset for link in module.asset_links]


def _module_asset_counts(module: TrainingModule) -> tuple[int, int]:
    """(total_assets, quiz_count) from a module's eager-loaded asset_links."""
    total = len(module.asset_links)
    quizzes = sum(
        1
        for link in module.asset_links
        if link.asset.asset_type == AssetType.QUIZ.value
    )
    return total, quizzes


@router.get("/courses", response_model=SelfPacedCourseListResponse)
async def list_self_paced_courses(
    student: TrainingStudent = Depends(get_current_student),
    db: AsyncSession = Depends(get_db),
) -> SelfPacedCourseListResponse:
    rows = await student_module_progress_crud.self_paced_programs_for_student(
        db, student.id
    )
    seen_programs: set[int] = set()
    courses: List[SelfPacedCourseSummary] = []

    for program, batch in rows:
        if program.id in seen_programs:
            continue
        seen_programs.add(program.id)

        program_full = await training_program_crud.get_with_modules_and_assets(db, program.id)
        if not program_full:
            continue

        published_modules = [
            m
            for m in program_full.modules
            if m.status == AssetStatus.PUBLISHED.value
        ]

        all_module_ids = [m.id for m in published_modules]
        progress_rows = await student_module_progress_crud.list_for_student_modules(
            db, student.id, all_module_ids
        )
        completed = sum(1 for p in progress_rows if p.completed_at is not None)
        total_assets = sum(len(m.asset_links) for m in published_modules)

        courses.append(
            SelfPacedCourseSummary(
                program_id=program.id,
                title=program.title,
                slug=program.slug,
                summary=program.summary,
                cover_image=program.cover_image,
                delivery_mode=program.delivery_mode,
                level=program.level,
                duration=program.duration,
                batch_name=batch.name,
                module_count=len(published_modules),
                completed_modules=completed,
                total_assets=total_assets,
            )
        )

    return SelfPacedCourseListResponse(courses=courses)


@router.get("/courses/{program_id}", response_model=SelfPacedCourseDetailResponse)
async def get_self_paced_course(
    program_id: int,
    student: TrainingStudent = Depends(get_current_student),
    db: AsyncSession = Depends(get_db),
) -> SelfPacedCourseDetailResponse:
    batch = await student_module_progress_crud.verify_self_paced_enrollment(
        db, student.id, program_id
    )
    if batch is None:
        raise NotFoundError("Course")

    program = await training_program_crud.get_with_modules_and_assets(db, program_id)
    if program is None:
        raise NotFoundError("Course")

    published_modules = [
        m for m in program.modules if m.status == AssetStatus.PUBLISHED.value
    ]
    module_ids = [m.id for m in published_modules]
    progress_rows = await student_module_progress_crud.list_for_student_modules(
        db, student.id, module_ids
    )
    progress_map = {p.module_id: p for p in progress_rows}

    module_summaries: List[SelfPacedModuleSummary] = []
    for m in published_modules:
        asset_count, quiz_count = _module_asset_counts(m)
        prog = progress_map.get(m.id)
        module_summaries.append(
            SelfPacedModuleSummary(
                module_id=m.id,
                title=m.title,
                description=m.description,
                display_order=m.display_order,
                estimated_minutes=m.estimated_minutes,
                asset_count=asset_count,
                quiz_count=quiz_count,
                started=prog is not None,
                completed=prog is not None and prog.completed_at is not None,
                last_asset_index=prog.last_asset_index if prog else 0,
            )
        )

    return SelfPacedCourseDetailResponse(
        program_id=program.id,
        title=program.title,
        slug=program.slug,
        summary=program.summary,
        description=program.description,
        cover_image=program.cover_image,
        delivery_mode=program.delivery_mode,
        level=program.level,
        duration=program.duration,
        batch_name=batch.name,
        modules=module_summaries,
    )


@router.get(
    "/courses/{program_id}/modules/{module_id}/materials",
    response_model=SelfPacedModuleMaterialsResponse,
)
async def get_self_paced_module_materials(
    program_id: int,
    module_id: int,
    student: TrainingStudent = Depends(get_current_student),
    db: AsyncSession = Depends(get_db),
) -> SelfPacedModuleMaterialsResponse:
    batch = await student_module_progress_crud.verify_self_paced_enrollment(
        db, student.id, program_id
    )
    if batch is None:
        raise NotFoundError("Course")

    module = await training_module_crud.get_with_assets(db, module_id)
    if module is None or module.program_id != program_id:
        raise NotFoundError("Module")
    if module.status != AssetStatus.PUBLISHED.value:
        raise NotFoundError("Module")

    program = await training_program_crud.get(db, program_id)

    assets = [
        await asset_to_response(db, link.asset, audience="student")
        for link in module.asset_links
    ]

    await student_module_progress_crud.upsert(
        db, student.id, module_id, last_asset_index=0
    )

    return SelfPacedModuleMaterialsResponse(
        program_id=program_id,
        module_id=module_id,
        module_title=module.title,
        program_title=program.title if program else "",
        batch_name=batch.name,
        assets=assets,
    )


@router.get(
    "/courses/{program_id}/modules/{module_id}/progress",
    response_model=StudentProgressResponse,
)
async def get_self_paced_module_progress(
    program_id: int,
    module_id: int,
    student: TrainingStudent = Depends(get_current_student),
    db: AsyncSession = Depends(get_db),
) -> StudentProgressResponse:
    batch = await student_module_progress_crud.verify_self_paced_enrollment(
        db, student.id, program_id
    )
    if batch is None:
        raise NotFoundError("Course")

    module = await training_module_crud.get_with_assets(db, module_id)
    if module is None or module.program_id != program_id:
        raise NotFoundError("Module")

    assets = [link.asset for link in module.asset_links]
    passed_ids = await session_quiz_attempt_crud.passed_asset_ids_for_module(
        db, student.id, module_id
    )
    summaries = await session_quiz_attempt_crud.summary_for_student_module(
        db, student.id, module_id
    )
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
        module_id=module_id, first_locked_index=first_locked, items=items
    )


@router.post(
    "/courses/{program_id}/modules/{module_id}/assets/{asset_id}/quiz-attempts",
    response_model=QuizAttemptResult,
    status_code=status.HTTP_201_CREATED,
)
async def submit_self_paced_quiz_attempt(
    program_id: int,
    module_id: int,
    asset_id: int,
    payload: QuizAttemptSubmission,
    student: TrainingStudent = Depends(get_current_student),
    db: AsyncSession = Depends(get_db),
) -> QuizAttemptResult:
    batch = await student_module_progress_crud.verify_self_paced_enrollment(
        db, student.id, program_id
    )
    if batch is None:
        raise NotFoundError("Course")

    assets = await _module_assets(db, module_id)
    asset = next((a for a in assets if a.id == asset_id), None)
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

    attempt_number = await session_quiz_attempt_crud.next_attempt_number(
        db, student.id, asset.id
    )
    try:
        attempt = await session_quiz_attempt_crud.create(
            db,
            obj_in={
                "student_id": student.id,
                "session_id": None,
                "module_id": module_id,
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
        await db.rollback()
        existing = await session_quiz_attempt_crud.list_for_student_asset(
            db, student.id, asset.id
        )
        if not existing:
            raise
        attempt = existing[-1]
        score, total, passed = attempt.score, attempt.total_questions, attempt.passed
        answers = json.loads(attempt.answers_json)

    passed_ids = await session_quiz_attempt_crud.passed_asset_ids_for_module(
        db, student.id, module_id
    )
    asset_index = next(i for i, a in enumerate(assets) if a.id == asset.id)
    unlocked_next = _first_locked_index(assets, passed_ids) > asset_index

    if passed:
        all_passed = _first_locked_index(assets, passed_ids) >= len(assets)
        if all_passed:
            await student_module_progress_crud.upsert(
                db,
                student.id,
                module_id,
                last_asset_index=asset_index,
                completed=True,
            )

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
            QuizQuestionFeedback(**fb)
            for fb in quiz_grading.question_feedback(questions, answers)
        ],
    )


@router.post("/courses/{program_id}/modules/{module_id}/bookmark")
async def update_module_bookmark(
    program_id: int,
    module_id: int,
    last_asset_index: int = Body(..., embed=True),
    student: TrainingStudent = Depends(get_current_student),
    db: AsyncSession = Depends(get_db),
):
    batch = await student_module_progress_crud.verify_self_paced_enrollment(
        db, student.id, program_id
    )
    if batch is None:
        raise NotFoundError("Course")

    module = await training_module_crud.get_with_assets(db, module_id)
    if module is None:
        raise NotFoundError("Course")
    
    assets = [a.asset for a in module.assets if a.asset.is_active]
    progress = await student_module_progress_crud.get(db, student.id, module_id)
    passed_ids = set(progress.passed_asset_ids) if progress else set()
    
    completed = False
    if last_asset_index >= len(assets) - 1:
        if _first_locked_index(assets, passed_ids) >= len(assets):
            completed = True

    await student_module_progress_crud.upsert(
        db, student.id, module_id, last_asset_index=last_asset_index, completed=completed
    )
    return {"success": True}
