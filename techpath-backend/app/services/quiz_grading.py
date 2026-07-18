"""Server-side grading for quiz lecture assets.

Pure functions over an already-loaded asset config — no DB access, no I/O — so the
arithmetic that decides whether a student passes is trivially testable and can't be
influenced by anything the client sent. The endpoint layer persists the result; this
module only decides what the result is.

The one rule worth stating outright: a submitted score is never trusted. The request
carries selected option indices and nothing else, and the correct answers are read
here from the stored asset.
"""

from typing import Any, Dict, List, Optional, Tuple

from app.core.config import settings


class QuizConfigError(ValueError):
    """The asset's stored config isn't a usable quiz (malformed or missing questions)."""


def extract_questions(config: Optional[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Pull the question list out of an asset's config blob.

    Returns an empty list for a quiz with no questions — that's a valid, if pointless,
    quiz and it grades as passed (see ``grade``), which is what keeps an empty quiz
    from silently blocking a student's progress.
    """
    if not config:
        return []
    questions = config.get("questions")
    if questions is None:
        return []
    if not isinstance(questions, list):
        raise QuizConfigError("Quiz config 'questions' is not a list")
    return questions


def pass_mark_for(config: Optional[Dict[str, Any]]) -> float:
    """The fraction of questions needed to pass this particular quiz.

    Quiz assets authored through the CMS carry their own ``pass_mark_percent`` (an
    integer 0-100, see ``QuizAssetIn``), so an author who set one gets it honoured.
    ``settings.QUIZ_PASS_MARK`` (a fraction) is the fallback for quizzes authored
    before that field existed or with it left unset.

    Note the unit change: the stored field is a percentage, the setting and the return
    value are fractions. Mixing the two would make every quiz either trivially passable
    or impossible, so the conversion happens here, once.
    """
    if config:
        raw = config.get("pass_mark_percent")
        if isinstance(raw, (int, float)) and not isinstance(raw, bool):
            if 0 <= raw <= 100:
                return float(raw) / 100.0
    return float(settings.QUIZ_PASS_MARK)


def validate_answers(questions: List[Dict[str, Any]], answers: Any) -> List[int]:
    """Check a submission against the quiz's shape before anything is graded or stored.

    Raises ``ValueError`` with a message the endpoint turns into a ValidationError.
    """
    if not isinstance(answers, list):
        raise ValueError("Answers must be a list of selected option indices")

    if len(answers) != len(questions):
        missing = [i for i in range(len(questions)) if i >= len(answers)]
        if missing:
            shown = ", ".join(str(i + 1) for i in missing)
            raise ValueError(f"Answer every question before submitting — missing: {shown}")
        raise ValueError(f"Expected {len(questions)} answers, got {len(answers)}")

    cleaned: List[int] = []
    for i, (answer, question) in enumerate(zip(answers, questions)):
        # bool is an int subclass in Python; True would otherwise sail through as
        # option index 1 and be graded as a real answer.
        if not isinstance(answer, int) or isinstance(answer, bool):
            raise ValueError(f"Answer for question {i + 1} must be an option index")
        options = question.get("options") or []
        if answer < 0 or answer >= len(options):
            raise ValueError(
                f"Answer for question {i + 1} is not one of its {len(options)} options"
            )
        cleaned.append(answer)
    return cleaned


def grade(
    questions: List[Dict[str, Any]], answers: List[int], pass_mark: float
) -> Tuple[int, int, bool]:
    """Score a validated submission. Returns ``(score, total, passed)``.

    ``passed`` compares the raw fraction ``score / total`` against ``pass_mark``. It is
    deliberately not computed from a rounded percentage: on a 3-question quiz at a 0.7
    mark, 2 correct is 0.667 and must fail, but rounding to 67% and then comparing —
    or worse, rounding up — is how that silently becomes a pass.

    A zero-question quiz passes. That is what stops an empty quiz from being an
    unpassable wall in the middle of a student's material.
    """
    total = len(questions)
    if total == 0:
        return 0, 0, True

    score = sum(
        1 for question, answer in zip(questions, answers) if question.get("correct_index") == answer
    )
    return score, total, (score / total) >= pass_mark


def question_feedback(questions: List[Dict[str, Any]], answers: List[int]) -> List[Dict[str, Any]]:
    """Per-question result for the submitting student.

    This is the only path by which ``correct_index`` and ``explanation`` reach a
    student, and only for an attempt they have already submitted — everywhere else
    they're stripped (see ``asset_to_response``).
    """
    feedback: List[Dict[str, Any]] = []
    for i, (question, answer) in enumerate(zip(questions, answers)):
        correct_index = question.get("correct_index")
        feedback.append(
            {
                "index": i,
                "your_answer": answer,
                "correct_index": correct_index,
                "is_correct": correct_index == answer,
                "explanation": question.get("explanation"),
            }
        )
    return feedback
