"""Tests for the trainer-side live audio/video media lifecycle: stream-path minting on
start, release on end, and trainer-only exposure of the publish (WHIP) URL.
"""
import pytest
from fastapi import BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.v1.endpoints.trainer import end_session, start_session, update_media_state
from app.core.constants import UserRole
from app.core.exceptions import ForbiddenError, ValidationError
from app.crud.training import training_module_crud, training_program_crud
from app.crud.training_roster import training_batch_crud
from app.models.user import User
from app.schemas.classroom import MediaStateRequest
from app.schemas.training import TrainingModuleCreate, TrainingProgramCreate
from app.schemas.training_roster import StartSessionRequest, TrainingSessionCreate
from app.services.roster.mock_provider import MockRosterProvider
from app.services.roster_sync_service import RosterSyncService

TRAINER_EMAIL = "techpath.biz@gmail.com"
OTHER_TRAINER_EMAIL = "priya.trainer@techpath.biz"


def _user(email: str, role: str = UserRole.TRAINER.value) -> User:
    user = User(email=email, name="T", role=role, is_active=True)
    user.id = 1
    return user


async def _seed_session(db: AsyncSession):
    """A real batch/module/session via the same trainer-flow endpoint the UI uses, so
    the test exercises the actual create_session -> start_session path."""
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

    from app.crud.training_roster import training_session_crud

    session = await training_session_crud.create(
        db,
        obj_in={
            "batch_id": batch.id,
            "module_id": module.id,
            "title": "Live media test",
        },
    )
    return session


class TestStreamPathLifecycle:
    async def test_start_session_mints_stream_path_and_whip_url(
        self, test_db: AsyncSession
    ) -> None:
        session = await _seed_session(test_db)

        response = await start_session(
            session.id,
            StartSessionRequest(),
            db=test_db,
            current_user=_user(TRAINER_EMAIL),
        )

        assert response.media is not None
        assert response.media.whip_url is not None
        assert response.media.whip_url.endswith("/whip")

    async def test_restarting_a_live_session_keeps_the_same_stream_path(
        self, test_db: AsyncSession
    ) -> None:
        """A trainer's browser may already be mid-WHIP-handshake — restarting an
        already-live session must not mint a fresh path out from under it."""
        session = await _seed_session(test_db)

        first = await start_session(
            session.id, StartSessionRequest(), db=test_db, current_user=_user(TRAINER_EMAIL)
        )
        second = await start_session(
            session.id, StartSessionRequest(), db=test_db, current_user=_user(TRAINER_EMAIL)
        )

        assert first.media.whip_url == second.media.whip_url

    async def test_second_session_for_same_batch_cannot_go_live_concurrently(
        self, test_db: AsyncSession
    ) -> None:
        """FR-015: a batch must never have two simultaneous live broadcasts."""
        from app.crud.training_roster import training_session_crud as ts_crud

        first = await _seed_session(test_db)
        second = await ts_crud.create(
            test_db,
            obj_in={
                "batch_id": first.batch_id,
                "module_id": first.module_id,
                "title": "Second session",
            },
        )
        await start_session(
            first.id, StartSessionRequest(), db=test_db, current_user=_user(TRAINER_EMAIL)
        )

        with pytest.raises(ValidationError):
            await start_session(
                second.id, StartSessionRequest(), db=test_db, current_user=_user(TRAINER_EMAIL)
            )

    async def test_non_owning_trainer_cannot_start_session(self, test_db: AsyncSession) -> None:
        session = await _seed_session(test_db)

        with pytest.raises(ForbiddenError):
            await start_session(
                session.id,
                StartSessionRequest(),
                db=test_db,
                current_user=_user(OTHER_TRAINER_EMAIL),
            )

    async def test_end_session_releases_stream_path(self, test_db: AsyncSession) -> None:
        session = await _seed_session(test_db)
        await start_session(
            session.id, StartSessionRequest(), db=test_db, current_user=_user(TRAINER_EMAIL)
        )

        response = await end_session(
            session.id, BackgroundTasks(), db=test_db, current_user=_user(TRAINER_EMAIL)
        )

        assert response.media is None

    async def test_non_owning_trainer_cannot_end_session(self, test_db: AsyncSession) -> None:
        session = await _seed_session(test_db)
        await start_session(
            session.id, StartSessionRequest(), db=test_db, current_user=_user(TRAINER_EMAIL)
        )

        with pytest.raises(ForbiddenError):
            await end_session(
                session.id,
                BackgroundTasks(),
                db=test_db,
                current_user=_user(OTHER_TRAINER_EMAIL),
            )


class TestMediaState:
    async def test_partial_update_persists_and_broadcasts(self, test_db: AsyncSession) -> None:
        session = await _seed_session(test_db)
        await start_session(
            session.id, StartSessionRequest(), db=test_db, current_user=_user(TRAINER_EMAIL)
        )

        response = await update_media_state(
            session.id,
            MediaStateRequest(mic_muted=True),
            db=test_db,
            current_user=_user(TRAINER_EMAIL),
        )

        assert response.media.mic_muted is True
        # Untouched fields keep their prior (default) value — a partial update of one
        # flag must not silently reset the others.
        assert response.media.camera_off is False
        assert response.media.screen_sharing is False

    async def test_second_partial_update_does_not_clobber_the_first(
        self, test_db: AsyncSession
    ) -> None:
        session = await _seed_session(test_db)
        await start_session(
            session.id, StartSessionRequest(), db=test_db, current_user=_user(TRAINER_EMAIL)
        )
        await update_media_state(
            session.id,
            MediaStateRequest(mic_muted=True),
            db=test_db,
            current_user=_user(TRAINER_EMAIL),
        )

        response = await update_media_state(
            session.id,
            MediaStateRequest(screen_sharing=True),
            db=test_db,
            current_user=_user(TRAINER_EMAIL),
        )

        assert response.media.mic_muted is True
        assert response.media.screen_sharing is True

    async def test_rejects_non_owning_trainer(self, test_db: AsyncSession) -> None:
        session = await _seed_session(test_db)
        await start_session(
            session.id, StartSessionRequest(), db=test_db, current_user=_user(TRAINER_EMAIL)
        )

        with pytest.raises(ForbiddenError):
            await update_media_state(
                session.id,
                MediaStateRequest(mic_muted=True),
                db=test_db,
                current_user=_user(OTHER_TRAINER_EMAIL),
            )

    async def test_rejects_when_session_not_live(self, test_db: AsyncSession) -> None:
        session = await _seed_session(test_db)

        with pytest.raises(ValidationError):
            await update_media_state(
                session.id,
                MediaStateRequest(mic_muted=True),
                db=test_db,
                current_user=_user(TRAINER_EMAIL),
            )

    async def test_going_live_resets_leftover_media_state(self, test_db: AsyncSession) -> None:
        """Defends the scheduled->live transition's reset: a row that somehow already
        carries a stale mic_muted=True (e.g. state that predates a fix, or a future
        reschedule-in-place flow) must not surface as muted the moment presenting
        starts — a trainer's fresh session always begins unmuted."""
        session = await _seed_session(test_db)
        session.media_mic_muted = True
        test_db.add(session)
        await test_db.flush()

        response = await start_session(
            session.id, StartSessionRequest(), db=test_db, current_user=_user(TRAINER_EMAIL)
        )

        assert response.media.mic_muted is False
