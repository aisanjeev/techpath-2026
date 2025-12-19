"""Media file Pydantic schemas."""
from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, ConfigDict, Field


class MediaFileUsageBase(BaseModel):
    """Base schema for media file usage."""

    entity_type: str = Field(..., max_length=50)
    entity_id: int
    field_name: str = Field(..., max_length=50)


class MediaFileUsageCreate(MediaFileUsageBase):
    """Schema for creating a media file usage record."""

    pass


class MediaFileUsageResponse(MediaFileUsageBase):
    """Schema for media file usage response."""

    id: int
    file_id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class MediaFileBase(BaseModel):
    """Base schema for media file."""

    filename: str = Field(..., max_length=255)
    content_type: str = Field(..., max_length=100)
    alt_text: Optional[str] = Field(None, max_length=255)


class MediaFileCreate(MediaFileBase):
    """Schema for creating a media file record."""

    stored_path: str = Field(..., max_length=500)
    file_hash: str = Field(..., max_length=64)
    size: int
    width: Optional[int] = None
    height: Optional[int] = None


class MediaFileUpdate(BaseModel):
    """Schema for updating a media file record."""

    alt_text: Optional[str] = Field(None, max_length=255)


class MediaFileResponse(MediaFileBase):
    """Schema for media file response."""

    id: int
    stored_path: str
    file_hash: str
    size: int
    width: Optional[int] = None
    height: Optional[int] = None
    url: str = ""  # Will be populated by API
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class MediaFileDetailResponse(MediaFileResponse):
    """Schema for detailed media file response with usages."""

    usages: List[MediaFileUsageResponse] = []
    usage_count: int = 0


class MediaFileListResponse(BaseModel):
    """Schema for media file list response."""

    id: int
    filename: str
    stored_path: str
    content_type: str
    size: int
    width: Optional[int] = None
    height: Optional[int] = None
    alt_text: Optional[str] = None
    url: str = ""
    usage_count: int = 0
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class MediaUploadResponse(BaseModel):
    """Schema for upload response."""

    success: bool = True
    data: MediaFileResponse
    is_duplicate: bool = False
    message: str = "File uploaded successfully"

