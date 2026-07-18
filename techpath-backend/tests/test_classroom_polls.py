"""Tests for live classroom polls: open-poll lookup, vote casting (upsert semantics),
and vote tallying.
"""
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.constants import PollStatus, SessionStatus
from app.crud.classroom import (
    session_participant_crud,
    session_poll_crud,
    session_poll_vote_crud,
)
from app.crud.training_roster import training_batch_crud, training_session_crud
from app.models.classroom import SessionParticipant, SessionPoll
from app.models.training_roster import TrainingSession
from app.services.roster.mock_provider import MockRosterProvider
from app.services.roster_sync_service import RosterSyncService


async def _seed_session(db: AsyncSession) -> TrainingSession:
    await RosterSyncService(provider=MockRosterProvider()).sync_all(db)
    batch = await training_batch_crud.get_by_external_id(db, "BATCH-001")
    return await training_session_crud.create(
        db, obj_in={"batch_id": batch.id, "status": SessionStatus.LIVE.value}
    )


async def _participant(
    db: AsyncSession, session_id: int, name: str = "Guest"
) -> SessionParticipant:
    return await session_participant_crud.join(
        db, session_id=session_id, display_name=name, student_id=None, is_guest=True
    )


async def _poll(
    db: AsyncSession, session_id: int, status: str = PollStatus.OPEN.value
) -> SessionPoll:
    return await session_poll_crud.create(
        db,
        obj_in={
            "session_id": session_id,
            "question": "Any questions?",
            "options_json": '["Yes", "No"]',
            "status": status,
        },
    )


class TestGetOpenPoll:
    async def test_returns_none_when_no_polls_exist(self, test_db: AsyncSession) -> None:
        session = await _seed_session(test_db)
        assert await session_poll_crud.get_open_poll(test_db, session.id) is None

    async def test_returns_none_when_only_closed_polls_exist(
        self, test_db: AsyncSession
    ) -> None:
        session = await _seed_session(test_db)
        await _poll(test_db, session.id, status=PollStatus.CLOSED.value)

        assert await session_poll_crud.get_open_poll(test_db, session.id) is None

    async def test_returns_the_most_recently_created_open_poll(
        self, test_db: AsyncSession
    ) -> None:
        session = await _seed_session(test_db)
        await _poll(test_db, session.id)
        newest = await _poll(test_db, session.id)

        result = await session_poll_crud.get_open_poll(test_db, session.id)
        assert result is not None
        assert result.id == newest.id


class TestCastVote:
    async def test_first_vote_creates_a_row(self, test_db: AsyncSession) -> None:
        session = await _seed_session(test_db)
        poll = await _poll(test_db, session.id)
        participant = await _participant(test_db, session.id)

        vote = await session_poll_vote_crud.cast(
            test_db, poll_id=poll.id, participant_id=participant.id, option_index=0
        )
        assert vote.option_index == 0

        fetched = await session_poll_vote_crud.get_for_participant(
            test_db, poll.id, participant.id
        )
        assert fetched is not None
        assert fetched.id == vote.id

    async def test_second_vote_updates_rather_than_duplicates(
        self, test_db: AsyncSession
    ) -> None:
        session = await _seed_session(test_db)
        poll = await _poll(test_db, session.id)
        participant = await _participant(test_db, session.id)

        first = await session_poll_vote_crud.cast(
            test_db, poll_id=poll.id, participant_id=participant.id, option_index=0
        )
        second = await session_poll_vote_crud.cast(
            test_db, poll_id=poll.id, participant_id=participant.id, option_index=1
        )

        assert second.id == first.id
        assert second.option_index == 1

        tally = await session_poll_crud.tally(test_db, poll.id)
        assert sum(tally.values()) == 1, "changing an answer must not create a second row"


class TestTally:
    async def test_tally_counts_votes_per_option(self, test_db: AsyncSession) -> None:
        session = await _seed_session(test_db)
        poll = await _poll(test_db, session.id)
        p1 = await _participant(test_db, session.id, "A")
        p2 = await _participant(test_db, session.id, "B")
        p3 = await _participant(test_db, session.id, "C")

        await session_poll_vote_crud.cast(
            test_db, poll_id=poll.id, participant_id=p1.id, option_index=0
        )
        await session_poll_vote_crud.cast(
            test_db, poll_id=poll.id, participant_id=p2.id, option_index=0
        )
        await session_poll_vote_crud.cast(
            test_db, poll_id=poll.id, participant_id=p3.id, option_index=1
        )

        tally = await session_poll_crud.tally(test_db, poll.id)
        assert tally == {0: 2, 1: 1}

    async def test_option_with_no_votes_is_absent_not_zero(self, test_db: AsyncSession) -> None:
        session = await _seed_session(test_db)
        poll = await _poll(test_db, session.id)
        participant = await _participant(test_db, session.id)

        await session_poll_vote_crud.cast(
            test_db, poll_id=poll.id, participant_id=participant.id, option_index=0
        )

        tally = await session_poll_crud.tally(test_db, poll.id)
        assert tally == {0: 1}
        assert 1 not in tally
