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
    Table,
    Column,
    Text,
    UniqueConstraint,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.constants import SessionStatus
from app.models.base import Base, TimestampMixin

batch_programs = Table(
    "training_batch_programs",
    Base.metadata,
    Column("batch_id", Integer, ForeignKey("training_batches.id", ondelete="CASCADE"), primary_key=True),
    Column("program_id", Integer, ForeignKey("training_programs.id", ondelete="CASCADE"), primary_key=True),
)


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
    # sync must never overwrite this. (Legacy column to be dropped in migration)
    # program_id: Mapped[Optional[int]] = ...

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

    is_self_paced: Mapped[bool] = mapped_column(
        Boolean, default=False, server_default="false", nullable=False
    )

    student_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    course_ref: Mapped[Optional[str]] = mapped_column(String(128), nullable=True)

    # Verbatim upstream payload, so fields we haven't modelled yet aren't lost and can
    # be promoted to real columns later without a re-sync.
    raw_json: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    external_updated_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    synced_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)

    programs: Mapped[List["TrainingProgram"]] = relationship(  # noqa: F821
        "TrainingProgram", secondary=batch_programs, back_populates="batches", lazy="selectin"
    )
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

    # Same mint-on-start/release-on-end lifecycle as join_code, but for the live
    # audio/video transport (see app/services/classroom/media.py): a high-entropy,
    # never-displayed secret path segment used to build WHIP/WHEP/HLS URLs against the
    # self-hosted media server. Unlike join_code it is never shown on screen or spoken
    # aloud, so it can afford far more entropy than six digits.
    live_stream_path: Mapped[Optional[str]] = mapped_column(
        String(64), unique=True, index=True, nullable=True
    )

    # Trainer's last-known media state, broadcast to students on change and used to
    # bootstrap a late joiner — same "persist derived live state on the session row"
    # pattern as current_asset_id/timer_started_at above. Reset to defaults on the next
    # start_session, meaningful only while status == live.
    # Whether the trainer has chosen to broadcast camera/mic at all. Deliberately
    # separate from media_camera_off: "camera off" still publishes a stream (audio only,
    # students keep the video frame with a placeholder), whereas broadcasting=False means
    # nothing is published and students get no video frame whatsoever. Starts False every
    # session — going live opens the classroom, it does not open the trainer's camera.
    media_broadcasting: Mapped[bool] = mapped_column(
        Boolean, default=False, server_default="false", nullable=False
    )
    media_mic_muted: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    media_camera_off: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    media_screen_sharing: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    keep_recording: Mapped[bool] = mapped_column(Boolean, default=False, server_default="false", nullable=False)
    questions_are_public: Mapped[bool] = mapped_column(Boolean, default=True, server_default="true", nullable=False)

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

    # Session-level gate for the student portal: null means no assets have been released
    # yet for this session. Set automatically when the first asset is released; cleared
    # when the last asset is un-released. Per-asset granularity lives in
    # SessionAssetRelease — this column exists solely so the portal list query can filter
    # without a subquery per row.
    materials_published_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    materials_published_by_user_id: Mapped[Optional[int]] = mapped_column(
        Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True
    )

    batch: Mapped["TrainingBatch"] = relationship("TrainingBatch", back_populates="sessions")
    module: Mapped[Optional["TrainingModule"]] = relationship("TrainingModule")  # noqa: F821
    current_asset: Mapped[Optional["LectureAsset"]] = relationship("LectureAsset")  # noqa: F821
    asset_releases: Mapped[List["SessionAssetRelease"]] = relationship(
        "SessionAssetRelease", back_populates="session", cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"<TrainingSession(id={self.id}, batch={self.batch_id}, status='{self.status}')>"


class SessionAssetRelease(Base):
    """Per-asset release record for a session's post-class student portal access.

    A row here means the asset is visible to enrolled students in the portal for this
    session. The containing TrainingSession.materials_published_at is automatically
    managed: set when the first row is inserted, cleared when the last is deleted.
    """

    __tablename__ = "session_asset_releases"
    __table_args__ = (
        UniqueConstraint("session_id", "asset_id", name="uq_session_asset_release"),
        Index("ix_session_asset_releases_session", "session_id"),
    )

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    session_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("training_sessions.id", ondelete="CASCADE"), nullable=False
    )
    asset_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("lecture_assets.id", ondelete="CASCADE"), nullable=False
    )
    released_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    released_by_user_id: Mapped[Optional[int]] = mapped_column(
        Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True
    )

    session: Mapped["TrainingSession"] = relationship(
        "TrainingSession", back_populates="asset_releases"
    )

    def __repr__(self) -> str:
        return f"<SessionAssetRelease(session={self.session_id}, asset={self.asset_id})>"


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


class TrainingSessionQuestion(Base, TimestampMixin):
    """A question submitted by a student during a live virtual classroom session."""

    __tablename__ = "training_session_questions"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    session_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("training_sessions.id", ondelete="CASCADE"), nullable=False, index=True
    )
    student_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("training_students.id", ondelete="CASCADE"), nullable=False, index=True
    )
    
    question_text: Mapped[str] = mapped_column(String(500), nullable=False)
    is_answered: Mapped[bool] = mapped_column(Boolean, default=False, server_default="false", nullable=False)
    upvotes: Mapped[int] = mapped_column(Integer, default=0, server_default="0", nullable=False)

    def __repr__(self) -> str:
        return f"<TrainingSessionQuestion(id={self.id}, session={self.session_id}, student={self.student_id})>"


class SessionQuizAttempt(Base, TimestampMixin):
    """One student's graded submission of one quiz asset, in one session.

    Rows are immutable: a retry inserts a new row with the next ``attempt_number``
    rather than overwriting. That keeps the full history a trainer's report needs for
    free, and means "has this student passed?" is a plain EXISTS over ``passed`` — no
    separate progress table to drift out of sync with the attempts that produced it.

    ``total_questions`` is the question count *at grading time*, not the asset's count
    now. A trainer editing a quiz after students have attempted it must not silently
    rescore them, so the two are compared to flag an attempt as stale instead. This
    only catches questions being added or removed — a reworded question, or a changed
    correct answer at the same count, still looks current. Accepted deliberately; a
    content hash is the additive upgrade if that ever matters.
    """

    __tablename__ = "session_quiz_attempts"
    __table_args__ = (
        # The actual double-submit guard. A double-clicked submit or a retried request
        # races two inserts with the same attempt_number and the DB rejects one —
        # client-side disabling alone can't survive two tabs. Same reasoning as
        # SessionPollVote's unique constraint against double voting.
        UniqueConstraint("student_id", "asset_id", "attempt_number", name="uq_quiz_attempt_number"),
        Index("ix_quiz_attempts_session_asset", "session_id", "asset_id"),
        Index("ix_quiz_attempts_student_session", "student_id", "session_id"),
        Index("ix_quiz_attempts_student_module", "student_id", "module_id"),
    )

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    student_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("training_students.id", ondelete="CASCADE"), nullable=False
    )
    session_id: Mapped[Optional[int]] = mapped_column(
        Integer, ForeignKey("training_sessions.id", ondelete="CASCADE"), nullable=True
    )
    module_id: Mapped[Optional[int]] = mapped_column(
        Integer, ForeignKey("training_modules.id", ondelete="CASCADE"), nullable=True
    )
    asset_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("lecture_assets.id", ondelete="CASCADE"), nullable=False
    )

    attempt_number: Mapped[int] = mapped_column(Integer, nullable=False)
    # JSON array of selected option indices, positionally aligned to the quiz's
    # questions. Text rather than a native JSON column so the same DDL works on both
    # SQLite and MySQL — matches options_json/config_json/tags_json elsewhere.
    answers_json: Mapped[str] = mapped_column(Text, nullable=False)

    score: Mapped[int] = mapped_column(Integer, nullable=False)
    total_questions: Mapped[int] = mapped_column(Integer, nullable=False)
    passed: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    attempted_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)

    def __repr__(self) -> str:
        return (
            f"<SessionQuizAttempt(student={self.student_id}, asset={self.asset_id}, "
            f"attempt={self.attempt_number}, score={self.score}/{self.total_questions})>"
        )


class StudentModuleProgress(Base, TimestampMixin):
    """Per-student, per-module progress for self-paced training.

    Created on first access and updated as the student works through the module's
    assets. ``last_asset_index`` is a bookmark so they can resume where they left off.
    ``completed_at`` is set when every required quiz in the module has a passing
    attempt — computed by the endpoint, not maintained by a trigger.
    """

    __tablename__ = "student_module_progress"
    __table_args__ = (
        UniqueConstraint("student_id", "module_id", name="uq_student_module_progress"),
        Index("ix_student_module_progress_student", "student_id"),
    )

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    student_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("training_students.id", ondelete="CASCADE"), nullable=False
    )
    module_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("training_modules.id", ondelete="CASCADE"), nullable=False
    )

    started_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    completed_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    last_accessed_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    last_asset_index: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
