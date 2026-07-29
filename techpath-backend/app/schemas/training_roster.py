"""Schemas for the roster mirror, sessions and sync status."""
from datetime import date, datetime
from typing import List, Optional

from pydantic import BaseModel, ConfigDict, Field

from app.schemas.classroom import MediaView


class BatchProgramSummary(BaseModel):
    id: int
    title: str
    summary: Optional[str] = None
    level: Optional[str] = None
    module_count: int = 0
    asset_count: int = 0
    model_config = ConfigDict(from_attributes=True)


class TrainingBatchResponse(BaseModel):
    id: int
    external_id: str
    name: str
    code: Optional[str] = None
    programs: List[BatchProgramSummary] = Field(default_factory=list)
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    timezone: Optional[str] = None
    schedule: Optional[dict] = None
    status: Optional[str] = None
    mode: Optional[str] = None
    location: Optional[str] = None
    trainer_email: Optional[str] = None
    trainer_name: Optional[str] = None
    is_self_paced: bool = False
    student_count: int = 0
    course_ref: Optional[str] = None
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
    program_ids: List[int] = Field(
        default_factory=list, description="List of Training programme IDs to teach for this batch; empty to unlink all"
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


class ToggleRecordingRequest(BaseModel):
    keep_recording: bool


class ToggleQuestionsPublicRequest(BaseModel):
    questions_are_public: bool


class TrainingSessionQuestionCreate(BaseModel):
    question_text: str = Field(..., max_length=500, min_length=1)


class TrainingSessionQuestionResponse(BaseModel):
    id: int
    session_id: int
    student_id: int
    student_name: Optional[str] = None
    question_text: str
    is_answered: bool
    upvotes: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
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
    keep_recording: bool = False
    questions_are_public: bool = True
    materials_published_at: Optional[datetime] = None
    # Trainer-facing view: whip_url populated only while live. See MediaView docstring.
    media: Optional[MediaView] = None

    model_config = ConfigDict(from_attributes=True)


class AssetReleaseItem(BaseModel):
    """One asset's release status within a session, for the materials status endpoint."""

    asset_id: int
    asset_title: str
    asset_type: str
    is_released: bool
    released_at: Optional[datetime] = None
    released_by_user_id: Optional[int] = None
    display_order: int


class SessionMaterialsStatusResponse(BaseModel):
    session_id: int
    assets: List[AssetReleaseItem] = Field(default_factory=list)

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
    programs: List[BatchProgramSummary] = Field(default_factory=list)
    module_count: int = 0
    asset_count: int = 0
    completed_module_count: int = 0

    model_config = ConfigDict(from_attributes=True)
