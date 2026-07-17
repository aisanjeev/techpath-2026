"""DTOs for the external roster API.

These mirror the published contract in ``docs/ROSTER_API.md``. They use
``extra="allow"`` deliberately: the external system will grow fields we haven't modelled,
and an unknown key should end up preserved in ``raw_json`` rather than raising and
stopping the sync.
"""
from datetime import date, datetime
from typing import Generic, List, Optional, TypeVar

from pydantic import BaseModel, ConfigDict, Field

T = TypeVar("T")


class ExternalBatch(BaseModel):
    model_config = ConfigDict(extra="allow")

    id: str
    name: str
    code: Optional[str] = None
    status: Optional[str] = None
    mode: Optional[str] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    schedule: Optional[dict] = None
    trainer_id: Optional[str] = None
    trainer_name: Optional[str] = None
    # The mapping key to a TechPath login.
    trainer_email: Optional[str] = None
    course_ref: Optional[str] = None
    student_count: int = 0
    location: Optional[str] = None
    updated_at: Optional[datetime] = None


class ExternalStudent(BaseModel):
    model_config = ConfigDict(extra="allow")

    id: str
    name: str
    email: Optional[str] = None
    phone: Optional[str] = None
    roll_no: Optional[str] = None
    status: Optional[str] = None
    enrolled_on: Optional[date] = None
    photo_url: Optional[str] = None
    batch_ids: List[str] = Field(default_factory=list)
    updated_at: Optional[datetime] = None


class ExternalTrainer(BaseModel):
    model_config = ConfigDict(extra="allow")

    id: str
    name: str
    email: str
    phone: Optional[str] = None
    status: Optional[str] = None
    expertise: List[str] = Field(default_factory=list)
    updated_at: Optional[datetime] = None


class PageMeta(BaseModel):
    model_config = ConfigDict(extra="allow")

    page: int = 1
    page_size: int = 0
    total: int = 0
    has_more: bool = False


class RosterPage(BaseModel, Generic[T]):
    """One page of a list response: ``{data: [...], meta: {...}}``."""

    data: List[T]
    meta: PageMeta
