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
