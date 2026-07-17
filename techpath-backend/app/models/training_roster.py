"""Local mirror of batches and students owned by the external roster API.

These tables are a cache, not a source of truth. Everything except ``program_id`` is
overwritten by the sync; the external system owns it. We mirror rather than proxy for
two reasons that matter: an offline classroom has to resolve its roster with no network
at all, and mapping a trainer to their batches by email would otherwise fan out into a
request per dashboard load.

``external_id`` is the join key and is expected to be immutable upstream. Our integer
primary keys are internal and are never exposed to the external system.
"""
from datetime import date, datetime
from typing import List, Optional

from sqlalchemy import (
    Boolean,
    Date,
    DateTime,
    ForeignKey,
    Index,
    Integer,
    String,
    Text,
    UniqueConstraint,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.constants import SessionStatus
from app.models.base import Base, TimestampMixin


class TrainingBatch(Base, TimestampMixin):
    """A mirrored cohort."""

    __tablename__ = "training_batches"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    external_id: Mapped[str] = mapped_column(
        String(128), unique=True, index=True, nullable=False
    )

    name: Mapped[str] = mapped_column(String(255), nullable=False)
    code: Mapped[Optional[str]] = mapped_column(String(100), nullable=True, index=True)

    # Ours, not theirs. Set by an admin to link a batch to its training content; the
    # sync must never overwrite this.
    program_id: Mapped[Optional[int]] = mapped_column(
        Integer, ForeignKey("training_programs.id", ondelete="SET NULL"), nullable=True
    )

    start_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    end_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    timezone: Mapped[Optional[str]] = mapped_column(String(64), nullable=True)
    schedule_json: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    status: Mapped[Optional[str]] = mapped_column(String(50), nullable=True, index=True)
    mode: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)
    location: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)

    # The mapping key: matched against the TechPath login email of a trainer.
    trainer_email: Mapped[Optional[str]] = mapped_column(String(255), nullable=True, index=True)
    trainer_external_id: Mapped[Optional[str]] = mapped_column(String(128), nullable=True)
    trainer_name: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)

    student_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    course_ref: Mapped[Optional[str]] = mapped_column(String(128), nullable=True)

    # Verbatim upstream payload, so fields we haven't modelled yet aren't lost and can
    # be promoted to real columns later without a re-sync.
    raw_json: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    external_updated_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    synced_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)

    program: Mapped[Optional["TrainingProgram"]] = relationship("TrainingProgram")  # noqa: F821
    memberships: Mapped[List["TrainingBatchStudent"]] = relationship(
        "TrainingBatchStudent", back_populates="batch", cascade="all, delete-orphan"
    )
    sessions: Mapped[List["TrainingSession"]] = relationship(
        "TrainingSession", back_populates="batch", cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"<TrainingBatch(id={self.id}, external_id='{self.external_id}')>"


class TrainingStudent(Base, TimestampMixin):
    """A mirrored student. Global identity — may belong to several batches."""

    __tablename__ = "training_students"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    external_id: Mapped[str] = mapped_column(
        String(128), unique=True, index=True, nullable=False
    )

    name: Mapped[str] = mapped_column(String(255), nullable=False)
    email: Mapped[Optional[str]] = mapped_column(String(255), nullable=True, index=True)
    phone: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    roll_no: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    status: Mapped[Optional[str]] = mapped_column(String(50), nullable=True, index=True)
    photo_url: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    enrolled_on: Mapped[Optional[date]] = mapped_column(Date, nullable=True)

    # Linked on first successful Gmail sign-in to the student portal, matched against
    # `email` above — never set by the roster sync itself. Mirrors User.firebase_uid,
    # but deliberately lives on a separate table: a student is not a `User` and must
    # never gain role-gated access by being resolved through that model instead of
    # this one. Null means this student has never signed in to the portal.
    firebase_uid: Mapped[Optional[str]] = mapped_column(
        String(128), unique=True, index=True, nullable=True
    )

    raw_json: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    external_updated_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    synced_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)

    memberships: Mapped[List["TrainingBatchStudent"]] = relationship(
        "TrainingBatchStudent", back_populates="student", cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"<TrainingStudent(id={self.id}, external_id='{self.external_id}')>"


class TrainingBatchStudent(Base):
    """Batch membership. Many-to-many: a student can attend more than one batch."""

    __tablename__ = "training_batch_students"
    __table_args__ = (UniqueConstraint("batch_id", "student_id", name="uq_batch_student"),)

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    batch_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("training_batches.id", ondelete="CASCADE"), nullable=False
    )
    student_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("training_students.id", ondelete="CASCADE"), nullable=False
    )
    membership_status: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    enrolled_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), nullable=True
    )

    batch: Mapped["TrainingBatch"] = relationship("TrainingBatch", back_populates="memberships")
    student: Mapped["TrainingStudent"] = relationship(
        "TrainingStudent", back_populates="memberships"
    )


class TrainingSession(Base, TimestampMixin):
    """A scheduled or running class: one batch teaching one module.

    Thin for now — starting a session flips its status and mints a join code, and that
    is all. It exists already so that the trainer flow operates on a real row, and so
    the live-classroom work has something to hang attendance, polls and progress off
    without a migration on a hot table.
    """

    __tablename__ = "training_sessions"
    __table_args__ = (Index("ix_training_sessions_batch_start", "batch_id", "scheduled_start"),)

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    batch_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("training_batches.id", ondelete="CASCADE"), nullable=False
    )
    module_id: Mapped[Optional[int]] = mapped_column(
        Integer, ForeignKey("training_modules.id", ondelete="SET NULL"), nullable=True
    )
    trainer_user_id: Mapped[Optional[int]] = mapped_column(
        Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True
    )

    title: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    scheduled_start: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), nullable=True, index=True
    )
    scheduled_end: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    status: Mapped[str] = mapped_column(
        String(50), default=SessionStatus.SCHEDULED.value, nullable=False, index=True
    )

    # Minted when presenting starts; students join with it. Unique only among live
    # sessions in practice — it is released back when the session ends.
    join_code: Mapped[Optional[str]] = mapped_column(
        String(6), unique=True, index=True, nullable=True
    )

    started_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    ended_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)

    # The asset the trainer is currently showing — session state, not just an event, so
    # a student joining mid-session (or reconnecting) can bootstrap it directly rather
    # than replaying the event log looking for the last slide_change.
    current_asset_id: Mapped[Optional[int]] = mapped_column(
        Integer, ForeignKey("lecture_assets.id", ondelete="SET NULL"), nullable=True
    )

    # A countdown the trainer started, broadcast to every client. Persisted (not just an
    # event) for the same reason current_asset_id is: a client bootstrapping mid-timer
    # needs to compute remaining time from started_at, not from a message it may have
    # missed. Both null when no timer is running.
    timer_started_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    timer_duration_seconds: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)

    # Whole-session publish switch for the post-session student portal: null means the
    # module's assets aren't visible to any student yet, regardless of who attended.
    # Deliberately session-wide, not per-asset — a trainer un/republishes the whole
    # thing, not individual pieces.
    materials_published_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    materials_published_by_user_id: Mapped[Optional[int]] = mapped_column(
        Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True
    )

    batch: Mapped["TrainingBatch"] = relationship("TrainingBatch", back_populates="sessions")
    module: Mapped[Optional["TrainingModule"]] = relationship("TrainingModule")  # noqa: F821
    current_asset: Mapped[Optional["LectureAsset"]] = relationship("LectureAsset")  # noqa: F821

    def __repr__(self) -> str:
        return f"<TrainingSession(id={self.id}, batch={self.batch_id}, status='{self.status}')>"


class TrainingSyncState(Base, TimestampMixin):
    """Bookkeeping for the incremental roster sync, one row per resource."""

    __tablename__ = "training_sync_state"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    resource: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)

    # High-water mark passed back as ?updated_since= on the next run.
    cursor_updated_since: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), nullable=True
    )

    last_run_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    last_success_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    last_status: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    last_error: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    records_processed: Mapped[int] = mapped_column(Integer, default=0, nullable=False)

    # Overlap guard. Production runs multiple workers and the UI exposes a manual
    # "Sync now" button, so two syncs can otherwise interleave and double-apply.
    is_running: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    run_started_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), nullable=True
    )

    def __repr__(self) -> str:
        return f"<TrainingSyncState(resource='{self.resource}', last_status='{self.last_status}')>"
