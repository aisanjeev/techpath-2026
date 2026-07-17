"""Read-only trainer reports over a session's history: attendance, poll history, and a
confusion timeline mined from the realtime event outbox.

Mounted under the same ``/trainer`` prefix as ``app/api/v1/endpoints/trainer.py`` (see
``app/api/v1/router.py``) — kept in a separate module purely so this feature can land
without touching that file's owner. Access control mirrors it exactly: a trainer may
only report on sessions belonging to their own batches, an admin may report on any.
"""
import json
import logging
from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.v1.dependencies import get_current_trainer_user
from app.core.constants import UserRole
from app.core.exceptions import ForbiddenError, NotFoundError
from app.crud.training_roster import training_session_crud
from app.db.session import get_db
from app.models.classroom import ClassroomEvent, SessionParticipant, SessionPoll, SessionPollVote
from app.models.user import User
from app.schemas.trainer_reports import (
    AttendanceReportResponse,
    AttendanceRow,
    ConfusionTimelinePoint,
    ConfusionTimelineResponse,
    PollHistoryEntry,
    PollHistoryResponse,
)


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


@router.get(
    "/sessions/{session_id}/confusion-timeline", response_model=ConfusionTimelineResponse
)
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
