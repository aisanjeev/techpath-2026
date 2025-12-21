"""Contact and newsletter Pydantic schemas."""
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class ContactInquiryBase(BaseModel):
    """Base contact inquiry schema."""

    name: str = Field(..., min_length=1, max_length=255)
    email: EmailStr
    message: str = Field(..., min_length=10, max_length=5000)


class ContactInquiryCreate(ContactInquiryBase):
    """Schema for creating a contact inquiry."""

    phone: Optional[str] = Field(None, max_length=50)
    company: Optional[str] = Field(None, max_length=255)
    subject: Optional[str] = Field(None, max_length=255)
    service_interest: Optional[str] = Field(None, max_length=255)


class ContactInquiryUpdate(BaseModel):
    """Schema for updating a contact inquiry (admin)."""

    status: Optional[str] = Field(None, pattern="^(new|in_progress|resolved|closed)$")
    notes: Optional[str] = None


class ContactInquiryResponse(ContactInquiryBase):
    """Schema for contact inquiry response."""

    id: int
    phone: Optional[str] = None
    company: Optional[str] = None
    subject: Optional[str] = None
    service_interest: Optional[str] = None
    status: str
    notes: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class NewsletterBase(BaseModel):
    """Base newsletter schema."""

    email: EmailStr


class NewsletterCreate(NewsletterBase):
    """Schema for newsletter subscription."""

    name: Optional[str] = Field(None, max_length=255)
    source: Optional[str] = Field(None, max_length=100)


class NewsletterResponse(NewsletterBase):
    """Schema for newsletter subscription response."""

    id: int
    name: Optional[str] = None
    is_active: bool
    source: Optional[str] = None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

