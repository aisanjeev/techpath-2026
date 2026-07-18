"""CRUD for live classroom participants, polls, votes, and the live-code buffer."""
import uuid
from datetime import datetime, timezone
from typing import Any, Optional

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models.classroom import (
    DoubtRequest,
    SessionCodeState,
    SessionParticipant,
    SessionPoll,
    SessionPollVote,
    SessionRecording,
)
from app.models.training_roster import TrainingBatchStudent, TrainingStudent


class CRUDSessionParticipant(CRUDBase[SessionParticipant, Any, Any]):
    async def get_by_key(
        self, db: AsyncSession, session_id: int, participant_key: str
    ) -> Optional[SessionParticipant]:
        result = await db.execute(
            select(SessionParticipant).where(
                SessionParticipant.session_id == session_id,
                SessionParticipant.participant_key == participant_key,
            )
        )
        return result.scalar_one_or_none()

    async def find_student_in_batch(
        self, db: AsyncSession, batch_id: int, email: str
    ) -> Optional[TrainingStudent]:
        """A roster-email match, scoped to the batch this session belongs to — matching
        against the global student table alone would let anyone with any roster email
        talk their way into a session for a batch they were never enrolled in."""
        result = await db.execute(
            select(TrainingStudent)
            .join(TrainingBatchStudent, TrainingBatchStudent.student_id == TrainingStudent.id)
            .where(
                TrainingBatchStudent.batch_id == batch_id,
                func.lower(TrainingStudent.email) == email.lower(),
            )
        )
        return result.scalar_one_or_none()

    async def join(
        self,
        db: AsyncSession,
        *,
        session_id: int,
        display_name: str,
        student_id: Optional[int],
        is_guest: bool,
    ) -> SessionParticipant:
        """Always mints a fresh participant row — a rejoin (new tab, cleared storage)
        is a new attendance entry, not silently merged into an old one. Reconnects
        within the same browser session go through ``touch()`` instead, keyed by the
        participant_key already held client-side."""
        now = datetime.now(timezone.utc)
        participant = SessionParticipant(
            session_id=session_id,
            student_id=student_id,
            participant_key=str(uuid.uuid4()),
            display_name=display_name,
            is_guest=is_guest,
            first_joined_at=now,
            last_seen_at=now,
            is_online=True,
        )
        db.add(participant)
        await db.flush()
        await db.refresh(participant)
        return participant

    async def touch(self, db: AsyncSession, participant: SessionParticipant) -> SessionParticipant:
        """Reconnect: same participant_key, so update presence rather than re-join."""
        participant.last_seen_at = datetime.now(timezone.utc)
        participant.is_online = True
        participant.left_at = None
        db.add(participant)
        await db.flush()
        return participant

    async def mark_offline(self, db: AsyncSession, participant: SessionParticipant) -> None:
        participant.is_online = False
        participant.left_at = datetime.now(timezone.utc)
        db.add(participant)
        await db.flush()

    async def set_confusion(
        self, db: AsyncSession, participant: SessionParticipant, confused: bool
    ) -> SessionParticipant:
        participant.is_confused = confused
        participant.confused_updated_at = datetime.now(timezone.utc)
        db.add(participant)
        await db.flush()
        return participant

    async def set_hand_raised(
        self, db: AsyncSession, participant: SessionParticipant, raised: bool
    ) -> SessionParticipant:
        """Mirrors ``set_confusion``. ``hand_raised_at`` is cleared on lowering (rather
        than left stale) so a re-raise always sorts to the back of the queue, same as a
        student who is only now asking."""
        participant.hand_raised = raised
        participant.hand_raised_at = datetime.now(timezone.utc) if raised else None
        db.add(participant)
        await db.flush()
        return participant

    async def kick(
        self, db: AsyncSession, participant: SessionParticipant
    ) -> SessionParticipant:
        """Trainer-initiated removal. Distinct from ``mark_offline``: this also flips
        ``is_removed`` so the participant's still-valid token can't silently rejoin (see
        ``get_current_participant`` and the WebSocket connect handler)."""
        participant.is_removed = True
        participant.is_online = False
        participant.left_at = datetime.now(timezone.utc)
        db.add(participant)
        await db.flush()
        return participant

    async def list_for_session(
        self, db: AsyncSession, session_id: int
    ) -> list[SessionParticipant]:
        result = await db.execute(
            select(SessionParticipant)
            .where(SessionParticipant.session_id == session_id)
            .order_by(SessionParticipant.is_online.desc(), SessionParticipant.display_name)
        )
        return list(result.scalars().all())

    async def hands_raised_queue(
        self, db: AsyncSession, session_id: int
    ) -> list[SessionParticipant]:
        """Participants with a hand up, first-raised first — the order a trainer should
        call on them in."""
        result = await db.execute(
            select(SessionParticipant)
            .where(
                SessionParticipant.session_id == session_id,
                SessionParticipant.hand_raised.is_(True),
            )
            .order_by(SessionParticipant.hand_raised_at.asc())
        )
        return list(result.scalars().all())

    async def confusion_summary(self, db: AsyncSession, session_id: int) -> dict:
        online = await db.execute(
            select(func.count(SessionParticipant.id)).where(
                SessionParticipant.session_id == session_id,
                SessionParticipant.is_online.is_(True),
            )
        )
        confused = await db.execute(
            select(func.count(SessionParticipant.id)).where(
                SessionParticipant.session_id == session_id,
                SessionParticipant.is_online.is_(True),
                SessionParticipant.is_confused.is_(True),
            )
        )
        online_count = online.scalar() or 0
        confused_count = confused.scalar() or 0
        return {
            "online": online_count,
            "confused": confused_count,
            "ratio": (confused_count / online_count) if online_count else 0.0,
        }


class CRUDSessionPoll(CRUDBase[SessionPoll, Any, Any]):
    async def get_open_poll(self, db: AsyncSession, session_id: int) -> Optional[SessionPoll]:
        result = await db.execute(
            select(SessionPoll)
            .where(SessionPoll.session_id == session_id, SessionPoll.status == "open")
            .order_by(SessionPoll.id.desc())
        )
        return result.scalars().first()

    async def tally(self, db: AsyncSession, poll_id: int) -> dict[int, int]:
        result = await db.execute(
            select(SessionPollVote.option_index, func.count(SessionPollVote.id))
            .where(SessionPollVote.poll_id == poll_id)
            .group_by(SessionPollVote.option_index)
        )
        return dict(result.all())


class CRUDSessionPollVote(CRUDBase[SessionPollVote, Any, Any]):
    async def cast(
        self, db: AsyncSession, *, poll_id: int, participant_id: int, option_index: int
    ) -> SessionPollVote:
        """A voter can change their mind — upsert rather than reject the second call."""
        result = await db.execute(
            select(SessionPollVote).where(
                SessionPollVote.poll_id == poll_id,
                SessionPollVote.participant_id == participant_id,
            )
        )
        existing = result.scalar_one_or_none()
        if existing:
            existing.option_index = option_index
            existing.voted_at = datetime.now(timezone.utc)
            db.add(existing)
            await db.flush()
            return existing

        vote = SessionPollVote(
            poll_id=poll_id,
            participant_id=participant_id,
            option_index=option_index,
            voted_at=datetime.now(timezone.utc),
        )
        db.add(vote)
        await db.flush()
        return vote

    async def get_for_participant(
        self, db: AsyncSession, poll_id: int, participant_id: int
    ) -> Optional[SessionPollVote]:
        result = await db.execute(
            select(SessionPollVote).where(
                SessionPollVote.poll_id == poll_id,
                SessionPollVote.participant_id == participant_id,
            )
        )
        return result.scalar_one_or_none()


class CRUDSessionCodeState(CRUDBase[SessionCodeState, Any, Any]):
    async def get_for_session(
        self, db: AsyncSession, session_id: int
    ) -> Optional[SessionCodeState]:
        result = await db.execute(
            select(SessionCodeState).where(SessionCodeState.session_id == session_id)
        )
        return result.scalar_one_or_none()

    async def upsert(
        self, db: AsyncSession, *, session_id: int, language: str, content: str
    ) -> SessionCodeState:
        existing = await self.get_for_session(db, session_id)
        if existing:
            existing.language = language
            existing.content = content
            db.add(existing)
            await db.flush()
            return existing

        state = SessionCodeState(session_id=session_id, language=language, content=content)
        db.add(state)
        await db.flush()
        return state


class CRUDSessionRecording(CRUDBase[SessionRecording, Any, Any]):
    async def get_by_session(
        self, db: AsyncSession, session_id: int
    ) -> Optional[SessionRecording]:
        """The most recent recording for a session — CRUD-layer note in
        data-model.md: no DB-level uniqueness is enforced, so this is "latest wins"
        rather than "the only one that could exist"."""
        result = await db.execute(
            select(SessionRecording)
            .where(SessionRecording.session_id == session_id)
            .order_by(SessionRecording.id.desc())
        )
        return result.scalars().first()


session_participant_crud = CRUDSessionParticipant(SessionParticipant)
session_poll_crud = CRUDSessionPoll(SessionPoll)
session_poll_vote_crud = CRUDSessionPollVote(SessionPollVote)
session_code_state_crud = CRUDSessionCodeState(SessionCodeState)
session_recording_crud = CRUDSessionRecording(SessionRecording)

class CRUDDoubtRequest(CRUDBase[DoubtRequest, Any, Any]):
    async def create_request(
        self, db: AsyncSession, *, session_id: int, participant_id: int
    ) -> DoubtRequest:
        req = DoubtRequest(session_id=session_id, participant_id=participant_id, status="pending")
        db.add(req)
        await db.flush()
        return req

    async def get_for_participant(
        self, db: AsyncSession, session_id: int, participant_id: int
    ) -> Optional[DoubtRequest]:
        result = await db.execute(
            select(DoubtRequest).where(
                DoubtRequest.session_id == session_id,
                DoubtRequest.participant_id == participant_id,
            ).order_by(DoubtRequest.id.desc())
        )
        return result.scalars().first()

    async def list_pending(
        self, db: AsyncSession, session_id: int
    ) -> list[DoubtRequest]:
        result = await db.execute(
            select(DoubtRequest)
            .where(DoubtRequest.session_id == session_id, DoubtRequest.status == "pending")
            .order_by(DoubtRequest.created_at.asc())
        )
        return list(result.scalars().all())

    async def list_by_session(
        self, db: AsyncSession, session_id: int, statuses: list[str] = None
    ) -> list[DoubtRequest]:
        from sqlalchemy.orm import joinedload
        stmt = (
            select(DoubtRequest)
            .options(joinedload(DoubtRequest.participant))
            .where(DoubtRequest.session_id == session_id)
        )
        if statuses:
            stmt = stmt.where(DoubtRequest.status.in_(statuses))
        result = await db.execute(stmt.order_by(DoubtRequest.created_at.asc()))
        return list(result.scalars().all())

    async def update_status(
        self, db: AsyncSession, doubt_id: int, status: str
    ) -> Optional[DoubtRequest]:
        from sqlalchemy.orm import joinedload
        result = await db.execute(
            select(DoubtRequest)
            .options(joinedload(DoubtRequest.participant))
            .where(DoubtRequest.id == doubt_id)
        )
        req = result.scalar_one_or_none()
        if req:
            req.status = status
            db.add(req)
            await db.flush()
        return req

doubt_request_crud = CRUDDoubtRequest(DoubtRequest)
