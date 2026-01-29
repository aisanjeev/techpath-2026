"""Pilot signup Pydantic schemas."""
from datetime import datetime
from typing import Literal, Optional

from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator

from app.utils.validators import validate_phone


class PilotSignupBase(BaseModel):
    """Base pilot signup schema."""

    name: str = Field(..., min_length=2, max_length=100)
    email: EmailStr
    phone: str = Field(..., min_length=10, max_length=15)
    business_name: str = Field(..., min_length=2, max_length=100, alias="businessName")
    industry: Literal["travel", "gym", "retail", "realestate", "education", "healthcare", "other"]
    message: Optional[str] = Field(None, max_length=500)

    @field_validator("name", "business_name")
    @classmethod
    def validate_name_format(cls, v: str) -> str:
        """Validate name contains only letters, spaces, and hyphens."""
        import re
        if not re.match(r"^[a-zA-Z\s\-]+$", v):
            raise ValueError("Must contain only letters, spaces, and hyphens")
        return v.strip()

    @field_validator("phone")
    @classmethod
    def validate_phone_format(cls, v: str) -> str:
        """Validate phone number format."""
        if not validate_phone(v):
            raise ValueError("Invalid phone number format")
        return v


class PilotSignupCreate(PilotSignupBase):
    """Schema for creating a pilot signup."""

    model_config = ConfigDict(populate_by_name=True)


class PilotSignupUpdate(BaseModel):
    """Schema for updating a pilot signup (admin)."""

    status: Optional[str] = Field(None, pattern="^(new|contacted|qualified|rejected)$")
    notes: Optional[str] = None


class PilotSignupResponse(BaseModel):
    """Schema for pilot signup response."""

    id: int
    name: str
    email: str
    phone: str
    business_name: str
    industry: str
    message: Optional[str] = None
    status: str
    notes: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class PilotSignupSubmitResponse(BaseModel):
    """Schema for pilot signup submission response."""

    success: bool = True
    message: str
    data: dict

    model_config = ConfigDict(from_attributes=True)
