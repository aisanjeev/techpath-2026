"""Tests for the participant-facing side of live audio/video: GET /classroom/{id}/state
exposes whep_url/hls_url (never whip_url) only while the session is live and has a
stream path, matching contracts/live-media-api.md.
"""
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.v1.endpoints.classroom import get_state
from app.core.constants import SessionStatus
from app.crud.classroom import session_participant_crud
from app.crud.training_roster import training_batch_crud, training_session_crud
from app.services.roster.mock_provider import MockRosterProvider
from app.services.roster_sync_service import RosterSyncService


async def _seed_batch_and_session(db: AsyncSession, **session_fields):
    await RosterSyncService(provider=MockRosterProvider()).sync_all(db)
    batch = await training_batch_crud.get_by_external_id(db, "BATCH-001")
    session = await training_session_crud.create(
        db, obj_in={"batch_id": batch.id, "status": SessionStatus.LIVE.value, **session_fields}
    )
    return batch, session


async def _join(db: AsyncSession, session_id: int):
    return await session_participant_crud.join(
        db, session_id=session_id, display_name="Guest", student_id=None, is_guest=True
    )


class TestParticipantMediaView:
    async def test_media_present_for_live_session_with_stream_path(
        self, test_db: AsyncSession
    ) -> None:
        _, session = await _seed_batch_and_session(test_db, live_stream_path="class-1-abc123")
        participant = await _join(test_db, session.id)

        state = await get_state(session.id, participant, test_db)

        assert state.media is not None
        assert state.media.whep_url is not None
        assert state.media.whep_url.endswith("/whep")
        assert state.media.hls_url is not None
        assert state.media.hls_url.endswith("/index.m3u8")

    async def test_media_view_never_exposes_a_whip_url(self, test_db: AsyncSession) -> None:
        """The participant surface must never carry the publish URL — only the trainer
        response (built by a different function, _trainer_media_view) can."""
        _, session = await _seed_batch_and_session(test_db, live_stream_path="class-1-abc123")
        participant = await _join(test_db, session.id)

        state = await get_state(session.id, participant, test_db)

        assert state.media.whip_url is None

    async def test_media_absent_when_no_stream_path(self, test_db: AsyncSession) -> None:
        """A chat/poll-only class (trainer never started media) must not surface a
        media block at all."""
        _, session = await _seed_batch_and_session(test_db)
        participant = await _join(test_db, session.id)

        state = await get_state(session.id, participant, test_db)

        assert state.media is None

    async def test_media_reflects_trainer_mic_state(self, test_db: AsyncSession) -> None:
        _, session = await _seed_batch_and_session(
            test_db, live_stream_path="class-1-abc123", media_mic_muted=True
        )
        participant = await _join(test_db, session.id)

        state = await get_state(session.id, participant, test_db)

        assert state.media.mic_muted is True

    async def test_media_absent_when_session_not_live(self, test_db: AsyncSession) -> None:
        _, session = await _seed_batch_and_session(
            test_db, status=SessionStatus.ENDED.value, live_stream_path="class-1-abc123"
        )
        participant = await _join(test_db, session.id)

        state = await get_state(session.id, participant, test_db)

        assert state.media is None
