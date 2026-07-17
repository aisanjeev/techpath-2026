"""Incremental sync from the external roster API into the local mirror.

Three things here are load-bearing and easy to get subtly wrong:

1. ``program_id`` on a batch is ours, not theirs. The sync must never overwrite it, or
   an admin's content linkage silently evaporates on the next run.
2. The cursor advances to the newest ``updated_at`` we actually *saw*, minus a small
   overlap — never to ``now()``. Our clock and theirs are not the same clock, and any
   skew silently drops records that changed during the window. It then looks like their
   API is lying.
3. A sync failure must never propagate into a page load. The mirror going stale is a
   nuisance; the batches page 500ing is an outage.
"""
import json
import logging
from datetime import datetime, timedelta, timezone
from typing import Any, Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.training_roster import (
    TrainingBatch,
    TrainingBatchStudent,
    TrainingStudent,
    TrainingSyncState,
)
from app.services.roster.base import RosterProvider
from app.services.roster.factory import get_roster_provider

logger = logging.getLogger(__name__)

# Re-fetch a little before the high-water mark to absorb clock skew between us and the
# external system. Cheap: upserts are idempotent, so overlap costs a few redundant rows.
CURSOR_OVERLAP = timedelta(minutes=1)

# A run that claims to still be going after this is assumed dead (worker restarted
# mid-sync) and the lock is taken anyway.
STALE_LOCK_AFTER = timedelta(minutes=15)

MAX_PAGES = 1000  # circuit breaker: a has_more that never goes false must not hang us


class SyncResult:
    def __init__(self, resource: str) -> None:
        self.resource = resource
        self.processed = 0
        self.created = 0
        self.updated = 0
        self.skipped_locked = False
        self.error: Optional[str] = None

    @property
    def ok(self) -> bool:
        return self.error is None and not self.skipped_locked

    def as_dict(self) -> dict:
        return {
            "resource": self.resource,
            "processed": self.processed,
            "created": self.created,
            "updated": self.updated,
            "skipped_locked": self.skipped_locked,
            "error": self.error,
        }


def _aware(value: Optional[datetime]) -> Optional[datetime]:
    if value is None:
        return None
    return value.replace(tzinfo=timezone.utc) if value.tzinfo is None else value


class RosterSyncService:
    def __init__(self, provider: Optional[RosterProvider] = None, page_size: int = 100) -> None:
        self._provider = provider or get_roster_provider()
        self._page_size = page_size

    # ---------- sync state ----------

    async def _get_state(self, db: AsyncSession, resource: str) -> TrainingSyncState:
        result = await db.execute(
            select(TrainingSyncState).where(TrainingSyncState.resource == resource)
        )
        state = result.scalar_one_or_none()
        if state is None:
            state = TrainingSyncState(resource=resource)
            db.add(state)
            await db.flush()
        return state

    async def _acquire(self, db: AsyncSession, state: TrainingSyncState) -> bool:
        now = datetime.now(timezone.utc)
        started = _aware(state.run_started_at)
        if state.is_running and started and now - started < STALE_LOCK_AFTER:
            return False
        state.is_running = True
        state.run_started_at = now
        state.last_run_at = now
        db.add(state)
        await db.flush()
        return True

    async def _release(
        self,
        db: AsyncSession,
        state: TrainingSyncState,
        result: SyncResult,
        cursor: Optional[datetime],
    ) -> None:
        state.is_running = False
        state.run_started_at = None
        state.records_processed = result.processed
        if result.error:
            state.last_status = "error"
            state.last_error = result.error[:2000]
            # Deliberately do not advance the cursor on failure: a partial advance would
            # mean the records we never processed are skipped forever.
        else:
            state.last_status = "success"
            state.last_error = None
            state.last_success_at = datetime.now(timezone.utc)
            if cursor is not None:
                state.cursor_updated_since = cursor - CURSOR_OVERLAP
        db.add(state)
        await db.flush()

    # ---------- batches ----------

    async def sync_batches(self, db: AsyncSession) -> SyncResult:
        result = SyncResult("batches")
        state = await self._get_state(db, "batches")

        if not await self._acquire(db, state):
            result.skipped_locked = True
            logger.info("Batch sync already running; skipping")
            return result

        newest: Optional[datetime] = None
        try:
            since = _aware(state.cursor_updated_since)
            page = 1
            while page <= MAX_PAGES:
                chunk = await self._provider.list_batches(
                    updated_since=since, page=page, page_size=self._page_size
                )
                for row in chunk.data:
                    created = await self._upsert_batch(db, row)
                    result.processed += 1
                    result.created += int(created)
                    result.updated += int(not created)
                    ts = _aware(row.updated_at)
                    if ts and (newest is None or ts > newest):
                        newest = ts
                if not chunk.meta.has_more:
                    break
                page += 1
            await self._release(db, state, result, newest)
        except Exception as exc:  # noqa: BLE001 — the mirror must degrade, not crash
            logger.exception("Batch sync failed")
            result.error = str(exc)
            await self._release(db, state, result, None)
        return result

    async def _upsert_batch(self, db: AsyncSession, row: Any) -> bool:
        existing = (
            await db.execute(
                select(TrainingBatch).where(TrainingBatch.external_id == str(row.id))
            )
        ).scalar_one_or_none()

        schedule = json.dumps(row.schedule) if row.schedule else None
        fields = {
            "name": row.name,
            "code": row.code,
            "status": row.status,
            "mode": row.mode,
            "start_date": row.start_date,
            "end_date": row.end_date,
            "timezone": (row.schedule or {}).get("timezone") if row.schedule else None,
            "schedule_json": schedule,
            "trainer_email": (row.trainer_email or "").lower() or None,
            "trainer_external_id": row.trainer_id,
            "trainer_name": row.trainer_name,
            "student_count": row.student_count,
            "course_ref": row.course_ref,
            "location": row.location,
            "raw_json": row.model_dump_json(),
            "external_updated_at": _aware(row.updated_at),
            "synced_at": datetime.now(timezone.utc),
        }

        if existing is None:
            db.add(TrainingBatch(external_id=str(row.id), **fields))
            await db.flush()
            return True

        # program_id is intentionally absent from `fields` — it is operator-set.
        # trainer_email is also preserved when the external API sends null but we
        # already have an admin-assigned value.
        for key, value in fields.items():
            if key == "trainer_email" and value is None and existing.trainer_email:
                continue
            setattr(existing, key, value)
        db.add(existing)
        await db.flush()
        return False

    # ---------- students ----------

    async def sync_students(self, db: AsyncSession) -> SyncResult:
        result = SyncResult("students")
        state = await self._get_state(db, "students")

        if not await self._acquire(db, state):
            result.skipped_locked = True
            logger.info("Student sync already running; skipping")
            return result

        newest: Optional[datetime] = None
        try:
            since = _aware(state.cursor_updated_since)
            page = 1
            while page <= MAX_PAGES:
                chunk = await self._provider.list_students(
                    updated_since=since, page=page, page_size=self._page_size
                )
                for row in chunk.data:
                    created = await self._upsert_student(db, row)
                    result.processed += 1
                    result.created += int(created)
                    result.updated += int(not created)
                    ts = _aware(row.updated_at)
                    if ts and (newest is None or ts > newest):
                        newest = ts
                if not chunk.meta.has_more:
                    break
                page += 1
            await self._release(db, state, result, newest)
        except Exception as exc:  # noqa: BLE001
            logger.exception("Student sync failed")
            result.error = str(exc)
            await self._release(db, state, result, None)
        return result

    async def _upsert_student(self, db: AsyncSession, row: Any) -> bool:
        existing = (
            await db.execute(
                select(TrainingStudent).where(TrainingStudent.external_id == str(row.id))
            )
        ).scalar_one_or_none()

        fields = {
            "name": row.name,
            "email": (row.email or "").lower() or None,
            "phone": row.phone,
            "roll_no": row.roll_no,
            "status": row.status,
            "photo_url": row.photo_url,
            "enrolled_on": row.enrolled_on,
            "raw_json": row.model_dump_json(),
            "external_updated_at": _aware(row.updated_at),
            "synced_at": datetime.now(timezone.utc),
        }

        if existing is None:
            student = TrainingStudent(external_id=str(row.id), **fields)
            db.add(student)
            await db.flush()
            created = True
        else:
            for key, value in fields.items():
                setattr(existing, key, value)
            db.add(existing)
            await db.flush()
            student = existing
            created = False

        await self._sync_memberships(db, student, row.batch_ids or [])
        return created

    async def _sync_memberships(
        self, db: AsyncSession, student: TrainingStudent, batch_external_ids: list
    ) -> None:
        """Make local membership match the upstream ``batch_ids`` exactly.

        Removals matter as much as additions: a student moved out of a batch must stop
        appearing on its roster, or trainers mark attendance for people who left.
        """
        wanted_batches = (
            await db.execute(
                select(TrainingBatch).where(
                    TrainingBatch.external_id.in_([str(b) for b in batch_external_ids])
                )
            )
        ).scalars().all()
        wanted_ids = {b.id for b in wanted_batches}

        current = (
            await db.execute(
                select(TrainingBatchStudent).where(
                    TrainingBatchStudent.student_id == student.id
                )
            )
        ).scalars().all()
        current_ids = {m.batch_id for m in current}

        for membership in current:
            if membership.batch_id not in wanted_ids:
                await db.delete(membership)

        for batch_id in wanted_ids - current_ids:
            db.add(
                TrainingBatchStudent(
                    batch_id=batch_id,
                    student_id=student.id,
                    membership_status=student.status,
                    enrolled_at=datetime.now(timezone.utc),
                )
            )
        await db.flush()

    # ---------- orchestration ----------

    async def sync_all(self, db: AsyncSession) -> dict:
        """Batches first: students reference batches when building memberships."""
        batches = await self.sync_batches(db)
        students = await self.sync_students(db)
        return {"batches": batches.as_dict(), "students": students.as_dict()}
