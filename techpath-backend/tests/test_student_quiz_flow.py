"""Tests for graded quizzes: answer-key redaction, grading, and progress gating.

The redaction tests here are the regression guard for the whole feature.
``asset_to_response`` defaults to the *unredacted* trainer view because most of its
callers are the CMS and the presenter — which means a new student-facing caller that
forgets ``audience="student"`` silently reintroduces the leak. These tests assert on
the student-destined paths specifically so that mistake fails loudly.

Note "student-destined" is about where the payload *goes*, not who called. The slide
broadcast is a trainer-authenticated endpoint whose payload is pushed to every
connected student, so it is tested here alongside the genuinely student-facing ones.
"""

import json
import uuid
from datetime import datetime, timezone

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.v1.dependencies import get_current_student
from app.core.constants import AssetType, SessionStatus
from app.crud.training import asset_to_response
from app.crud.training_roster import (
    training_batch_crud,
    training_session_crud,
    training_student_crud,
)
from app.main import app
from app.models.training import LectureAsset, TrainingModule, TrainingModuleAsset, TrainingProgram
from app.models.training_roster import TrainingStudent
from app.services.roster.mock_provider import MockRosterProvider
from app.services.roster_sync_service import RosterSyncService


KNOWN_STUDENT_EMAIL = "aarav.sharma@example.com"


QUIZ_CONFIG = {
    "questions": [
        {
            "question": "What does CIDR stand for?",
            "options": ["Classless Inter-Domain Routing", "Cisco Internal Domain Route"],
            "correct_index": 0,
            "explanation": "CIDR replaced classful addressing in 1993.",
        },
        {
            "question": "Which port does HTTPS use by default?",
            "options": ["80", "443", "8080"],
            "correct_index": 1,
            "explanation": "443 is the registered port for HTTP over TLS.",
        },
    ],
    "pass_mark_percent": 70,
}


async def _quiz_asset(db: AsyncSession, config: dict = None) -> LectureAsset:
    asset = LectureAsset(
        public_id=str(uuid.uuid4()),
        title="Networking Fundamentals Check",
        asset_type=AssetType.QUIZ.value,
        config_json=json.dumps(config if config is not None else QUIZ_CONFIG),
    )
    db.add(asset)
    await db.flush()
    return asset


def _questions(response) -> list:
    assert response.config is not None
    return response.config["questions"]


class TestAnswerKeyRedaction:
    """User Story 1 — the answer key must not reach a student before they submit."""

    async def test_student_audience_strips_correct_index_and_explanation(
        self, test_db: AsyncSession
    ) -> None:
        asset = await _quiz_asset(test_db)

        response = await asset_to_response(test_db, asset, audience="student")

        for question in _questions(response):
            # Key absence, not a null value — a null still tells you the field exists,
            # and this assertion is what stops the leak from creeping back as
            # `correct_index: None`.
            assert "correct_index" not in question
            assert "explanation" not in question
            # The question itself must survive redaction, or the quiz is unusable.
            assert question["question"]
            assert len(question["options"]) >= 2

    async def test_trainer_audience_keeps_the_answer_key(self, test_db: AsyncSession) -> None:
        asset = await _quiz_asset(test_db)

        response = await asset_to_response(test_db, asset, audience="trainer")

        questions = _questions(response)
        assert questions[0]["correct_index"] == 0
        assert questions[1]["correct_index"] == 1
        assert questions[0]["explanation"].startswith("CIDR replaced")

    async def test_default_audience_is_trainer(self, test_db: AsyncSession) -> None:
        """Pins the documented default. If this ever flips, every student-facing call
        site's explicit audience="student" becomes load-bearing in the other direction
        and the CMS quietly loses its answer key."""
        asset = await _quiz_asset(test_db)

        response = await asset_to_response(test_db, asset)

        assert _questions(response)[0]["correct_index"] == 0

    async def test_redaction_does_not_mutate_the_stored_asset(self, test_db: AsyncSession) -> None:
        """Redacting for a student must not poison a later trainer read of the same
        asset — the failure this guards against would be near-impossible to trace."""
        asset = await _quiz_asset(test_db)

        await asset_to_response(test_db, asset, audience="student")
        after = await asset_to_response(test_db, asset, audience="trainer")

        assert _questions(after)[0]["correct_index"] == 0
        assert json.loads(asset.config_json)["questions"][0]["correct_index"] == 0

    async def test_non_quiz_assets_are_untouched(self, test_db: AsyncSession) -> None:
        asset = LectureAsset(
            public_id=str(uuid.uuid4()),
            title="Cheat sheet",
            asset_type=AssetType.MARKDOWN.value,
            body="# Notes",
            config_json=json.dumps({"language": "python"}),
        )
        test_db.add(asset)
        await test_db.flush()

        response = await asset_to_response(test_db, asset, audience="student")

        assert response.config == {"language": "python"}

    async def test_pass_mark_percent_survives_redaction(self, test_db: AsyncSession) -> None:
        """Only the per-question answer key is secret. The pass mark is not — the
        student is told what they need to score."""
        asset = await _quiz_asset(test_db)

        response = await asset_to_response(test_db, asset, audience="student")

        assert response.config["pass_mark_percent"] == 70

    async def test_malformed_quiz_config_does_not_crash_redaction(
        self, test_db: AsyncSession
    ) -> None:
        """A quiz whose config predates the current shape must degrade, not 500 — this
        runs on already-published material."""
        asset = await _quiz_asset(test_db, config={"questions": "not-a-list"})

        response = await asset_to_response(test_db, asset, audience="student")

        assert response.config["questions"] == "not-a-list"


# ---------------------------------------------------------------------------
# Endpoint-level fixtures: a published session whose module holds real material
# ---------------------------------------------------------------------------


async def _markdown_asset(db: AsyncSession, title: str) -> LectureAsset:
    asset = LectureAsset(
        public_id=str(uuid.uuid4()),
        title=title,
        asset_type=AssetType.MARKDOWN.value,
        body=f"# {title}",
    )
    db.add(asset)
    await db.flush()
    return asset


async def _published_session_with_material(db: AsyncSession, assets: list):
    """Roster-synced batch + student, a module holding ``assets`` in order, and a
    published session pointing at it.

    Deliberately built through the real access path — the endpoints gate on
    ``get_enrolled_published``, so a shortcut that skipped enrollment or publication
    would make these tests pass without exercising the gate at all.
    """
    await RosterSyncService(provider=MockRosterProvider()).sync_all(db)
    batch = await training_batch_crud.get_by_external_id(db, "BATCH-001")
    student = await training_student_crud.get_by_email(db, KNOWN_STUDENT_EMAIL)

    program = TrainingProgram(title="Prog", slug=f"prog-{uuid.uuid4().hex[:8]}")
    db.add(program)
    await db.flush()

    module = TrainingModule(program_id=program.id, title="Mod", slug=f"mod-{uuid.uuid4().hex[:8]}")
    db.add(module)
    await db.flush()

    for order, asset in enumerate(assets):
        db.add(TrainingModuleAsset(module_id=module.id, asset_id=asset.id, display_order=order))
    await db.flush()

    session = await training_session_crud.create(
        db,
        obj_in={
            "batch_id": batch.id,
            "module_id": module.id,
            "status": SessionStatus.ENDED.value,
            "materials_published_at": datetime.now(timezone.utc),
        },
    )
    return session, student


def _as_student(student: TrainingStudent) -> None:
    app.dependency_overrides[get_current_student] = lambda: student


@pytest.fixture(autouse=True)
def _clear_student_override():
    yield
    app.dependency_overrides.pop(get_current_student, None)


class TestQuizSubmission:
    """User Story 2 — a student can actually take the quiz and be scored."""

    async def test_submitting_returns_score_and_the_answer_key(
        self, test_db: AsyncSession, client
    ) -> None:
        quiz = await _quiz_asset(test_db)
        session, student = await _published_session_with_material(test_db, [quiz])
        _as_student(student)

        resp = await client.post(
            f"/api/v1/student/sessions/{session.id}/assets/{quiz.id}/quiz-attempts",
            json={"answers": [0, 1]},
        )

        assert resp.status_code == 201
        data = resp.json()
        assert data["score"] == 2
        assert data["total_questions"] == 2
        assert data["passed"] is True
        assert data["attempt_number"] == 1
        # Post-submission is the ONE place a student is handed the answer key.
        assert data["questions"][0]["correct_index"] == 0
        assert data["questions"][0]["explanation"].startswith("CIDR replaced")

    async def test_wrong_answers_fail_but_still_explain(
        self, test_db: AsyncSession, client
    ) -> None:
        quiz = await _quiz_asset(test_db)
        session, student = await _published_session_with_material(test_db, [quiz])
        _as_student(student)

        resp = await client.post(
            f"/api/v1/student/sessions/{session.id}/assets/{quiz.id}/quiz-attempts",
            json={"answers": [1, 0]},
        )

        data = resp.json()
        assert data["score"] == 0
        assert data["passed"] is False
        assert data["questions"][0]["is_correct"] is False
        assert data["questions"][0]["explanation"]

    async def test_retry_records_a_second_independent_attempt(
        self, test_db: AsyncSession, client
    ) -> None:
        quiz = await _quiz_asset(test_db)
        session, student = await _published_session_with_material(test_db, [quiz])
        _as_student(student)
        url = f"/api/v1/student/sessions/{session.id}/assets/{quiz.id}/quiz-attempts"

        first = await client.post(url, json={"answers": [1, 0]})
        second = await client.post(url, json={"answers": [0, 1]})

        assert first.json()["attempt_number"] == 1
        assert first.json()["passed"] is False
        assert second.json()["attempt_number"] == 2
        assert second.json()["passed"] is True

    async def test_incomplete_submission_is_rejected(self, test_db: AsyncSession, client) -> None:
        quiz = await _quiz_asset(test_db)
        session, student = await _published_session_with_material(test_db, [quiz])
        _as_student(student)

        resp = await client.post(
            f"/api/v1/student/sessions/{session.id}/assets/{quiz.id}/quiz-attempts",
            json={"answers": [0]},
        )

        assert resp.status_code == 422

    async def test_out_of_range_option_is_rejected(self, test_db: AsyncSession, client) -> None:
        quiz = await _quiz_asset(test_db)
        session, student = await _published_session_with_material(test_db, [quiz])
        _as_student(student)

        resp = await client.post(
            f"/api/v1/student/sessions/{session.id}/assets/{quiz.id}/quiz-attempts",
            json={"answers": [0, 99]},
        )

        assert resp.status_code == 422

    async def test_non_quiz_asset_is_rejected(self, test_db: AsyncSession, client) -> None:
        notes = await _markdown_asset(test_db, "Notes")
        session, student = await _published_session_with_material(test_db, [notes])
        _as_student(student)

        resp = await client.post(
            f"/api/v1/student/sessions/{session.id}/assets/{notes.id}/quiz-attempts",
            json={"answers": []},
        )

        assert resp.status_code == 422

    async def test_quiz_outside_this_session_is_not_gradeable(
        self, test_db: AsyncSession, client
    ) -> None:
        """A student must not be able to grade themselves against a quiz that isn't in
        the material they actually attended."""
        in_session = await _markdown_asset(test_db, "Notes")
        orphan_quiz = await _quiz_asset(test_db)
        session, student = await _published_session_with_material(test_db, [in_session])
        _as_student(student)

        resp = await client.post(
            f"/api/v1/student/sessions/{session.id}/assets/{orphan_quiz.id}/quiz-attempts",
            json={"answers": [0, 1]},
        )

        assert resp.status_code == 404


class TestProgressGating:
    """User Story 3 — a quiz blocks what comes after it until it is passed."""

    async def test_unpassed_quiz_locks_everything_after_it(
        self, test_db: AsyncSession, client
    ) -> None:
        intro = await _markdown_asset(test_db, "Intro")
        quiz = await _quiz_asset(test_db)
        followup = await _markdown_asset(test_db, "Follow-up")
        session, student = await _published_session_with_material(test_db, [intro, quiz, followup])
        _as_student(student)

        resp = await client.get(f"/api/v1/student/sessions/{session.id}/progress")

        data = resp.json()
        assert data["first_locked_index"] == 1
        assert data["items"][0]["locked"] is False  # intro
        assert data["items"][1]["locked"] is False  # the quiz itself stays reachable
        assert data["items"][2]["locked"] is True  # everything past it does not
        assert data["items"][1]["passed"] is False
        assert data["items"][0]["passed"] is None  # non-quiz has nothing to pass

    async def test_passing_unlocks_the_next_item(self, test_db: AsyncSession, client) -> None:
        quiz = await _quiz_asset(test_db)
        followup = await _markdown_asset(test_db, "Follow-up")
        session, student = await _published_session_with_material(test_db, [quiz, followup])
        _as_student(student)

        submit = await client.post(
            f"/api/v1/student/sessions/{session.id}/assets/{quiz.id}/quiz-attempts",
            json={"answers": [0, 1]},
        )
        assert submit.json()["unlocked_next"] is True

        after = await client.get(f"/api/v1/student/sessions/{session.id}/progress")
        data = after.json()
        assert data["first_locked_index"] == 2
        assert all(item["locked"] is False for item in data["items"])

    async def test_failing_does_not_unlock(self, test_db: AsyncSession, client) -> None:
        quiz = await _quiz_asset(test_db)
        followup = await _markdown_asset(test_db, "Follow-up")
        session, student = await _published_session_with_material(test_db, [quiz, followup])
        _as_student(student)

        submit = await client.post(
            f"/api/v1/student/sessions/{session.id}/assets/{quiz.id}/quiz-attempts",
            json={"answers": [1, 0]},
        )

        assert submit.json()["unlocked_next"] is False
        after = await client.get(f"/api/v1/student/sessions/{session.id}/progress")
        assert after.json()["items"][1]["locked"] is True

    async def test_material_without_a_quiz_is_never_gated(
        self, test_db: AsyncSession, client
    ) -> None:
        assets = [await _markdown_asset(test_db, f"Page {i}") for i in range(3)]
        session, student = await _published_session_with_material(test_db, assets)
        _as_student(student)

        resp = await client.get(f"/api/v1/student/sessions/{session.id}/progress")

        data = resp.json()
        assert data["first_locked_index"] == 3
        assert all(item["locked"] is False for item in data["items"])

    async def test_empty_quiz_never_blocks(self, test_db: AsyncSession, client) -> None:
        """A quiz with no questions has nothing to answer, so it must not become an
        unpassable wall in the middle of someone's material."""
        empty = await _quiz_asset(test_db, config={"questions": []})
        followup = await _markdown_asset(test_db, "Follow-up")
        session, student = await _published_session_with_material(test_db, [empty, followup])
        _as_student(student)

        resp = await client.get(f"/api/v1/student/sessions/{session.id}/progress")

        data = resp.json()
        assert data["first_locked_index"] == 2
        assert data["items"][1]["locked"] is False

    async def test_progress_requires_enrollment_and_publication(
        self, test_db: AsyncSession, client
    ) -> None:
        quiz = await _quiz_asset(test_db)
        session, student = await _published_session_with_material(test_db, [quiz])
        _as_student(student)

        resp = await client.get("/api/v1/student/sessions/999999/progress")

        assert resp.status_code == 404


class TestTrainerQuizResults:
    """User Story 4 — the trainer can see who passed and what the group got wrong."""

    @staticmethod
    def _as_trainer(email: str = "techpath.biz@gmail.com", role: str = "trainer"):
        from app.api.v1.dependencies import get_current_trainer_user
        from app.models.user import User

        user = User(id=1, email=email, role=role, name="T")
        app.dependency_overrides[get_current_trainer_user] = lambda: user
        return user

    @pytest.fixture(autouse=True)
    def _clear_trainer_override(self):
        yield
        from app.api.v1.dependencies import get_current_trainer_user

        app.dependency_overrides.pop(get_current_trainer_user, None)

    async def test_includes_roster_students_with_no_attempt(
        self, test_db: AsyncSession, client
    ) -> None:
        """The whole point of querying from the roster outward: a student who never
        opened the quiz is the trainer's most actionable signal, and an attempts-only
        query would drop them silently."""
        quiz = await _quiz_asset(test_db)
        session, student = await _published_session_with_material(test_db, [quiz])
        _as_student(student)
        await client.post(
            f"/api/v1/student/sessions/{session.id}/assets/{quiz.id}/quiz-attempts",
            json={"answers": [0, 1]},
        )

        self._as_trainer()
        resp = await client.get(f"/api/v1/trainer/sessions/{session.id}/quiz-results")

        assert resp.status_code == 200
        summary = resp.json()["quizzes"][0]
        assert summary["roster_size"] >= 2
        assert len(summary["students"]) == summary["roster_size"]

        attempted = [s for s in summary["students"] if s["attempt_count"] > 0]
        never = [s for s in summary["students"] if s["attempt_count"] == 0]
        assert len(attempted) == 1
        assert attempted[0]["passed"] is True
        assert never, "roster students with no attempt must still be listed"
        assert all(s["passed"] is False and s["best_score"] is None for s in never)

    async def test_best_of_multiple_attempts_is_reported(
        self, test_db: AsyncSession, client
    ) -> None:
        quiz = await _quiz_asset(test_db)
        session, student = await _published_session_with_material(test_db, [quiz])
        _as_student(student)
        url = f"/api/v1/student/sessions/{session.id}/assets/{quiz.id}/quiz-attempts"
        await client.post(url, json={"answers": [1, 0]})  # 0/2
        await client.post(url, json={"answers": [0, 1]})  # 2/2
        await client.post(url, json={"answers": [1, 0]})  # 0/2 again

        self._as_trainer()
        resp = await client.get(f"/api/v1/trainer/sessions/{session.id}/quiz-results")

        row = next(s for s in resp.json()["quizzes"][0]["students"] if s["attempt_count"] == 3)
        # Best-of, not most-recent: unlimited retries must not punish practising.
        assert row["best_score"] == 2
        assert row["passed"] is True

    async def test_question_stats_count_each_student_once(
        self, test_db: AsyncSession, client
    ) -> None:
        quiz = await _quiz_asset(test_db)
        session, student = await _published_session_with_material(test_db, [quiz])
        _as_student(student)
        url = f"/api/v1/student/sessions/{session.id}/assets/{quiz.id}/quiz-attempts"
        await client.post(url, json={"answers": [0, 1]})
        await client.post(url, json={"answers": [0, 1]})

        self._as_trainer()
        resp = await client.get(f"/api/v1/trainer/sessions/{session.id}/quiz-results")

        stats = resp.json()["quizzes"][0]["question_stats"]
        assert stats[0]["attempted_count"] == 1, "retries must not inflate the denominator"
        assert stats[0]["correct_count"] == 1

    async def test_trainer_from_another_batch_is_refused(
        self, test_db: AsyncSession, client
    ) -> None:
        quiz = await _quiz_asset(test_db)
        session, _ = await _published_session_with_material(test_db, [quiz])

        self._as_trainer(email="someone.else@techpath.biz")
        resp = await client.get(f"/api/v1/trainer/sessions/{session.id}/quiz-results")

        assert resp.status_code == 403

    async def test_admin_may_report_on_any_session(self, test_db: AsyncSession, client) -> None:
        quiz = await _quiz_asset(test_db)
        session, _ = await _published_session_with_material(test_db, [quiz])

        self._as_trainer(email="admin@techpath.biz", role="admin")
        resp = await client.get(f"/api/v1/trainer/sessions/{session.id}/quiz-results")

        assert resp.status_code == 200

    async def test_session_without_quizzes_returns_empty(
        self, test_db: AsyncSession, client
    ) -> None:
        notes = await _markdown_asset(test_db, "Notes")
        session, _ = await _published_session_with_material(test_db, [notes])

        self._as_trainer()
        resp = await client.get(f"/api/v1/trainer/sessions/{session.id}/quiz-results")

        assert resp.status_code == 200
        assert resp.json()["quizzes"] == []

    async def test_edited_quiz_marks_old_attempts_stale_without_regrading(
        self, test_db: AsyncSession, client
    ) -> None:
        """A trainer adding a question must not silently rescore or re-lock students
        who already passed."""
        quiz = await _quiz_asset(test_db)
        session, student = await _published_session_with_material(test_db, [quiz])
        _as_student(student)
        await client.post(
            f"/api/v1/student/sessions/{session.id}/assets/{quiz.id}/quiz-attempts",
            json={"answers": [0, 1]},
        )

        extended = json.loads(json.dumps(QUIZ_CONFIG))
        extended["questions"].append(
            {"question": "New Q", "options": ["a", "b"], "correct_index": 0}
        )
        quiz.config_json = json.dumps(extended)
        test_db.add(quiz)
        await test_db.flush()

        self._as_trainer()
        resp = await client.get(f"/api/v1/trainer/sessions/{session.id}/quiz-results")

        row = next(s for s in resp.json()["quizzes"][0]["students"] if s["attempt_count"] == 1)
        assert row["is_stale"] is True
        assert row["best_score"] == 2, "the original score must be preserved"
        assert row["passed"] is True, "a student who passed stays passed"
