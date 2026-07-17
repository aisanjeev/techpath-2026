"""Tests for the roster mirror and its sync.

The mock provider is the contract made executable, so these tests are also the
specification the external API has to satisfy.
"""
import json
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Optional

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.training import training_program_crud
from app.crud.training_roster import (
    sync_state_crud,
    training_batch_crud,
    training_student_crud,
)
from app.schemas.roster_external import (
    ExternalBatch,
    ExternalStudent,
    PageMeta,
    RosterPage,
)
from app.schemas.training import TrainingProgramCreate
from app.services.roster.base import RosterProvider
from app.services.roster.mock_provider import MockRosterProvider
from app.services.roster_sync_service import CURSOR_OVERLAP, RosterSyncService


class TestMockProviderFidelity:
    """A mock that lies about paging leaves the sync's paging loop untested."""

    async def test_paginates_and_reports_has_more(self) -> None:
        provider = MockRosterProvider()

        p1 = await provider.list_batches(page=1, page_size=2)
        assert len(p1.data) == 2
        assert p1.meta.has_more is True
        assert p1.meta.total == 5

        p3 = await provider.list_batches(page=3, page_size=2)
        assert len(p3.data) == 1
        assert p3.meta.has_more is False

    async def test_ordering_is_stable_across_pages(self) -> None:
        provider = MockRosterProvider()
        ids = []
        for page in (1, 2, 3):
            chunk = await provider.list_batches(page=page, page_size=2)
            ids.extend(b.id for b in chunk.data)
        assert ids == sorted(ids)
        assert len(ids) == len(set(ids)), "a record must not appear on two pages"

    async def test_updated_since_filters(self) -> None:
        provider = MockRosterProvider()
        cutoff = datetime(2026, 7, 13, tzinfo=timezone.utc)
        chunk = await provider.list_batches(updated_since=cutoff, page_size=100)
        assert {b.id for b in chunk.data} == {"BATCH-003", "BATCH-005"}

    async def test_batch_students_is_scoped(self) -> None:
        provider = MockRosterProvider()
        chunk = await provider.list_batch_students("BATCH-001", page_size=100)
        assert {s.id for s in chunk.data} == {"STU-001", "STU-002", "STU-003"}

    async def test_health(self) -> None:
        assert await MockRosterProvider().health() is True
        assert await MockRosterProvider(Path("/nonexistent")).health() is False


class TestSyncBatches:
    async def test_creates_then_updates_idempotently(self, test_db: AsyncSession) -> None:
        service = RosterSyncService(provider=MockRosterProvider())

        first = await service.sync_batches(test_db)
        assert first.ok
        assert first.created == 5
        assert first.updated == 0

        # A second run with the cursor set should not duplicate anything.
        second = await service.sync_batches(test_db)
        assert second.ok
        assert second.created == 0

        batches, total = await training_batch_crud.search(test_db, limit=100)
        assert total == 5

    async def test_maps_fields_and_keeps_raw_payload(self, test_db: AsyncSession) -> None:
        await RosterSyncService(provider=MockRosterProvider()).sync_batches(test_db)

        batch = await training_batch_crud.get_by_external_id(test_db, "BATCH-001")
        assert batch.name == "Python Fundamentals — July Morning"
        assert batch.code == "PY-2026-JUL-A"
        assert batch.trainer_email == "techpath.biz@gmail.com"
        assert batch.timezone == "Asia/Kolkata"
        assert json.loads(batch.schedule_json)["days"] == ["Mon", "Wed", "Fri"]
        # Unmodelled upstream fields survive rather than being dropped.
        assert json.loads(batch.raw_json)["id"] == "BATCH-001"
        assert batch.synced_at is not None

    async def test_sync_never_clobbers_program_id(self, test_db: AsyncSession) -> None:
        """program_id is ours. Losing it on every sync would silently unlink content."""
        service = RosterSyncService(provider=MockRosterProvider())
        await service.sync_batches(test_db)

        program = await training_program_crud.create_from_schema(
            test_db, obj_in=TrainingProgramCreate(title="Python", slug="python")
        )
        batch = await training_batch_crud.get_by_external_id(test_db, "BATCH-001")
        batch.program_id = program.id
        test_db.add(batch)
        await test_db.flush()

        # Force a full re-sync by clearing the cursor.
        state = await sync_state_crud.get_by_resource(test_db, "batches")
        state.cursor_updated_since = None
        test_db.add(state)
        await test_db.flush()

        result = await service.sync_batches(test_db)
        assert result.updated == 5

        batch = await training_batch_crud.get_by_external_id(test_db, "BATCH-001")
        assert batch.program_id == program.id, "sync overwrote operator-set linkage"

    async def test_trainer_email_is_normalised(self, test_db: AsyncSession) -> None:
        """The two systems don't share a keyboard; matching must not hinge on case."""

        class UpperEmailProvider(MockRosterProvider):
            async def list_batches(self, **kwargs):
                page = await super().list_batches(**kwargs)
                for b in page.data:
                    if b.trainer_email:
                        b.trainer_email = b.trainer_email.upper()
                return page

        await RosterSyncService(provider=UpperEmailProvider()).sync_batches(test_db)
        batch = await training_batch_crud.get_by_external_id(test_db, "BATCH-001")
        assert batch.trainer_email == "techpath.biz@gmail.com"

        found = await training_batch_crud.get_by_trainer_email(
            test_db, "TechPath.Biz@Gmail.COM"
        )
        assert len(found) == 3


class TestSyncCursor:
    async def test_cursor_uses_observed_max_not_now(self, test_db: AsyncSession) -> None:
        """Advancing to now() drops records changed during the run when the two clocks
        disagree — and it looks like the external API is lying."""
        before = datetime.now(timezone.utc)
        await RosterSyncService(provider=MockRosterProvider()).sync_batches(test_db)

        state = await sync_state_crud.get_by_resource(test_db, "batches")
        cursor = state.cursor_updated_since
        if cursor.tzinfo is None:
            cursor = cursor.replace(tzinfo=timezone.utc)

        newest_fixture = datetime(2026, 7, 15, 9, 45, tzinfo=timezone.utc)
        assert cursor == newest_fixture - CURSOR_OVERLAP
        assert cursor < before, "cursor must track their clock, not ours"

    async def test_cursor_has_an_overlap_window(self, test_db: AsyncSession) -> None:
        await RosterSyncService(provider=MockRosterProvider()).sync_batches(test_db)
        state = await sync_state_crud.get_by_resource(test_db, "batches")

        newest = datetime(2026, 7, 15, 9, 45, tzinfo=timezone.utc)
        cursor = state.cursor_updated_since
        if cursor.tzinfo is None:
            cursor = cursor.replace(tzinfo=timezone.utc)
        assert newest - cursor == CURSOR_OVERLAP

    async def test_a_record_on_the_boundary_is_not_missed(self, test_db: AsyncSession) -> None:
        """The overlap exists so a record written during the previous run is re-seen."""
        provider = MockRosterProvider()
        await RosterSyncService(provider=provider).sync_batches(test_db)

        state = await sync_state_crud.get_by_resource(test_db, "batches")
        cursor = state.cursor_updated_since
        if cursor.tzinfo is None:
            cursor = cursor.replace(tzinfo=timezone.utc)

        chunk = await provider.list_batches(updated_since=cursor, page_size=100)
        assert "BATCH-005" in {b.id for b in chunk.data}


class TestSyncFailure:
    async def test_failure_records_error_and_does_not_advance_cursor(
        self, test_db: AsyncSession
    ) -> None:
        """A partial advance would skip the unprocessed records forever."""

        class BrokenProvider(MockRosterProvider):
            async def list_batches(self, **kwargs):
                raise RuntimeError("roster API exploded")

        result = await RosterSyncService(provider=BrokenProvider()).sync_batches(test_db)

        assert not result.ok
        assert "exploded" in result.error

        state = await sync_state_crud.get_by_resource(test_db, "batches")
        assert state.last_status == "error"
        assert state.cursor_updated_since is None
        assert state.is_running is False, "the lock must be released even on failure"

    async def test_failure_does_not_raise_to_the_caller(self, test_db: AsyncSession) -> None:
        """A stale mirror is a nuisance; a 500 on the batches page is an outage."""

        class BrokenProvider(MockRosterProvider):
            async def list_students(self, **kwargs):
                raise RuntimeError("boom")

        result = await RosterSyncService(provider=BrokenProvider()).sync_students(test_db)
        assert result.error is not None

    async def test_overlapping_run_is_skipped(self, test_db: AsyncSession) -> None:
        """Two workers plus a manual Sync now button can otherwise interleave."""
        service = RosterSyncService(provider=MockRosterProvider())
        state = await sync_state_crud.get_by_resource(test_db, "batches")
        if state is None:
            await service._get_state(test_db, "batches")
            state = await sync_state_crud.get_by_resource(test_db, "batches")
        state.is_running = True
        state.run_started_at = datetime.now(timezone.utc)
        test_db.add(state)
        await test_db.flush()

        result = await service.sync_batches(test_db)
        assert result.skipped_locked is True
        assert result.processed == 0

    async def test_stale_lock_is_taken_over(self, test_db: AsyncSession) -> None:
        """A worker killed mid-sync must not wedge the lock forever."""
        service = RosterSyncService(provider=MockRosterProvider())
        await service._get_state(test_db, "batches")
        state = await sync_state_crud.get_by_resource(test_db, "batches")
        state.is_running = True
        state.run_started_at = datetime.now(timezone.utc) - timedelta(hours=2)
        test_db.add(state)
        await test_db.flush()

        result = await service.sync_batches(test_db)
        assert result.skipped_locked is False
        assert result.processed == 5


class TestSyncStudents:
    async def test_memberships_are_built(self, test_db: AsyncSession) -> None:
        service = RosterSyncService(provider=MockRosterProvider())
        await service.sync_batches(test_db)
        await service.sync_students(test_db)

        batch = await training_batch_crud.get_by_external_id(test_db, "BATCH-001")
        students = await training_batch_crud.students(test_db, batch.id)
        assert {s.external_id for s in students} == {"STU-001", "STU-002", "STU-003"}

    async def test_student_can_be_in_two_batches(self, test_db: AsyncSession) -> None:
        service = RosterSyncService(provider=MockRosterProvider())
        await service.sync_batches(test_db)
        await service.sync_students(test_db)

        student = await training_student_crud.get_by_external_id(test_db, "STU-002")
        batch_ids = await training_student_crud.batch_ids(test_db, student.id)
        assert len(batch_ids) == 2

    async def test_removal_from_a_batch_is_reflected(self, test_db: AsyncSession) -> None:
        """A student moved out must stop appearing on the old roster, or trainers mark
        attendance for people who left."""
        service = RosterSyncService(provider=MockRosterProvider())
        await service.sync_batches(test_db)
        await service.sync_students(test_db)

        batch = await training_batch_crud.get_by_external_id(test_db, "BATCH-002")
        assert len(await training_batch_crud.students(test_db, batch.id)) == 2

        class MovedProvider(MockRosterProvider):
            async def list_students(self, **kwargs):
                page = await super().list_students(**kwargs)
                for s in page.data:
                    if s.id == "STU-002":
                        s.batch_ids = ["BATCH-001"]  # dropped from BATCH-002
                return page

        state = await sync_state_crud.get_by_resource(test_db, "students")
        state.cursor_updated_since = None
        test_db.add(state)
        await test_db.flush()

        await RosterSyncService(provider=MovedProvider()).sync_students(test_db)

        remaining = await training_batch_crud.students(test_db, batch.id)
        assert {s.external_id for s in remaining} == {"STU-004"}

    async def test_student_with_no_batches_is_still_mirrored(
        self, test_db: AsyncSession
    ) -> None:
        service = RosterSyncService(provider=MockRosterProvider())
        await service.sync_batches(test_db)
        await service.sync_students(test_db)

        orphan = await training_student_crud.get_by_external_id(test_db, "STU-006")
        assert orphan is not None
        assert await training_student_crud.batch_ids(test_db, orphan.id) == []


class TestSyncAll:
    async def test_batches_are_synced_before_students(self, test_db: AsyncSession) -> None:
        """Memberships resolve batch ids, so the order is load-bearing."""
        results = await RosterSyncService(provider=MockRosterProvider()).sync_all(test_db)

        assert results["batches"]["created"] == 5
        assert results["students"]["created"] == 6

        batch = await training_batch_crud.get_by_external_id(test_db, "BATCH-003")
        assert len(await training_batch_crud.students(test_db, batch.id)) == 1
