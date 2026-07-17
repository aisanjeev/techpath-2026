"""Tests for the post-session student materials portal: the Firebase-account linking
gate (``get_or_link_from_firebase``) and the enrollment+publish access gate
(``get_enrolled_published`` / ``list_published_for_student``).

These two gates are the entire security boundary described in
``student_portal.py``'s module docstring — a student sees a session's materials if and
only if they are enrolled in its batch *and* it has since been published. Every test here is really
checking one of those two conditions in isolation, plus the identity-linking rules that
decide who "a student" resolves to in the first place.
"""
from datetime import datetime, timezone

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.constants import SessionStatus
from app.crud.training_roster import (
    training_batch_crud,
    training_session_crud,
    training_student_crud,
)
from app.models.training_roster import TrainingBatch, TrainingSession, TrainingStudent
from app.services.roster.mock_provider import MockRosterProvider
from app.services.roster_sync_service import RosterSyncService


KNOWN_STUDENT_EMAIL = "aarav.sharma@example.com"


async def _seed_batch_and_session(
    db: AsyncSession, external_batch_id: str = "BATCH-001"
) -> tuple[TrainingBatch, TrainingSession]:
    await RosterSyncService(provider=MockRosterProvider()).sync_all(db)
    batch = await training_batch_crud.get_by_external_id(db, external_batch_id)
    session = await training_session_crud.create(
        db, obj_in={"batch_id": batch.id, "status": SessionStatus.ENDED.value}
    )
    return batch, session


async def _known_student(db: AsyncSession) -> TrainingStudent:
    await RosterSyncService(provider=MockRosterProvider()).sync_all(db)
    student = await training_student_crud.get_by_email(db, KNOWN_STUDENT_EMAIL)
    assert student is not None, "fixture drifted: expected KNOWN_STUDENT_EMAIL in mock roster"
    return student


class TestGetOrLinkFromFirebase:
    async def test_unrecognised_email_is_rejected_not_auto_created(
        self, test_db: AsyncSession
    ) -> None:
        """The core security property: a Gmail account is proof of an email address,
        never proof of roster membership. No row may be created for a stranger."""
        await RosterSyncService(provider=MockRosterProvider()).sync_all(test_db)

        result = await training_student_crud.get_or_link_from_firebase(
            test_db, "fb-uid-stranger", "nobody@nowhere.com"
        )

        assert result is None
        # Only the mock roster's own seeded students should exist — none created here.
        no_match = await training_student_crud.get_by_email(test_db, "nobody@nowhere.com")
        assert no_match is None

    async def test_first_login_links_by_email_and_persists_uid(
        self, test_db: AsyncSession
    ) -> None:
        student = await _known_student(test_db)
        assert student.firebase_uid is None

        linked = await training_student_crud.get_or_link_from_firebase(
            test_db, "fb-uid-1", KNOWN_STUDENT_EMAIL
        )

        assert linked is not None
        assert linked.id == student.id
        assert linked.firebase_uid == "fb-uid-1"

    async def test_email_match_is_case_insensitive(self, test_db: AsyncSession) -> None:
        student = await _known_student(test_db)

        linked = await training_student_crud.get_or_link_from_firebase(
            test_db, "fb-uid-2", KNOWN_STUDENT_EMAIL.upper()
        )

        assert linked is not None
        assert linked.id == student.id

    async def test_returning_student_resolves_via_uid_fast_path(
        self, test_db: AsyncSession
    ) -> None:
        student = await _known_student(test_db)
        first = await training_student_crud.get_or_link_from_firebase(
            test_db, "fb-uid-3", KNOWN_STUDENT_EMAIL
        )
        assert first.id == student.id

        # Second login: uid alone resolves it, independent of whatever email string
        # comes along this time (Google is the source of truth for the uid->account
        # binding once linked, not a re-check against the roster email).
        second = await training_student_crud.get_or_link_from_firebase(
            test_db, "fb-uid-3", "irrelevant-on-second-login@example.com"
        )

        assert second is not None
        assert second.id == student.id

    async def test_a_different_uid_cannot_hijack_an_already_linked_email(
        self, test_db: AsyncSession
    ) -> None:
        """Security-relevant: once a roster row is claimed by one Google account, a
        second Google account asserting the same email must not silently take it over."""
        student = await _known_student(test_db)
        await training_student_crud.get_or_link_from_firebase(
            test_db, "fb-uid-original", KNOWN_STUDENT_EMAIL
        )

        result = await training_student_crud.get_or_link_from_firebase(
            test_db, "fb-uid-hijacker", KNOWN_STUDENT_EMAIL
        )

        assert result is None
        await test_db.refresh(student)
        assert student.firebase_uid == "fb-uid-original"


class TestEnrollmentPlusPublishGate:
    async def test_unenrolled_student_is_rejected_even_if_published(
        self, test_db: AsyncSession
    ) -> None:
        # Create a batch the student is not in
        not_my_batch = await training_batch_crud.create(
            test_db, obj_in={"external_id": "OTHER-BATCH", "name": "Other"}
        )
        session = await training_session_crud.create(
            test_db, obj_in={"batch_id": not_my_batch.id, "status": SessionStatus.ENDED.value}
        )
        student = await _known_student(test_db)
        session.materials_published_at = datetime.now(timezone.utc)
        test_db.add(session)
        await test_db.flush()

        result = await training_session_crud.get_enrolled_published(
            test_db, session.id, student.id
        )

        assert result is None

    async def test_enrolled_student_is_rejected_if_not_yet_published(
        self, test_db: AsyncSession
    ) -> None:
        _, session = await _seed_batch_and_session(test_db)
        student = await _known_student(test_db)
        assert session.materials_published_at is None

        result = await training_session_crud.get_enrolled_published(
            test_db, session.id, student.id
        )

        assert result is None

    async def test_enrolled_student_of_a_published_session_is_allowed(
        self, test_db: AsyncSession
    ) -> None:
        _, session = await _seed_batch_and_session(test_db)
        student = await _known_student(test_db)
        
        session.materials_published_at = datetime.now(timezone.utc)
        test_db.add(session)
        await test_db.flush()

        result = await training_session_crud.get_enrolled_published(
            test_db, session.id, student.id
        )

        assert result is not None
        assert result.id == session.id

    async def test_list_published_for_student_only_includes_enrolled_and_published(
        self, test_db: AsyncSession
    ) -> None:
        batch, enrolled_and_published = await _seed_batch_and_session(test_db)
        student = await _known_student(test_db)
        enrolled_and_published.materials_published_at = datetime.now(timezone.utc)
        test_db.add(enrolled_and_published)

        enrolled_not_published = await training_session_crud.create(
            test_db, obj_in={"batch_id": batch.id, "status": SessionStatus.ENDED.value}
        )
        test_db.add(enrolled_not_published)
        
        not_my_batch = await training_batch_crud.create(
            test_db, obj_in={"external_id": "OTHER-BATCH", "name": "Other"}
        )
        not_enrolled_but_published = await training_session_crud.create(
            test_db, obj_in={"batch_id": not_my_batch.id, "status": SessionStatus.ENDED.value}
        )
        not_enrolled_but_published.materials_published_at = datetime.now(timezone.utc)
        test_db.add(not_enrolled_but_published)
        await test_db.flush()

        results = await training_session_crud.list_published_for_student(test_db, student.id)

        assert [s.id for s in results] == [enrolled_and_published.id]
