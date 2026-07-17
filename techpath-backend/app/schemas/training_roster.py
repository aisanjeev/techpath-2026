"""Schemas for the roster mirror, sessions and sync status."""
from datetime import date, datetime
from typing import List, Optional

from pydantic import BaseModel, ConfigDict, Field


class TrainingBatchResponse(BaseModel):
    id: int
    external_id: str
    name: str
    code: Optional[str] = None
    program_id: Optional[int] = None
    program_title: Optional[str] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    timezone: Optional[str] = None
    schedule: Optional[dict] = None
    status: Optional[str] = None
    mode: Optional[str] = None
    location: Optional[str] = None
    trainer_email: Optional[str] = None
    trainer_name: Optional[str] = None
    student_count: int = 0
    course_ref: Optional[str] = None
    # Surfaced so operators can see how fresh the mirror is rather than trusting it.
    synced_at: Optional[datetime] = None
    external_updated_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)


class TrainingStudentResponse(BaseModel):
    id: int
    external_id: str
    name: str
    email: Optional[str] = None
    phone: Optional[str] = None
    roll_no: Optional[str] = None
    status: Optional[str] = None
    photo_url: Optional[str] = None
    enrolled_on: Optional[date] = None
    synced_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)


class LinkProgramRequest(BaseModel):
    program_id: Optional[int] = Field(
        None, description="Training programme to teach for this batch; null to unlink"
    )


class AssignTrainerRequest(BaseModel):
    trainer_email: Optional[str] = Field(
        None,
        max_length=255,
        description="Trainer email to assign; null to unassign",
    )


class SyncStateResponse(BaseModel):
    resource: str
    cursor_updated_since: Optional[datetime] = None
    last_run_at: Optional[datetime] = None
    last_success_at: Optional[datetime] = None
    last_status: Optional[str] = None
    last_error: Optional[str] = None
    records_processed: int = 0
    is_running: bool = False

    model_config = ConfigDict(from_attributes=True)


class SyncStatusResponse(BaseModel):
    provider: str
    healthy: bool
    resources: List[SyncStateResponse] = []


class SyncRunResponse(BaseModel):
    success: bool = True
    results: dict


# ---------- sessions ----------


class TrainingSessionCreate(BaseModel):
    batch_id: int = Field(..., gt=0)
    module_id: Optional[int] = None
    title: Optional[str] = Field(None, max_length=255)
    scheduled_start: Optional[datetime] = None
    scheduled_end: Optional[datetime] = None


class TrainingSessionUpdate(BaseModel):
    module_id: Optional[int] = None
    title: Optional[str] = Field(None, max_length=255)
    scheduled_start: Optional[datetime] = None
    scheduled_end: Optional[datetime] = None
    status: Optional[str] = None


class TrainingSessionResponse(BaseModel):
    id: int
    batch_id: int
    batch_name: Optional[str] = None
    module_id: Optional[int] = None
    module_title: Optional[str] = None
    title: Optional[str] = None
    scheduled_start: Optional[datetime] = None
    scheduled_end: Optional[datetime] = None
    status: str
    join_code: Optional[str] = None
    started_at: Optional[datetime] = None
    ended_at: Optional[datetime] = None
    materials_published_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)


class StartSessionRequest(BaseModel):
    module_id: Optional[int] = Field(
        None, description="Module to present; defaults to the one already on the session"
    )


class TrainerBatchSummary(BaseModel):
    """A trainer's view of one of their batches."""

    id: int
    external_id: str
    name: str
    code: Optional[str] = None
    status: Optional[str] = None
    mode: Optional[str] = None
    location: Optional[str] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    student_count: int = 0
    program_id: Optional[int] = None
    program_title: Optional[str] = None
    module_count: int = 0

    model_config = ConfigDict(from_attributes=True)
