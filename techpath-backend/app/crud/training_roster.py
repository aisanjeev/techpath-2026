"""CRUD for the roster mirror and training sessions."""
import random
import string
from datetime import date, datetime, time, timedelta, timezone
from typing import Any, List, Optional

from sqlalchemy import case, func, or_, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.core.constants import SessionStatus
from app.crud.base import CRUDBase
from app.models.classroom import SessionParticipant
from app.services.classroom import media
from app.models.training import TrainingModule, TrainingProgram
from app.models.training_roster import (
    StudentModuleProgress,
    TrainingBatch,
    TrainingBatchStudent,
    TrainingSession,
    TrainingStudent,
    TrainingSyncState,
)

JOIN_CODE_ALPHABET = string.digits
JOIN_CODE_LENGTH = 6


class CRUDTrainingBatch(CRUDBase[TrainingBatch, Any, Any]):
    async def get_by_external_id(
        self, db: AsyncSession, external_id: str
    ) -> Optional[TrainingBatch]:
        result = await db.execute(
            select(TrainingBatch).where(TrainingBatch.external_id == external_id)
        )
        return result.scalar_one_or_none()

    async def get_by_trainer_email(
        self, db: AsyncSession, email: str, *, status: Optional[str] = None
    ) -> List[TrainingBatch]:
        """Batches assigned to a trainer. Email is the agreed mapping key, and is
        compared case-insensitively because the two systems don't share a keyboard."""
        query = select(TrainingBatch).where(
            func.lower(TrainingBatch.trainer_email) == email.lower()
        )
        if status:
            query = query.where(TrainingBatch.status == status)
        result = await db.execute(query.order_by(TrainingBatch.start_date.desc()))
        return list(result.scalars().all())

    async def search(
        self,
        db: AsyncSession,
        *,
        skip: int = 0,
        limit: int = 20,
        status: Optional[str] = None,
        trainer_email: Optional[str] = None,
        search: Optional[str] = None,
    ) -> tuple[List[TrainingBatch], int]:
        query = select(TrainingBatch)
        count_query = select(func.count(TrainingBatch.id))

        conditions = []
        if status:
            conditions.append(TrainingBatch.status == status)
        if trainer_email:
            conditions.append(func.lower(TrainingBatch.trainer_email) == trainer_email.lower())
        if search:
            term = f"%{search}%"
            conditions.append(
                or_(
                    TrainingBatch.name.ilike(term),
                    TrainingBatch.code.ilike(term),
                    TrainingBatch.external_id.ilike(term),
                )
            )

        for cond in conditions:
            query = query.where(cond)
            count_query = count_query.where(cond)

        query = query.order_by(TrainingBatch.start_date.desc(), TrainingBatch.id.desc())
        rows = list((await db.execute(query.offset(skip).limit(limit))).scalars().all())
        total = (await db.execute(count_query)).scalar() or 0
        return rows, total

    async def students(self, db: AsyncSession, batch_id: int) -> List[TrainingStudent]:
        result = await db.execute(
            select(TrainingStudent)
            .join(TrainingBatchStudent, TrainingBatchStudent.student_id == TrainingStudent.id)
            .where(TrainingBatchStudent.batch_id == batch_id)
            .order_by(TrainingStudent.name)
        )
        return list(result.scalars().all())


class CRUDTrainingStudent(CRUDBase[TrainingStudent, Any, Any]):
    async def get_by_external_id(
        self, db: AsyncSession, external_id: str
    ) -> Optional[TrainingStudent]:
        result = await db.execute(
            select(TrainingStudent).where(TrainingStudent.external_id == external_id)
        )
        return result.scalar_one_or_none()

    async def get_by_firebase_uid(
        self, db: AsyncSession, firebase_uid: str
    ) -> Optional[TrainingStudent]:
        result = await db.execute(
            select(TrainingStudent).where(TrainingStudent.firebase_uid == firebase_uid)
        )
        return result.scalar_one_or_none()

    async def get_by_email(self, db: AsyncSession, email: str) -> Optional[TrainingStudent]:
        """Case-insensitive — the roster and Google don't share a keyboard either."""
        result = await db.execute(
            select(TrainingStudent).where(func.lower(TrainingStudent.email) == email.lower())
        )
        return result.scalar_one_or_none()

    async def get_or_link_from_firebase(
        self, db: AsyncSession, firebase_uid: str, email: str
    ) -> Optional[TrainingStudent]:
        """Resolve a Firebase-authenticated student portal sign-in to a roster row.

        Unlike ``CRUDUser.get_or_create_from_firebase``, this never creates a row —
        ``training_students`` is a mirror of an external roster (see module docstring),
        so "not in the roster" must mean "no access", not "provision a new record". A
        Gmail account is proof of an email address, never proof of roster membership.

        Primary lookup is by firebase_uid (fast path for a returning student). First-time
        sign-in falls back to matching by email and links this uid to that row — but only
        when the row isn't already linked to a *different* uid, so a stale or duplicate
        roster email can't be used to hijack an already-claimed student's materials.
        """
        student = await self.get_by_firebase_uid(db, firebase_uid)
        if student:
            return student

        student = await self.get_by_email(db, email)
        if student and student.firebase_uid is None:
            student.firebase_uid = firebase_uid
            db.add(student)
            await db.flush()
            await db.refresh(student)
            return student

        return None

    async def search(
        self,
        db: AsyncSession,
        *,
        skip: int = 0,
        limit: int = 20,
        status: Optional[str] = None,
        batch_id: Optional[int] = None,
        search: Optional[str] = None,
    ) -> tuple[List[TrainingStudent], int]:
        query = select(TrainingStudent)
        count_query = select(func.count(TrainingStudent.id))

        if batch_id is not None:
            query = query.join(
                TrainingBatchStudent, TrainingBatchStudent.student_id == TrainingStudent.id
            ).where(TrainingBatchStudent.batch_id == batch_id)
            count_query = count_query.join(
                TrainingBatchStudent, TrainingBatchStudent.student_id == TrainingStudent.id
            ).where(TrainingBatchStudent.batch_id == batch_id)

        conditions = []
        if status:
            conditions.append(TrainingStudent.status == status)
        if search:
            term = f"%{search}%"
            conditions.append(
                or_(
                    TrainingStudent.name.ilike(term),
                    TrainingStudent.email.ilike(term),
                    TrainingStudent.roll_no.ilike(term),
                )
            )
        for cond in conditions:
            query = query.where(cond)
            count_query = count_query.where(cond)

        query = query.order_by(TrainingStudent.name)
        rows = list((await db.execute(query.offset(skip).limit(limit))).scalars().all())
        total = (await db.execute(count_query)).scalar() or 0
        return rows, total

    async def batch_ids(self, db: AsyncSession, student_id: int) -> List[int]:
        result = await db.execute(
            select(TrainingBatchStudent.batch_id).where(
                TrainingBatchStudent.student_id == student_id
            )
        )
        return [row[0] for row in result.all()]


class CRUDTrainingSession(CRUDBase[TrainingSession, Any, Any]):
    async def get_with_relations(self, db: AsyncSession, id: int) -> Optional[TrainingSession]:
        result = await db.execute(
            select(TrainingSession)
            .where(TrainingSession.id == id)
            .options(
                selectinload(TrainingSession.batch), selectinload(TrainingSession.module)
            )
        )
        return result.scalar_one_or_none()

    async def get_by_join_code(self, db: AsyncSession, join_code: str) -> Optional[TrainingSession]:
        """The public classroom entry point. Only a ``live`` session's code is
        meant to work — join codes are released back to the pool once a session ends,
        so a code that resolves to an ended row is stale, not a valid classroom."""
        result = await db.execute(
            select(TrainingSession)
            .where(TrainingSession.join_code == join_code)
            .options(
                selectinload(TrainingSession.batch), selectinload(TrainingSession.module)
            )
        )
        return result.scalar_one_or_none()

    async def get_other_live_session(
        self, db: AsyncSession, batch_id: int, exclude_session_id: int
    ) -> Optional[TrainingSession]:
        """Is some *other* session for this batch already live? Used to stop a batch
        from ever having two simultaneous live broadcasts (FR-015) — excludes
        ``exclude_session_id`` itself so restarting/re-entering the same session is
        never mistaken for a conflict."""
        result = await db.execute(
            select(TrainingSession).where(
                TrainingSession.batch_id == batch_id,
                TrainingSession.status == SessionStatus.LIVE.value,
                TrainingSession.id != exclude_session_id,
            )
        )
        return result.scalars().first()

    async def list_for_batch(self, db: AsyncSession, batch_id: int) -> List[TrainingSession]:
        result = await db.execute(
            select(TrainingSession)
            .where(TrainingSession.batch_id == batch_id)
            .order_by(
                case((TrainingSession.scheduled_start.is_(None), 1), else_=0),
                TrainingSession.scheduled_start.desc(),
            )
            .options(selectinload(TrainingSession.module))
        )
        return list(result.scalars().all())

    async def get_today_for_trainer(
        self, db: AsyncSession, trainer_email: str, *, on: Optional[date] = None
    ) -> List[TrainingSession]:
        """Sessions for this trainer's batches today, plus anything already live.

        A session that ran past midnight is still the session they are teaching, so
        live ones are included regardless of their scheduled date.
        """
        day = on or datetime.now(timezone.utc).date()
        start = datetime.combine(day, time.min, tzinfo=timezone.utc)
        end = start + timedelta(days=1)

        result = await db.execute(
            select(TrainingSession)
            .join(TrainingBatch, TrainingSession.batch_id == TrainingBatch.id)
            .where(
                func.lower(TrainingBatch.trainer_email) == trainer_email.lower(),
                or_(
                    TrainingSession.scheduled_start.between(start, end),
                    TrainingSession.status == SessionStatus.LIVE.value,
                ),
            )
            .order_by(
                case((TrainingSession.scheduled_start.is_(None), 1), else_=0),
                TrainingSession.scheduled_start,
            )
            .options(selectinload(TrainingSession.batch), selectinload(TrainingSession.module))
        )
        return list(result.scalars().all())

    async def list_published_for_student(
        self, db: AsyncSession, student_id: int
    ) -> List[TrainingSession]:
        """The durable student-portal list: every session in a batch this student is
        enrolled in that a trainer has since published. Ordered most-recent
        class first, using whichever of started_at/scheduled_start is set — a session
        can be published without ``started_at`` in the unlikely case it was published
        before ever going live, though in practice publish only makes sense after."""
        result = await db.execute(
            select(TrainingSession)
            .join(
                TrainingBatchStudent,
                TrainingBatchStudent.batch_id == TrainingSession.batch_id,
            )
            .where(
                TrainingBatchStudent.student_id == student_id,
                TrainingSession.materials_published_at.isnot(None),
            )
            .order_by(
                func.coalesce(
                    TrainingSession.started_at, TrainingSession.scheduled_start
                ).desc()
            )
            .options(selectinload(TrainingSession.batch), selectinload(TrainingSession.module))
        )
        return list(result.scalars().unique().all())

    async def get_published_by_batch_and_module(
        self, db: AsyncSession, batch_id: int, module_id: int
    ) -> Optional[TrainingSession]:
        """Returns the first published session for this batch and module, if any exists."""
        result = await db.execute(
            select(TrainingSession).where(
                TrainingSession.batch_id == batch_id,
                TrainingSession.module_id == module_id,
                TrainingSession.materials_published_at.isnot(None),
            )
        )
        return result.scalars().first()

    async def get_enrolled_published(
        self, db: AsyncSession, session_id: int, student_id: int
    ) -> Optional[TrainingSession]:
        """A single session, but only if this exact student is enrolled in its batch
        and it has since been published — the gate ``GET /student/sessions/{id}/materials``
        relies on. Returns None for "doesn't exist", "not in batch", and "not published
        yet" alike, deliberately indistinguishable to the caller so a student can't
        probe session ids to learn which ones exist or who was in them."""
        result = await db.execute(
            select(TrainingSession)
            .join(
                TrainingBatchStudent,
                TrainingBatchStudent.batch_id == TrainingSession.batch_id,
            )
            .where(
                TrainingSession.id == session_id,
                TrainingBatchStudent.student_id == student_id,
                TrainingSession.materials_published_at.isnot(None),
            )
            .options(selectinload(TrainingSession.batch), selectinload(TrainingSession.module))
        )
        return result.scalar_one_or_none()

    async def mint_live_media(self, db: AsyncSession, session: TrainingSession) -> None:
        """Start publishing eligibility: mint the stream path if this session doesn't
        already have one. Mirrors ``join_code``'s mint-on-start lifecycle, but is
        idempotent for an already-live session (restarting must not invalidate a
        trainer's already-open publish connection)."""
        if session.live_stream_path:
            return
        session.live_stream_path = media.mint_live_stream_path(session.id)
        db.add(session)
        await db.flush()

    async def release_live_media(self, db: AsyncSession, session: TrainingSession) -> None:
        """Release the stream path back — same moment ``join_code`` is released."""
        if not session.live_stream_path:
            return
        session.live_stream_path = None
        db.add(session)
        await db.flush()

    async def generate_join_code(self, db: AsyncSession) -> str:
        """Mint a code not currently held by another session.

        Codes are released when a session ends, so the space only needs to be unique
        among the handful that are live at once.
        """
        for _ in range(50):
            code = "".join(random.choices(JOIN_CODE_ALPHABET, k=JOIN_CODE_LENGTH))
            taken = await db.execute(
                select(TrainingSession.id).where(TrainingSession.join_code == code)
            )
            if taken.scalar_one_or_none() is None:
                return code
        raise RuntimeError("Could not allocate a unique join code")


class CRUDSyncState(CRUDBase[TrainingSyncState, Any, Any]):
    async def all_states(self, db: AsyncSession) -> List[TrainingSyncState]:
        result = await db.execute(select(TrainingSyncState).order_by(TrainingSyncState.resource))
        return list(result.scalars().all())

    async def get_by_resource(
        self, db: AsyncSession, resource: str
    ) -> Optional[TrainingSyncState]:
        result = await db.execute(
            select(TrainingSyncState).where(TrainingSyncState.resource == resource)
        )
        return result.scalar_one_or_none()


class CRUDStudentModuleProgress(CRUDBase[StudentModuleProgress, Any, Any]):
    async def get_for_student_module(
        self, db: AsyncSession, student_id: int, module_id: int
    ) -> Optional[StudentModuleProgress]:
        result = await db.execute(
            select(StudentModuleProgress).where(
                StudentModuleProgress.student_id == student_id,
                StudentModuleProgress.module_id == module_id,
            )
        )
        return result.scalar_one_or_none()

    async def upsert(
        self,
        db: AsyncSession,
        student_id: int,
        module_id: int,
        *,
        last_asset_index: int = 0,
        completed: bool = False,
    ) -> StudentModuleProgress:
        from datetime import datetime, timezone

        now = datetime.now(timezone.utc)
        progress = await self.get_for_student_module(db, student_id, module_id)
        if progress is None:
            progress = StudentModuleProgress(
                student_id=student_id,
                module_id=module_id,
                started_at=now,
                last_accessed_at=now,
                last_asset_index=last_asset_index,
            )
            db.add(progress)
        else:
            progress.last_accessed_at = now
            progress.last_asset_index = last_asset_index
        if completed and progress.completed_at is None:
            progress.completed_at = now
        await db.flush()
        return progress

    async def list_for_student(
        self, db: AsyncSession, student_id: int
    ) -> List[StudentModuleProgress]:
        result = await db.execute(
            select(StudentModuleProgress).where(
                StudentModuleProgress.student_id == student_id
            )
        )
        return list(result.scalars().all())

    async def list_for_student_modules(
        self, db: AsyncSession, student_id: int, module_ids: List[int]
    ) -> List[StudentModuleProgress]:
        if not module_ids:
            return []
        result = await db.execute(
            select(StudentModuleProgress).where(
                StudentModuleProgress.student_id == student_id,
                StudentModuleProgress.module_id.in_(module_ids),
            )
        )
        return list(result.scalars().all())

    async def self_paced_programs_for_student(
        self, db: AsyncSession, student_id: int
    ) -> List[tuple]:
        """Programs the student can access via self-paced batches.

        Returns (TrainingProgram, TrainingBatch) tuples. A student may be in
        multiple self-paced batches linked to the same programme — deduplicated
        by the caller.
        """
        result = await db.execute(
            select(TrainingProgram, TrainingBatch)
            .join(TrainingBatch, TrainingBatch.program_id == TrainingProgram.id)
            .join(
                TrainingBatchStudent,
                TrainingBatchStudent.batch_id == TrainingBatch.id,
            )
            .where(
                TrainingBatchStudent.student_id == student_id,
                TrainingBatch.is_self_paced.is_(True),
                TrainingBatch.program_id.isnot(None),
            )
            .order_by(TrainingProgram.title)
        )
        return list(result.all())

    async def verify_self_paced_enrollment(
        self, db: AsyncSession, student_id: int, program_id: int
    ) -> Optional[TrainingBatch]:
        """Check that this student is in at least one self-paced batch linked to the
        given programme. Returns the batch (for its name) or None."""
        result = await db.execute(
            select(TrainingBatch)
            .join(
                TrainingBatchStudent,
                TrainingBatchStudent.batch_id == TrainingBatch.id,
            )
            .where(
                TrainingBatchStudent.student_id == student_id,
                TrainingBatch.is_self_paced.is_(True),
                TrainingBatch.program_id == program_id,
            )
            .limit(1)
        )
        return result.scalar_one_or_none()


training_batch_crud = CRUDTrainingBatch(TrainingBatch)
training_student_crud = CRUDTrainingStudent(TrainingStudent)
training_session_crud = CRUDTrainingSession(TrainingSession)
sync_state_crud = CRUDSyncState(TrainingSyncState)
student_module_progress_crud = CRUDStudentModuleProgress(StudentModuleProgress)
