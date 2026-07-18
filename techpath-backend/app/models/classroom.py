"""Live classroom: participants, polls, live code, and the realtime event outbox.

Production runs multiple uvicorn workers (see deploy-backend.yml), so a trainer and a
student can land on different worker processes with no shared memory between them. An
in-memory pub/sub would silently drop half its broadcasts. ``ClassroomEvent`` is the
fix: every state change is inserted here first, and each worker's WebSocket connections
are fed by a small per-session poller reading rows with ``id`` greater than the last one
it saw. Correct under any worker count, no new infrastructure (reuses the DB that is
already there). See ``app/services/classroom/bus.py``.

``SessionParticipant`` is both the attendance record and the identity anchor a browser
tab holds for the rest of the session (poll votes, confusion state) — a student never
gets a Firebase account, just a short-lived signed token minted at ``/classroom/identify``
whose ``sub`` claim is this row's ``participant_key``.
"""
import uuid
from datetime import datetime
from typing import Optional

from sqlalchemy import (
    Boolean,
    DateTime,
    ForeignKey,
    Index,
    Integer,
    String,
    Text,
    UniqueConstraint,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.constants import PollStatus, RecordingStatus
from app.models.base import Base, TimestampMixin

DOUBT_REQUESTED = "doubt_requested"
DOUBT_APPROVED = "doubt_approved"
DOUBT_REJECTED = "doubt_rejected"
DOUBT_COMPLETED = "doubt_completed"

from sqlalchemy import (
    Boolean,
    DateTime,
    ForeignKey,
    Index,
    Integer,
    String,
    Text,
    UniqueConstraint,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.constants import PollStatus, RecordingStatus
from app.models.base import Base, TimestampMixin


class SessionParticipant(Base, TimestampMixin):
    """One browser tab's presence in one session — attendance, confusion state, and the
    identity that poll votes and the WebSocket connection are keyed against."""

    __tablename__ = "session_participants"
    __table_args__ = (
        UniqueConstraint("session_id", "participant_key", name="uq_session_participant_key"),
        Index("ix_session_participants_session", "session_id"),
    )

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    session_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("training_sessions.id", ondelete="CASCADE"), nullable=False
    )
    # Matched by email at identify-time; null for a guest join.
    student_id: Mapped[Optional[int]] = mapped_column(
        Integer, ForeignKey("training_students.id", ondelete="SET NULL"), nullable=True
    )

    participant_key: Mapped[str] = mapped_column(
        String(36), default=lambda: str(uuid.uuid4()), nullable=False
    )
    display_name: Mapped[str] = mapped_column(String(200), nullable=False)
    is_guest: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    first_joined_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    last_seen_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    left_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    is_online: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    is_confused: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    confused_updated_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), nullable=True
    )

    hand_raised: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    hand_raised_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), nullable=True
    )

    # Distinguishes a trainer-initiated removal from an ordinary disconnect — a kicked
    # participant's existing token must not be able to silently rejoin.
    is_removed: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    student: Mapped[Optional["TrainingStudent"]] = relationship("TrainingStudent")  # noqa: F821

    def __repr__(self) -> str:
        return f"<SessionParticipant(session={self.session_id}, name='{self.display_name}')>"


class SessionPoll(Base, TimestampMixin):
    """A trainer-launched poll. ``options_json`` is a JSON array of option strings."""

    __tablename__ = "session_polls"
    __table_args__ = (Index("ix_session_polls_session", "session_id"),)

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    session_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("training_sessions.id", ondelete="CASCADE"), nullable=False
    )
    question: Mapped[str] = mapped_column(String(500), nullable=False)
    options_json: Mapped[str] = mapped_column(Text, nullable=False)
    status: Mapped[str] = mapped_column(
        String(20), default=PollStatus.OPEN.value, nullable=False, index=True
    )
    closed_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    # Set only when this poll was launched from a quiz question — lets the results view
    # highlight the right answer once voting closes. Null for a trainer's own free-form
    # poll, which has no "correct" answer.
    correct_option_index: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)

    votes: Mapped[list["SessionPollVote"]] = relationship(
        "SessionPollVote", back_populates="poll", cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"<SessionPoll(id={self.id}, session={self.session_id}, status='{self.status}')>"


class SessionPollVote(Base):
    """One participant's vote. Unique per (poll, participant) — the DB is the guard
    against double voting, not client-side state."""

    __tablename__ = "session_poll_votes"
    __table_args__ = (
        UniqueConstraint("poll_id", "participant_id", name="uq_poll_vote_participant"),
    )

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    poll_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("session_polls.id", ondelete="CASCADE"), nullable=False
    )
    participant_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("session_participants.id", ondelete="CASCADE"), nullable=False
    )
    option_index: Mapped[int] = mapped_column(Integer, nullable=False)
    voted_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)

    poll: Mapped["SessionPoll"] = relationship("SessionPoll", back_populates="votes")
    participant: Mapped["SessionParticipant"] = relationship("SessionParticipant")


class SessionCodeState(Base, TimestampMixin):
    """The trainer's live-coding buffer. One row per session; overwritten on every
    (debounced) broadcast so a student joining mid-session sees the current content."""

    __tablename__ = "session_code_states"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    session_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("training_sessions.id", ondelete="CASCADE"), unique=True, nullable=False
    )
    language: Mapped[str] = mapped_column(String(50), default="python", nullable=False)
    content: Mapped[str] = mapped_column(Text, default="", nullable=False)


class ClassroomEvent(Base):
    """Append-only outbox. ``id`` is the polling cursor every worker's broadcaster
    tracks per session — never updated, never deleted on the hot path."""

    __tablename__ = "classroom_events"
    __table_args__ = (Index("ix_classroom_events_session_id", "session_id", "id"),)

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    session_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("training_sessions.id", ondelete="CASCADE"), nullable=False
    )
    event_type: Mapped[str] = mapped_column(String(50), nullable=False)
    payload_json: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)

    def __repr__(self) -> str:
        return f"<ClassroomEvent(id={self.id}, session={self.session_id}, type='{self.event_type}')>"


class SessionRecording(Base, TimestampMixin):
    """The VOD produced from one session's live media, if it had any (see
    ``end_session``: created only when the session had a ``live_stream_path``).
    ``recording_path`` is the source file on the media server, used only to build the
    transcode request; ``watch_url`` is what a client actually links to once ready."""

    __tablename__ = "session_recordings"
    __table_args__ = (Index("ix_session_recordings_session_id", "session_id"),)

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    session_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("training_sessions.id", ondelete="CASCADE"), nullable=False
    )
    status: Mapped[str] = mapped_column(
        String(20), default=RecordingStatus.PROCESSING.value, nullable=False, index=True
    )
    recording_path: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    watch_url: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)

    def __repr__(self) -> str:
        return f"<SessionRecording(id={self.id}, session={self.session_id}, status='{self.status}')>"

class DoubtRequest(Base, TimestampMixin):
    """A student's request to speak via push-to-talk audio."""
    __tablename__ = "doubt_requests"
    __table_args__ = (Index("ix_doubt_requests_session_id", "session_id"),)

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    session_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("training_sessions.id", ondelete="CASCADE"), nullable=False
    )
    participant_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("session_participants.id", ondelete="CASCADE"), nullable=False
    )
    status: Mapped[str] = mapped_column(
        String(20), default="pending", nullable=False, index=True
    )

    participant: Mapped["SessionParticipant"] = relationship("SessionParticipant")

