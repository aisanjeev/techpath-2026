"""Unauthorized-access tests for live media (FR-006/SC-004): a caller must never reach
a WHIP/WHEP/HLS URL — or any other media state — without passing this feature's own
authorization boundary, on top of (not instead of) the boundaries the classroom feature
already enforces.
"""
import pytest
from fastapi.security import HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.v1.endpoints.classroom import get_current_participant, get_state
from app.api.v1.endpoints.trainer import end_session, start_session, update_media_state
from app.core.constants import SessionStatus, UserRole
from app.core.exceptions import ForbiddenError, UnauthorizedError
from app.crud.classroom import session_participant_crud
from app.crud.training import training_module_crud, training_program_crud
from app.crud.training_roster import training_batch_crud, training_session_crud
from app.models.user import User
from app.schemas.classroom import MediaStateRequest
from app.schemas.training import TrainingModuleCreate, TrainingProgramCreate
from app.schemas.training_roster import StartSessionRequest
from app.services.classroom.identity import mint_classroom_token
from app.services.roster.mock_provider import MockRosterProvider
from app.services.roster_sync_service import RosterSyncService

TRAINER_EMAIL = "techpath.biz@gmail.com"
OTHER_TRAINER_EMAIL = "priya.trainer@techpath.biz"


def _trainer(email: str = TRAINER_EMAIL) -> User:
    user = User(email=email, name="T", role=UserRole.TRAINER.value, is_active=True)
    user.id = 1
    return user


async def _seed_two_live_sessions(db: AsyncSession):
    """Two independent live sessions (different batches), so a token minted for one
    can be tried against the other — the cross-session leak this suite guards against."""
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
    batch_a = await training_batch_crud.get_by_external_id(db, "BATCH-001")  # owned by TRAINER_EMAIL
    batch_a.program_id = program.id
    db.add(batch_a)
    batch_b = await training_batch_crud.get_by_external_id(
        db, "BATCH-003"
    )  # owned by OTHER_TRAINER_EMAIL
    batch_b.program_id = program.id
    db.add(batch_b)
    await db.flush()

    session_a = await training_session_crud.create(
        db, obj_in={"batch_id": batch_a.id, "module_id": module.id, "title": "Session A"}
    )
    session_b = await training_session_crud.create(
        db, obj_in={"batch_id": batch_b.id, "module_id": module.id, "title": "Session B"}
    )
    await start_session(
        session_a.id, StartSessionRequest(), db=db, current_user=_trainer(TRAINER_EMAIL)
    )
    await start_session(
        session_b.id, StartSessionRequest(), db=db, current_user=_trainer(OTHER_TRAINER_EMAIL)
    )
    return session_a, session_b


class TestParticipantMediaAuthorization:
    async def test_session_as_token_is_rejected_against_session_b(
        self, test_db: AsyncSession
    ) -> None:
        """The exact mechanism gating who can ever receive a whep_url/hls_url: a
        classroom token only decodes successfully against the session_id it was minted
        for (see decode_classroom_token)."""
        session_a, session_b = await _seed_two_live_sessions(test_db)
        participant_a = await session_participant_crud.join(
            test_db, session_id=session_a.id, display_name="Guest", student_id=None, is_guest=True
        )
        token_for_a = mint_classroom_token(
            session_id=session_a.id,
            participant_key=participant_a.participant_key,
            display_name="Guest",
        )
        creds = HTTPAuthorizationCredentials(scheme="Bearer", credentials=token_for_a)

        with pytest.raises(UnauthorizedError):
            await get_current_participant(session_id=session_b.id, credentials=creds, db=test_db)

    async def test_no_credentials_cannot_reach_state(self, test_db: AsyncSession) -> None:
        session_a, _ = await _seed_two_live_sessions(test_db)

        with pytest.raises(UnauthorizedError):
            await get_current_participant(session_id=session_a.id, credentials=None, db=test_db)

    async def test_kicked_participants_token_no_longer_reaches_media(
        self, test_db: AsyncSession
    ) -> None:
        """A stale-but-cryptographically-valid token from a removed participant must
        not still be able to read the session's live media state."""
        session_a, _ = await _seed_two_live_sessions(test_db)
        participant = await session_participant_crud.join(
            test_db, session_id=session_a.id, display_name="Guest", student_id=None, is_guest=True
        )
        token = mint_classroom_token(
            session_id=session_a.id,
            participant_key=participant.participant_key,
            display_name="Guest",
        )
        await session_participant_crud.kick(test_db, participant)
        creds = HTTPAuthorizationCredentials(scheme="Bearer", credentials=token)

        with pytest.raises(UnauthorizedError):
            await get_current_participant(session_id=session_a.id, credentials=creds, db=test_db)

    async def test_legitimate_participant_only_ever_sees_their_own_sessions_media(
        self, test_db: AsyncSession
    ) -> None:
        """Sanity check alongside the rejection tests above: the boundary isn't
        over-tightened — a valid participant of session A still gets session A's
        whep_url."""
        session_a, session_b = await _seed_two_live_sessions(test_db)
        participant_a = await session_participant_crud.join(
            test_db, session_id=session_a.id, display_name="Guest", student_id=None, is_guest=True
        )

        state = await get_state(session_a.id, participant_a, test_db)

        assert state.media is not None
        assert state.media.whep_url is not None
        # Never the other, unrelated session's stream.
        session_b = await training_session_crud.get(test_db, session_b.id)
        assert session_b.live_stream_path not in state.media.whep_url


class TestTrainerMediaAuthorization:
    async def test_non_owning_trainer_cannot_read_whip_url(self, test_db: AsyncSession) -> None:
        session_a, _ = await _seed_two_live_sessions(test_db)

        with pytest.raises(ForbiddenError):
            await start_session(
                session_a.id,
                StartSessionRequest(),
                db=test_db,
                current_user=_trainer(OTHER_TRAINER_EMAIL),
            )

    async def test_non_owning_trainer_cannot_change_media_state(
        self, test_db: AsyncSession
    ) -> None:
        session_a, _ = await _seed_two_live_sessions(test_db)

        with pytest.raises(ForbiddenError):
            await update_media_state(
                session_a.id,
                MediaStateRequest(mic_muted=True),
                db=test_db,
                current_user=_trainer(OTHER_TRAINER_EMAIL),
            )

    async def test_non_owning_trainer_cannot_end_a_session_or_trigger_its_recording(
        self, test_db: AsyncSession
    ) -> None:
        from fastapi import BackgroundTasks

        session_a, _ = await _seed_two_live_sessions(test_db)

        with pytest.raises(ForbiddenError):
            await end_session(
                session_a.id,
                BackgroundTasks(),
                db=test_db,
                current_user=_trainer(OTHER_TRAINER_EMAIL),
            )
        # Still live — the rejected call must not have side-effected the session.
        session_a = await training_session_crud.get(test_db, session_a.id)
        assert session_a.status == SessionStatus.LIVE.value
