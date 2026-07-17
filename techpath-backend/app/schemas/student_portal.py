"""Schemas for the post-session student materials portal.

Separate from ``schemas/classroom.py`` on purpose: that file is the live-session,
no-account student experience (join code + short-lived token); this one is the
durable, Firebase-authenticated "come back later" experience. Different identity,
different lifetime, different access rule — keeping them apart keeps either from
growing an accidental dependency on the other's assumptions.
"""
from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, ConfigDict

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
