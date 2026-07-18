"""User-related Pydantic schemas."""
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class UserBase(BaseModel):
    """Base user schema."""

    email: EmailStr
    name: str = Field(..., min_length=1, max_length=255)


class UserCreate(UserBase):
    """Schema for creating a user."""

    password: str = Field(..., min_length=8, max_length=100)
    role: str = Field(default="user", pattern="^(admin|trainer|user)$")


class UserUpdate(BaseModel):
    """Schema for updating a user."""

    email: Optional[EmailStr] = None
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    password: Optional[str] = Field(None, min_length=8, max_length=100)
    role: Optional[str] = Field(None, pattern="^(admin|trainer|user)$")
    is_active: Optional[bool] = None
    avatar_url: Optional[str] = None


class UserProvision(BaseModel):
    """Create a user with an optional Firebase account in one step.

    If ``password`` is provided, the backend creates the Firebase account automatically
    so the admin doesn't need to visit the Firebase console at all. Without a password,
    only the local record is created (legacy two-step flow).
    """

    email: EmailStr
    name: str = Field(..., min_length=1, max_length=255)
    role: str = Field(default="trainer", pattern="^(admin|trainer|user)$")
    password: Optional[str] = Field(None, min_length=6, max_length=100)
    is_active: bool = True


class UserAdminUpdate(BaseModel):
    """Fields an admin may change on another user."""

    name: Optional[str] = Field(None, min_length=1, max_length=255)
    role: Optional[str] = Field(None, pattern="^(admin|trainer|user)$")
    is_active: Optional[bool] = None


class UserResponse(UserBase):
    """Schema for user response."""

    id: int
    role: str
    is_active: bool
    avatar_url: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class UserAdminResponse(UserResponse):
    """Admin view. ``has_signed_in`` is derived from firebase_uid being linked, which
    tells an admin whether a provisioned row has been claimed yet."""

    has_signed_in: bool = False


class UserLogin(BaseModel):
    """Schema for user login."""

    email: EmailStr
    password: str


class Token(BaseModel):
    """Schema for JWT token response."""

    access_token: str
    token_type: str = "bearer"
    expires_in: int  # seconds


class TokenData(BaseModel):
    """Schema for token payload data."""

    sub: str  # user email
    role: str
    exp: datetime

