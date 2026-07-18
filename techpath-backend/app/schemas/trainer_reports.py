"""Schemas for read-only trainer session reports: attendance, poll history, and the
confusion timeline. See ``app/api/v1/endpoints/trainer_reports.py`` — these are built
directly from the classroom models rather than reusing the live-session view schemas in
``app/schemas/classroom.py``, since a report looks back at history instead of describing
current state.
"""

from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel


# ---------- attendance ----------


class AttendanceRow(BaseModel):
    participant_id: int
    display_name: str
    is_guest: bool
    student_id: Optional[int] = None
    first_joined_at: datetime
    last_seen_at: datetime
    left_at: Optional[datetime] = None
    is_online: bool
    duration_minutes: float


class AttendanceReportResponse(BaseModel):
    session_id: int
    session_title: Optional[str] = None
    total_participants: int
    rows: List[AttendanceRow]


# ---------- poll history ----------


class PollHistoryEntry(BaseModel):
    id: int
    question: str
    options: List[str]
    status: str
    results: dict[int, int]
    total_votes: int
    correct_option_index: Optional[int] = None
    created_at: datetime
    closed_at: Optional[datetime] = None


class PollHistoryResponse(BaseModel):
    session_id: int
    polls: List[PollHistoryEntry]


# ---------- confusion timeline ----------


class ConfusionTimelinePoint(BaseModel):
    timestamp: datetime
    online: int
    confused: int
    ratio: float


class ConfusionTimelineResponse(BaseModel):
    session_id: int
    points: List[ConfusionTimelinePoint]


# ---------- quiz results ----------


class QuizStudentResult(BaseModel):
    """One roster student's standing on one quiz.

    Every student on the batch appears, including those who never attempted — a
    trainer's most useful signal is usually who has not engaged at all, which a
    query over attempts alone would silently omit. Those rows carry
    ``attempt_count == 0`` and null scores.
    """

    student_id: int
    name: str
    email: Optional[str] = None
    attempt_count: int
    best_score: Optional[int] = None
    total_questions: Optional[int] = None
    passed: bool
    last_attempted_at: Optional[datetime] = None
    # True when the best attempt was graded against a different question count than
    # the quiz has now. Partial by design: it catches questions being added or
    # removed, not a reworded question at the same count.
    is_stale: bool = False


class QuizQuestionStat(BaseModel):
    index: int
    question: str
    correct_count: int
    attempted_count: int


class QuizResultSummary(BaseModel):
    asset_id: int
    title: str
    total_questions: int
    pass_mark: float
    attempted_count: int
    passed_count: int
    roster_size: int
    question_stats: List[QuizQuestionStat]
    students: List[QuizStudentResult]


class QuizResultsResponse(BaseModel):
    session_id: int
    quizzes: List[QuizResultSummary]
