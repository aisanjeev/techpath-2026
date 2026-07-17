"""Tests for the live classroom participant lifecycle: joining, roster-email
matching, presence (touch/mark_offline), and confusion state.
"""
import uuid
from datetime import datetime, timezone

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.constants import SessionStatus
from app.crud.classroom import session_participant_crud
from app.crud.training_roster import training_batch_crud, training_session_crud
from app.models.training_roster import TrainingBatch, TrainingSession
from app.services.roster.mock_provider import MockRosterProvider
from app.services.roster_sync_service import RosterSyncService


def _as_aware(value: datetime) -> datetime:
    """SQLite has no tz-aware datetime storage, so a value that has round-tripped
    through ``db.refresh()`` (as ``join()`` does) comes back naive even though the app
    always writes UTC-aware values — normalize before comparing so the test isn't
    tripped up by a SQLite-only quirk. Same idiom as ``_aware()`` in
    app/services/roster_sync_service.py and ``_as_aware()`` in
    app/services/roster/mock_provider.py."""
    return value if value.tzinfo is not None else value.replace(tzinfo=timezone.utc)


async def _seed_batch_and_session(
    db: AsyncSession, external_batch_id: str = "BATCH-001"
) -> tuple[TrainingBatch, TrainingSession]:
    """Real mirrored roster data via the same sync path production uses, rather than
    hand-built rows — same pattern as test_trainer_flow.py's ``_seed`` helper."""
    await RosterSyncService(provider=MockRosterProvider()).sync_all(db)
    batch = await training_batch_crud.get_by_external_id(db, external_batch_id)
    session = await training_session_crud.create(
        db, obj_in={"batch_id": batch.id, "status": SessionStatus.LIVE.value}
    )
    return batch, session


class TestJoin:
    async def test_join_creates_participant_with_expected_fields(
        self, test_db: AsyncSession
    ) -> None:
        _, session = await _seed_batch_and_session(test_db)

        participant = await session_participant_crud.join(
            test_db,
            session_id=session.id,
            display_name="Aarav Sharma",
            student_id=None,
            is_guest=False,
        )

        assert participant.session_id == session.id
        assert participant.display_name == "Aarav Sharma"
        assert participant.is_guest is False
        assert participant.student_id is None
        # participant_key is a fresh UUID4 string, as CRUDSessionParticipant.join mints.
        assert uuid.UUID(participant.participant_key).version == 4
        assert participant.first_joined_at == participant.last_seen_at
        assert participant.is_online is True

    async def test_join_mints_a_fresh_key_on_every_call(self, test_db: AsyncSession) -> None:
        """A rejoin (new tab, cleared storage) is a new attendance entry, not merged
        into an old one — see the docstring on ``CRUDSessionParticipant.join``."""
        _, session = await _seed_batch_and_session(test_db)

        first = await session_participant_crud.join(
            test_db, session_id=session.id, display_name="Guest", student_id=None, is_guest=True
        )
        second = await session_participant_crud.join(
            test_db, session_id=session.id, display_name="Guest", student_id=None, is_guest=True
        )

        assert first.id != second.id
        assert first.participant_key != second.participant_key


class TestFindStudentInBatch:
    async def test_matches_email_of_student_enrolled_in_that_batch(
        self, test_db: AsyncSession
    ) -> None:
        batch, _ = await _seed_batch_and_session(test_db, "BATCH-001")

        student = await session_participant_crud.find_student_in_batch(
            test_db, batch.id, "aarav.sharma@example.com"
        )

        assert student is not None
        assert student.name == "Aarav Sharma"

    async def test_email_is_not_found_when_searched_against_a_different_batch(
        self, test_db: AsyncSession
    ) -> None:
        """Security-relevant: a roster-email match must be scoped to the batch the
        session belongs to. aarav.sharma@example.com is enrolled in BATCH-001 only
        (per the roster fixtures), so a lookup scoped to BATCH-002 must not find them —
        otherwise anyone with any roster email could talk their way into any batch."""
        await RosterSyncService(provider=MockRosterProvider()).sync_all(test_db)
        other_batch = await training_batch_crud.get_by_external_id(test_db, "BATCH-002")

        student = await session_participant_crud.find_student_in_batch(
            test_db, other_batch.id, "aarav.sharma@example.com"
        )

        assert student is None

    async def test_match_is_case_insensitive(self, test_db: AsyncSession) -> None:
        batch, _ = await _seed_batch_and_session(test_db, "BATCH-001")

        student = await session_participant_crud.find_student_in_batch(
            test_db, batch.id, "AARAV.SHARMA@EXAMPLE.COM"
        )

        assert student is not None
        assert student.name == "Aarav Sharma"


class TestPresence:
    async def test_touch_updates_last_seen_marks_online_and_clears_left_at(
        self, test_db: AsyncSession
    ) -> None:
        _, session = await _seed_batch_and_session(test_db)
        participant = await session_participant_crud.join(
            test_db, session_id=session.id, display_name="Guest", student_id=None, is_guest=True
        )
        await session_participant_crud.mark_offline(test_db, participant)
        assert participant.is_online is False
        assert participant.left_at is not None
        stale_last_seen = _as_aware(participant.last_seen_at)

        updated = await session_participant_crud.touch(test_db, participant)

        assert updated.is_online is True
        assert updated.left_at is None
        assert _as_aware(updated.last_seen_at) >= stale_last_seen

    async def test_mark_offline_sets_left_at_and_flips_online_false(
        self, test_db: AsyncSession
    ) -> None:
        _, session = await _seed_batch_and_session(test_db)
        participant = await session_participant_crud.join(
            test_db, session_id=session.id, display_name="Guest", student_id=None, is_guest=True
        )
        assert participant.is_online is True
        assert participant.left_at is None

        await session_participant_crud.mark_offline(test_db, participant)

        assert participant.is_online is False
        assert participant.left_at is not None


class TestConfusion:
    async def test_set_confusion_updates_flag_and_timestamp(self, test_db: AsyncSession) -> None:
        _, session = await _seed_batch_and_session(test_db)
        participant = await session_participant_crud.join(
            test_db, session_id=session.id, display_name="Guest", student_id=None, is_guest=True
        )
        assert participant.is_confused is False
        assert participant.confused_updated_at is None

        updated = await session_participant_crud.set_confusion(test_db, participant, True)

        assert updated.is_confused is True
        assert updated.confused_updated_at is not None

    async def test_confusion_summary_counts_online_and_confused_correctly(
        self, test_db: AsyncSession
    ) -> None:
        _, session = await _seed_batch_and_session(test_db)

        online_confused = await session_participant_crud.join(
            test_db, session_id=session.id, display_name="A", student_id=None, is_guest=True
        )
        await session_participant_crud.join(
            test_db, session_id=session.id, display_name="B", student_id=None, is_guest=True
        )
        offline_participant = await session_participant_crud.join(
            test_db, session_id=session.id, display_name="C", student_id=None, is_guest=True
        )
        await session_participant_crud.mark_offline(test_db, offline_participant)
        await session_participant_crud.set_confusion(test_db, online_confused, True)

        summary = await session_participant_crud.confusion_summary(test_db, session.id)

        assert summary["online"] == 2
        assert summary["confused"] == 1
        assert summary["ratio"] == pytest.approx(0.5)
