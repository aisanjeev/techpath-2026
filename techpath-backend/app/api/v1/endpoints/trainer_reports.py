"""Read-only trainer reports over a session's history: attendance, poll history, and a
confusion timeline mined from the realtime event outbox.

Mounted under the same ``/trainer`` prefix as ``app/api/v1/endpoints/trainer.py`` (see
``app/api/v1/router.py``) — kept in a separate module purely so this feature can land
without touching that file's owner. Access control mirrors it exactly: a trainer may
only report on sessions belonging to their own batches, an admin may report on any.
"""

import json
import logging
from datetime import datetime
from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.v1.dependencies import get_current_trainer_user
from app.core.constants import AssetType, UserRole
from app.core.exceptions import ForbiddenError, NotFoundError
from app.crud.quiz_attempts import session_quiz_attempt_crud
from app.crud.training import load_config, training_module_crud
from app.crud.training_roster import training_batch_crud, training_session_crud
from app.db.session import get_db
from app.models.classroom import ClassroomEvent, SessionParticipant, SessionPoll, SessionPollVote
from app.models.training_roster import SessionQuizAttempt
from app.models.user import User
from app.schemas.trainer_reports import (
    AttendanceReportResponse,
    AttendanceRow,
    ConfusionTimelinePoint,
    ConfusionTimelineResponse,
    PollHistoryEntry,
    PollHistoryResponse,
    QuizQuestionStat,
    QuizResultsResponse,
    QuizResultSummary,
    QuizStudentResult,
)
from app.services import quiz_grading


logger = logging.getLogger(__name__)

router = APIRouter()

# A trainer's chart doesn't need more resolution than this — downsample evenly rather
# than shipping thousands of points for a long-running session.
_MAX_TIMELINE_POINTS = 300


async def _assert_owns_batch(db: AsyncSession, user: User, batch) -> None:
    """A trainer may only see reports for their own batches; an admin may see any.

    Duplicated from ``app/api/v1/endpoints/trainer.py`` rather than imported — that
    module's leading-underscore helper isn't meant to be imported across files, and this
    keeps the two endpoint modules independently editable.
    """
    if user.role == UserRole.ADMIN.value:
        return
    if not batch.trainer_email or batch.trainer_email.lower() != user.email.lower():
        raise ForbiddenError("This batch is not assigned to you")


@router.get("/sessions/{session_id}/attendance", response_model=AttendanceReportResponse)
async def get_attendance_report(
    session_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_trainer_user),
) -> AttendanceReportResponse:
    """Every participant who ever joined, online or not — presence on
    ``SessionParticipant`` is the attendance record, there is no separate table."""
    session = await training_session_crud.get_with_relations(db, session_id)
    if not session:
        raise NotFoundError("Session")
    await _assert_owns_batch(db, current_user, session.batch)

    result = await db.execute(
        select(SessionParticipant)
        .where(SessionParticipant.session_id == session_id)
        .order_by(SessionParticipant.first_joined_at.asc())
    )
    participants = list(result.scalars().all())

    rows = [
        AttendanceRow(
            participant_id=p.id,
            display_name=p.display_name,
            is_guest=p.is_guest,
            student_id=p.student_id,
            first_joined_at=p.first_joined_at,
            last_seen_at=p.last_seen_at,
            left_at=p.left_at,
            is_online=p.is_online,
            duration_minutes=round(
                ((p.left_at or p.last_seen_at) - p.first_joined_at).total_seconds() / 60, 1
            ),
        )
        for p in participants
    ]

    return AttendanceReportResponse(
        session_id=session_id,
        session_title=session.title,
        total_participants=len(rows),
        rows=rows,
    )


@router.get("/sessions/{session_id}/polls/history", response_model=PollHistoryResponse)
async def get_poll_history(
    session_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_trainer_user),
) -> PollHistoryResponse:
    """Every poll ever run in the session, open or closed, most recent first."""
    session = await training_session_crud.get_with_relations(db, session_id)
    if not session:
        raise NotFoundError("Session")
    await _assert_owns_batch(db, current_user, session.batch)

    result = await db.execute(
        select(SessionPoll)
        .where(SessionPoll.session_id == session_id)
        .order_by(SessionPoll.id.desc())
    )
    polls = list(result.scalars().all())

    entries: List[PollHistoryEntry] = []
    for poll in polls:
        # Inlined rather than calling session_poll_crud.tally (crud/classroom.py is
        # another agent's file right now) — same three-line query it uses.
        tally_result = await db.execute(
            select(SessionPollVote.option_index, func.count(SessionPollVote.id))
            .where(SessionPollVote.poll_id == poll.id)
            .group_by(SessionPollVote.option_index)
        )
        results = dict(tally_result.all())
        entries.append(
            PollHistoryEntry(
                id=poll.id,
                question=poll.question,
                options=json.loads(poll.options_json),
                status=poll.status,
                results=results,
                total_votes=sum(results.values()),
                correct_option_index=poll.correct_option_index,
                created_at=poll.created_at,
                closed_at=poll.closed_at,
            )
        )

    return PollHistoryResponse(session_id=session_id, polls=entries)


@router.get("/sessions/{session_id}/confusion-timeline", response_model=ConfusionTimelineResponse)
async def get_confusion_timeline(
    session_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_trainer_user),
) -> ConfusionTimelineResponse:
    """The room's confusion level over time, mined from the ``roster_changed`` events
    already published to the outbox by ``publish_roster_snapshot`` — no new tracking
    needed, ``ClassroomEvent`` is append-only and already has everything."""
    session = await training_session_crud.get_with_relations(db, session_id)
    if not session:
        raise NotFoundError("Session")
    await _assert_owns_batch(db, current_user, session.batch)

    result = await db.execute(
        select(ClassroomEvent)
        .where(
            ClassroomEvent.session_id == session_id,
            ClassroomEvent.event_type == "roster_changed",
        )
        .order_by(ClassroomEvent.id)
    )
    events = list(result.scalars().all())

    points: List[ConfusionTimelinePoint] = []
    for event in events:
        payload = json.loads(event.payload_json)
        confusion = payload.get("confusion") or {}
        points.append(
            ConfusionTimelinePoint(
                timestamp=event.created_at,
                online=confusion.get("online", 0),
                confused=confusion.get("confused", 0),
                ratio=confusion.get("ratio", 0.0),
            )
        )

    if len(points) > _MAX_TIMELINE_POINTS:
        step = (len(points) // _MAX_TIMELINE_POINTS) + 1
        points = points[::step]

    return ConfusionTimelineResponse(session_id=session_id, points=points)


@router.get("/sessions/{session_id}/quiz-results", response_model=QuizResultsResponse)
async def get_quiz_results(
    session_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_trainer_user),
) -> QuizResultsResponse:
    """How the group did on each quiz in this session's material.

    Built from the batch roster outward rather than from the attempts inward: a
    trainer's most useful signal is usually who has not engaged at all, and an
    attempts-only query drops those students entirely.
    """
    session = await training_session_crud.get_with_relations(db, session_id)
    if not session:
        raise NotFoundError("Session")
    await _assert_owns_batch(db, current_user, session.batch)

    if not session.module_id:
        return QuizResultsResponse(session_id=session_id, quizzes=[])

    module = await training_module_crud.get_with_assets(db, session.module_id)
    if not module:
        return QuizResultsResponse(session_id=session_id, quizzes=[])

    quiz_assets = [
        link.asset for link in module.asset_links if link.asset.asset_type == AssetType.QUIZ.value
    ]
    if not quiz_assets:
        return QuizResultsResponse(session_id=session_id, quizzes=[])

    roster = await training_batch_crud.students(db, session.batch_id)
    attempts = await session_quiz_attempt_crud.list_for_session_assets(
        db, session_id, [a.id for a in quiz_assets]
    )

    by_asset: dict[int, List[SessionQuizAttempt]] = {a.id: [] for a in quiz_assets}
    for attempt in attempts:
        by_asset.setdefault(attempt.asset_id, []).append(attempt)

    summaries: List[QuizResultSummary] = []
    for asset in quiz_assets:
        config = load_config(asset.config_json)
        try:
            questions = quiz_grading.extract_questions(config)
        except quiz_grading.QuizConfigError:
            # A malformed quiz shouldn't take the whole report down with it.
            questions = []
        current_total = len(questions)

        asset_attempts = by_asset.get(asset.id, [])

        # Best attempt per student. "Best" is by score, ties broken by the later
        # attempt — with unlimited retries, best-of is the only summary that doesn't
        # punish a student for practising.
        best_by_student: dict[int, SessionQuizAttempt] = {}
        counts_by_student: dict[int, int] = {}
        last_at_by_student: dict[int, datetime] = {}
        for attempt in asset_attempts:
            counts_by_student[attempt.student_id] = counts_by_student.get(attempt.student_id, 0) + 1
            current_best = best_by_student.get(attempt.student_id)
            if current_best is None or attempt.score >= current_best.score:
                best_by_student[attempt.student_id] = attempt
            previous = last_at_by_student.get(attempt.student_id)
            if previous is None or attempt.attempted_at > previous:
                last_at_by_student[attempt.student_id] = attempt.attempted_at

        students: List[QuizStudentResult] = []
        for student in roster:
            best = best_by_student.get(student.id)
            students.append(
                QuizStudentResult(
                    student_id=student.id,
                    name=student.name,
                    email=student.email,
                    attempt_count=counts_by_student.get(student.id, 0),
                    best_score=best.score if best else None,
                    total_questions=best.total_questions if best else None,
                    passed=bool(best and best.passed),
                    last_attempted_at=last_at_by_student.get(student.id),
                    is_stale=bool(best and best.total_questions != current_total),
                )
            )

        # Per-question success, counted from each student's best attempt only so a
        # student retrying doesn't contribute several times to one question's rate.
        question_stats: List[QuizQuestionStat] = []
        for i, question in enumerate(questions):
            correct = 0
            attempted = 0
            for best in best_by_student.values():
                answers = json.loads(best.answers_json)
                if i >= len(answers):
                    # Attempt predates this question being added — it can't be scored
                    # against a question its author never saw.
                    continue
                attempted += 1
                if answers[i] == question.get("correct_index"):
                    correct += 1
            question_stats.append(
                QuizQuestionStat(
                    index=i,
                    question=question.get("question", ""),
                    correct_count=correct,
                    attempted_count=attempted,
                )
            )

        summaries.append(
            QuizResultSummary(
                asset_id=asset.id,
                title=asset.title,
                total_questions=current_total,
                pass_mark=quiz_grading.pass_mark_for(config),
                attempted_count=len(best_by_student),
                passed_count=sum(1 for b in best_by_student.values() if b.passed),
                roster_size=len(roster),
                question_stats=question_stats,
                students=students,
            )
        )

    return QuizResultsResponse(session_id=session_id, quizzes=summaries)
