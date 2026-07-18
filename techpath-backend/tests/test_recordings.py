"""Tests for the recorded-replay lifecycle: a SessionRecording row is created only when
a live session actually had media, the trainer can check its status, and a student only
ever sees it through the same enrolled+published gate that already guards materials.
"""
from datetime import datetime, timezone

import pytest
from fastapi import BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.v1.endpoints.student_portal import get_session_materials
from app.api.v1.endpoints.trainer import end_session, get_recording, start_session
from app.core.constants import RecordingStatus, UserRole
from app.core.exceptions import NotFoundError
from app.crud.classroom import session_recording_crud
from app.crud.training import training_module_crud, training_program_crud
from app.crud.training_roster import training_batch_crud, training_session_crud
from app.models.user import User
from app.schemas.training import TrainingModuleCreate, TrainingProgramCreate
from app.schemas.training_roster import StartSessionRequest
from app.services.roster.mock_provider import MockRosterProvider
from app.services.roster_sync_service import RosterSyncService

TRAINER_EMAIL = "techpath.biz@gmail.com"
KNOWN_STUDENT_EMAIL = "aarav.sharma@example.com"


def _trainer() -> User:
    user = User(email=TRAINER_EMAIL, name="T", role=UserRole.TRAINER.value, is_active=True)
    user.id = 1
    return user


async def _seed_session(db: AsyncSession):
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

    from app.crud.training_roster import training_student_crud

    student = await training_student_crud.get_by_email(db, KNOWN_STUDENT_EMAIL)
    assert student is not None, "fixture drifted: expected KNOWN_STUDENT_EMAIL in mock roster"

    session = await training_session_crud.create(
        db, obj_in={"batch_id": batch.id, "module_id": module.id, "title": "Recording test"}
    )
    return session, student


class TestRecordingCreatedOnEndSession:
    async def test_ending_a_session_with_media_creates_a_processing_recording(
        self, test_db: AsyncSession
    ) -> None:
        session, _ = await _seed_session(test_db)
        await start_session(
            session.id, StartSessionRequest(), db=test_db, current_user=_trainer()
        )

        await end_session(session.id, BackgroundTasks(), db=test_db, current_user=_trainer())

        recording = await session_recording_crud.get_by_session(test_db, session.id)
        assert recording is not None
        assert recording.status == RecordingStatus.PROCESSING.value
        assert recording.watch_url is not None

    async def test_ending_a_session_that_never_went_live_creates_no_recording(
        self, test_db: AsyncSession
    ) -> None:
        """A chat/poll-only class (never published live media) has nothing to
        transcode — no row should appear."""
        session, _ = await _seed_session(test_db)
        # Never started, so live_stream_path is None — exercises end_session's
        # "no media happened" branch directly.

        await end_session(session.id, BackgroundTasks(), db=test_db, current_user=_trainer())

        recording = await session_recording_crud.get_by_session(test_db, session.id)
        assert recording is None


class TestTrainerRecordingEndpoint:
    async def test_returns_404_when_no_recording_exists(self, test_db: AsyncSession) -> None:
        session, _ = await _seed_session(test_db)

        with pytest.raises(NotFoundError):
            await get_recording(session.id, db=test_db, current_user=_trainer())

    async def test_returns_status_once_a_recording_exists(self, test_db: AsyncSession) -> None:
        session, _ = await _seed_session(test_db)
        await start_session(
            session.id, StartSessionRequest(), db=test_db, current_user=_trainer()
        )
        await end_session(session.id, BackgroundTasks(), db=test_db, current_user=_trainer())

        view = await get_recording(session.id, db=test_db, current_user=_trainer())

        assert view.status == RecordingStatus.PROCESSING.value


class TestStudentRecordingVisibility:
    async def test_recording_hidden_until_materials_published(
        self, test_db: AsyncSession
    ) -> None:
        session, student = await _seed_session(test_db)
        await start_session(
            session.id, StartSessionRequest(), db=test_db, current_user=_trainer()
        )
        await end_session(session.id, BackgroundTasks(), db=test_db, current_user=_trainer())
        # Recording exists, but materials were never published — same enrolled+published
        # gate as every other student_portal.py route must still apply.

        with pytest.raises(NotFoundError):
            await get_session_materials(session.id, student=student, db=test_db)

    async def test_recording_visible_once_published(self, test_db: AsyncSession) -> None:
        session, student = await _seed_session(test_db)
        await start_session(
            session.id, StartSessionRequest(), db=test_db, current_user=_trainer()
        )
        await end_session(session.id, BackgroundTasks(), db=test_db, current_user=_trainer())
        session.materials_published_at = datetime.now(timezone.utc)
        test_db.add(session)
        await test_db.flush()

        materials = await get_session_materials(session.id, student=student, db=test_db)

        assert materials.recording is not None
        assert materials.recording.status == RecordingStatus.PROCESSING.value

    async def test_recording_is_none_when_session_never_had_media(
        self, test_db: AsyncSession
    ) -> None:
        session, student = await _seed_session(test_db)
        session.status = "ended"
        session.materials_published_at = datetime.now(timezone.utc)
        test_db.add(session)
        await test_db.flush()

        materials = await get_session_materials(session.id, student=student, db=test_db)

        assert materials.recording is None
