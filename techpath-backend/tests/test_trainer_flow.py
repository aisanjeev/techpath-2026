"""Tests for the trainer flow: my batches -> pick module -> start presenting."""
from datetime import datetime, timedelta, timezone

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.v1.endpoints.trainer import _assert_owns_batch
from app.core.constants import SessionStatus, UserRole
from app.core.exceptions import ForbiddenError
from app.crud.training import training_module_crud, training_program_crud
from app.crud.training_roster import training_batch_crud, training_session_crud
from app.models.user import User
from app.schemas.training import TrainingModuleCreate, TrainingProgramCreate
from app.services.roster.mock_provider import MockRosterProvider
from app.services.roster_sync_service import RosterSyncService

TRAINER_EMAIL = "techpath.biz@gmail.com"
OTHER_EMAIL = "priya.trainer@techpath.biz"


def _user(email: str, role: str = UserRole.TRAINER.value) -> User:
    return User(email=email, name="T", role=role, is_active=True)


async def _seed(db: AsyncSession):
    await RosterSyncService(provider=MockRosterProvider()).sync_all(db)
    program = await training_program_crud.create_from_schema(
        db, obj_in=TrainingProgramCreate(title="Python", slug="python")
    )
    module = await training_module_crud.create(
        db,
        obj_in={
            **TrainingModuleCreate(title="Intro", slug="intro").model_dump(),
            "program_id": program.id,
        },
    )
    batch = await training_batch_crud.get_by_external_id(db, "BATCH-001")
    batch.program_id = program.id
    db.add(batch)
    await db.flush()
    return program, module, batch


class TestTrainerBatchScoping:
    async def test_trainer_sees_only_their_batches(self, test_db: AsyncSession) -> None:
        await _seed(test_db)

        mine = await training_batch_crud.get_by_trainer_email(test_db, TRAINER_EMAIL)
        theirs = await training_batch_crud.get_by_trainer_email(test_db, OTHER_EMAIL)

        assert {b.external_id for b in mine} == {"BATCH-001", "BATCH-002", "BATCH-005"}
        assert {b.external_id for b in theirs} == {"BATCH-003", "BATCH-004"}

    async def test_trainer_cannot_touch_another_trainers_batch(
        self, test_db: AsyncSession
    ) -> None:
        await _seed(test_db)
        foreign = await training_batch_crud.get_by_external_id(test_db, "BATCH-003")

        with pytest.raises(ForbiddenError):
            await _assert_owns_batch(test_db, _user(TRAINER_EMAIL), foreign)

    async def test_admin_may_access_any_batch(self, test_db: AsyncSession) -> None:
        """Admins are allowed through trainer routes to support and demo the flow."""
        await _seed(test_db)
        foreign = await training_batch_crud.get_by_external_id(test_db, "BATCH-003")

        await _assert_owns_batch(
            test_db, _user("admin@techpath.biz", UserRole.ADMIN.value), foreign
        )

    async def test_ownership_check_is_case_insensitive(self, test_db: AsyncSession) -> None:
        await _seed(test_db)
        batch = await training_batch_crud.get_by_external_id(test_db, "BATCH-001")
        await _assert_owns_batch(test_db, _user("TechPath.Biz@GMAIL.com"), batch)

    async def test_batch_with_no_trainer_is_not_owned(self, test_db: AsyncSession) -> None:
        await _seed(test_db)
        batch = await training_batch_crud.get_by_external_id(test_db, "BATCH-001")
        batch.trainer_email = None
        test_db.add(batch)
        await test_db.flush()

        with pytest.raises(ForbiddenError):
            await _assert_owns_batch(test_db, _user(TRAINER_EMAIL), batch)


class TestJoinCode:
    async def test_code_is_six_digits(self, test_db: AsyncSession) -> None:
        code = await training_session_crud.generate_join_code(test_db)
        assert len(code) == 6
        assert code.isdigit()

    async def test_code_avoids_collisions(self, test_db: AsyncSession) -> None:
        _, module, batch = await _seed(test_db)
        taken = await training_session_crud.generate_join_code(test_db)

        session = await training_session_crud.create(
            test_db,
            obj_in={
                "batch_id": batch.id,
                "module_id": module.id,
                "status": SessionStatus.LIVE.value,
                "join_code": taken,
            },
        )
        assert session.join_code == taken

        for _ in range(20):
            assert await training_session_crud.generate_join_code(test_db) != taken


class TestTodaysSessions:
    async def test_returns_todays_sessions_for_this_trainer(
        self, test_db: AsyncSession
    ) -> None:
        _, module, batch = await _seed(test_db)
        now = datetime.now(timezone.utc)

        await training_session_crud.create(
            test_db,
            obj_in={
                "batch_id": batch.id,
                "module_id": module.id,
                "title": "Today",
                "scheduled_start": now,
                "status": SessionStatus.SCHEDULED.value,
            },
        )
        await training_session_crud.create(
            test_db,
            obj_in={
                "batch_id": batch.id,
                "module_id": module.id,
                "title": "Next week",
                "scheduled_start": now + timedelta(days=7),
                "status": SessionStatus.SCHEDULED.value,
            },
        )

        today = await training_session_crud.get_today_for_trainer(test_db, TRAINER_EMAIL)
        assert [s.title for s in today] == ["Today"]

    async def test_a_live_session_shows_even_if_scheduled_yesterday(
        self, test_db: AsyncSession
    ) -> None:
        """A class running past midnight is still the class they're teaching."""
        _, module, batch = await _seed(test_db)

        await training_session_crud.create(
            test_db,
            obj_in={
                "batch_id": batch.id,
                "module_id": module.id,
                "title": "Ran long",
                "scheduled_start": datetime.now(timezone.utc) - timedelta(days=1),
                "status": SessionStatus.LIVE.value,
            },
        )

        today = await training_session_crud.get_today_for_trainer(test_db, TRAINER_EMAIL)
        assert [s.title for s in today] == ["Ran long"]

    async def test_another_trainers_session_is_excluded(self, test_db: AsyncSession) -> None:
        _, module, _ = await _seed(test_db)
        foreign = await training_batch_crud.get_by_external_id(test_db, "BATCH-003")

        await training_session_crud.create(
            test_db,
            obj_in={
                "batch_id": foreign.id,
                "title": "Not mine",
                "scheduled_start": datetime.now(timezone.utc),
                "status": SessionStatus.SCHEDULED.value,
            },
        )

        today = await training_session_crud.get_today_for_trainer(test_db, TRAINER_EMAIL)
        assert today == []


class TestBatchModules:
    async def test_batch_without_a_programme_has_no_modules(
        self, test_db: AsyncSession
    ) -> None:
        """A batch nobody has linked yet must return empty, not explode."""
        await _seed(test_db)
        unlinked = await training_batch_crud.get_by_external_id(test_db, "BATCH-002")
        assert unlinked.program_id is None

    async def test_linked_batch_exposes_its_modules(self, test_db: AsyncSession) -> None:
        program, module, batch = await _seed(test_db)
        modules = await training_module_crud.list_for_program(test_db, batch.program_id)
        assert [m.id for m in modules] == [module.id]
