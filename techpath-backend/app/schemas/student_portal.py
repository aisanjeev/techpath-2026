"""Schemas for the post-session student materials portal.

Separate from ``schemas/classroom.py`` on purpose: that file is the live-session,
no-account student experience (join code + short-lived token); this one is the
durable, Firebase-authenticated "come back later" experience. Different identity,
different lifetime, different access rule — keeping them apart keeps either from
growing an accidental dependency on the other's assumptions.
"""

from datetime import datetime
from typing import Any, List, Optional

from pydantic import BaseModel, ConfigDict, Field

from app.schemas.classroom import RecordingView
from app.schemas.training import LectureAssetResponse


class StudentLoginResponse(BaseModel):
    display_name: str
    email: Optional[str] = None


class StudentSessionSummary(BaseModel):
    session_id: int
    title: Optional[str] = None
    batch_name: str
    module_title: Optional[str] = None
    session_date: Optional[datetime] = None
    published_at: datetime

    model_config = ConfigDict(from_attributes=False)


class StudentSessionListResponse(BaseModel):
    sessions: List[StudentSessionSummary]


class StudentSessionMaterialsResponse(BaseModel):
    session_id: int
    title: Optional[str] = None
    batch_name: str
    module_title: Optional[str] = None
    published_at: datetime
    assets: List[LectureAssetResponse]
    # Null when the session never had live media (chat/poll-only class) — distinct from
    # RecordingView.status == 'processing', which means media happened and the replay
    # just isn't ready yet.
    recording: Optional[RecordingView] = None


# ---------------------------------------------------------------------------
# Graded quizzes
# ---------------------------------------------------------------------------


class QuizAttemptSubmission(BaseModel):
    """A student's answers for one quiz.

    Answers only — deliberately no score field. The server grades against the stored
    answer key, and a client-supplied score would be worthless even if it were sent.
    Element ``i`` is the selected option index for question ``i``; per-element range
    checking happens in the grading service, which is the only thing that knows how
    many options each question has.
    """

    answers: List[Any] = Field(
        ...,
        description="Selected option index per question, positionally aligned to the quiz.",
    )


class QuizQuestionFeedback(BaseModel):
    """Per-question result. The only path by which a student receives an answer key,
    and only for an attempt they have already submitted."""

    index: int
    your_answer: int
    correct_index: Optional[int] = None
    is_correct: bool
    explanation: Optional[str] = None


class QuizAttemptResult(BaseModel):
    attempt_id: int
    attempt_number: int
    score: int
    total_questions: int
    percentage: float
    passed: bool
    pass_mark: float
    attempted_at: datetime
    # Lets the portal reveal the next material item straight away rather than
    # refetching progress after a passing submission.
    unlocked_next: bool
    questions: List[QuizQuestionFeedback]


class StudentProgressItem(BaseModel):
    """One material item's state for one student.

    ``passed`` is null for non-quiz items — they have nothing to pass, which is
    different from a quiz that has been failed.
    """

    asset_id: int
    index: int
    is_quiz: bool
    passed: Optional[bool] = None
    locked: bool
    best_score: Optional[int] = None
    total_questions: Optional[int] = None
    attempt_count: Optional[int] = None


class StudentProgressResponse(BaseModel):
    session_id: int
    # Index of the first quiz without a passing attempt; equals len(items) when there
    # is none. The quiz *at* this index is reachable — everything after it is not.
    first_locked_index: int
    items: List[StudentProgressItem]
