"""Unit tests for quiz grading arithmetic and submission validation.

Pure functions, no DB — see ``app/services/quiz_grading.py``. The boundary cases here
are the point of the file: a plausible implementation that rounds to a percentage
before comparing passes 2/3 at a 0.7 mark, which is wrong and silent.
"""

import pytest

from app.services.quiz_grading import (
    extract_questions,
    grade,
    pass_mark_for,
    question_feedback,
    validate_answers,
)


def _questions(n: int, options_each: int = 4) -> list:
    """n questions, correct answer always option 0, so a submission of all-zeros
    scores full marks and any other index is wrong."""
    return [
        {
            "question": f"Q{i}",
            "options": [f"opt{j}" for j in range(options_each)],
            "correct_index": 0,
            "explanation": f"because {i}",
        }
        for i in range(n)
    ]


class TestGradingBoundary:
    def test_two_of_three_fails_at_seventy_percent(self) -> None:
        """0.667 < 0.7 — the case that silently passes if the implementation rounds
        to a whole percentage before comparing."""
        score, total, passed = grade(_questions(3), [0, 0, 1], pass_mark=0.7)

        assert (score, total) == (2, 3)
        assert passed is False

    def test_seven_of_ten_passes_at_seventy_percent(self) -> None:
        """Exactly on the mark must pass — the comparison is >=, not >."""
        answers = [0] * 7 + [1] * 3
        score, total, passed = grade(_questions(10), answers, pass_mark=0.7)

        assert (score, total) == (7, 10)
        assert passed is True

    def test_full_marks_passes(self) -> None:
        score, total, passed = grade(_questions(3), [0, 0, 0], pass_mark=0.7)

        assert (score, total, passed) == (3, 3, True)

    def test_zero_correct_fails(self) -> None:
        score, total, passed = grade(_questions(3), [1, 1, 1], pass_mark=0.7)

        assert (score, total, passed) == (0, 3, False)

    def test_empty_quiz_passes(self) -> None:
        """A zero-question quiz must not become an unpassable wall mid-material."""
        score, total, passed = grade([], [], pass_mark=0.7)

        assert (score, total, passed) == (0, 0, True)

    def test_pass_mark_of_zero_passes_everything(self) -> None:
        _, _, passed = grade(_questions(3), [1, 1, 1], pass_mark=0.0)

        assert passed is True

    def test_pass_mark_of_one_requires_full_marks(self) -> None:
        _, _, near_miss = grade(_questions(3), [0, 0, 1], pass_mark=1.0)
        _, _, perfect = grade(_questions(3), [0, 0, 0], pass_mark=1.0)

        assert near_miss is False
        assert perfect is True


class TestPassMark:
    def test_asset_pass_mark_percent_is_honoured_and_converted(self) -> None:
        """Stored as a percentage (0-100), compared as a fraction. Getting the unit
        conversion wrong makes every quiz either free or impossible."""
        assert pass_mark_for({"pass_mark_percent": 60}) == pytest.approx(0.6)
        assert pass_mark_for({"pass_mark_percent": 100}) == pytest.approx(1.0)
        assert pass_mark_for({"pass_mark_percent": 0}) == pytest.approx(0.0)

    def test_falls_back_to_global_setting_when_unset(self) -> None:
        from app.core.config import settings

        assert pass_mark_for({}) == pytest.approx(settings.QUIZ_PASS_MARK)
        assert pass_mark_for(None) == pytest.approx(settings.QUIZ_PASS_MARK)

    def test_out_of_range_or_wrong_type_falls_back(self) -> None:
        from app.core.config import settings

        for bad in (
            {"pass_mark_percent": 150},
            {"pass_mark_percent": -1},
            {"pass_mark_percent": "70"},
            {"pass_mark_percent": True},
        ):
            assert pass_mark_for(bad) == pytest.approx(settings.QUIZ_PASS_MARK)


class TestValidateAnswers:
    def test_accepts_a_well_formed_submission(self) -> None:
        assert validate_answers(_questions(3), [0, 1, 2]) == [0, 1, 2]

    def test_rejects_missing_answers_and_names_them(self) -> None:
        with pytest.raises(ValueError) as exc:
            validate_answers(_questions(3), [0])

        # 1-based in the message — it's shown to a student, not a developer.
        assert "2" in str(exc.value) and "3" in str(exc.value)

    def test_rejects_too_many_answers(self) -> None:
        with pytest.raises(ValueError):
            validate_answers(_questions(2), [0, 1, 2])

    def test_rejects_option_index_out_of_range(self) -> None:
        with pytest.raises(ValueError, match="not one of its"):
            validate_answers(_questions(2, options_each=3), [0, 3])

    def test_rejects_negative_option_index(self) -> None:
        with pytest.raises(ValueError):
            validate_answers(_questions(2), [0, -1])

    def test_rejects_non_integer_answer(self) -> None:
        with pytest.raises(ValueError, match="option index"):
            validate_answers(_questions(2), [0, "1"])

    def test_rejects_boolean_answer(self) -> None:
        """bool is an int subclass in Python, so True would otherwise be graded as
        option index 1 — a real answer the student never gave."""
        with pytest.raises(ValueError, match="option index"):
            validate_answers(_questions(2), [0, True])

    def test_rejects_non_list_payload(self) -> None:
        with pytest.raises(ValueError):
            validate_answers(_questions(2), {"0": 1})


class TestExtractQuestions:
    def test_returns_questions(self) -> None:
        assert len(extract_questions({"questions": _questions(2)})) == 2

    def test_missing_or_empty_config_is_an_empty_quiz(self) -> None:
        assert extract_questions(None) == []
        assert extract_questions({}) == []

    def test_malformed_questions_raises(self) -> None:
        from app.services.quiz_grading import QuizConfigError

        with pytest.raises(QuizConfigError):
            extract_questions({"questions": "not-a-list"})


class TestQuestionFeedback:
    def test_reports_correctness_and_explanation_per_question(self) -> None:
        feedback = question_feedback(_questions(2), [0, 1])

        assert feedback[0]["is_correct"] is True
        assert feedback[0]["your_answer"] == 0
        assert feedback[0]["correct_index"] == 0
        assert feedback[1]["is_correct"] is False
        assert feedback[1]["explanation"] == "because 1"
