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


class SpamProtectionMixin(BaseModel):
    """Anti-spam fields accepted on public form submissions, never persisted.

    `website` is a honeypot — the frontend renders it visually hidden, so any
    non-empty value means a bot. Strip both fields before handing the payload
    to CRUD (see SPAM_PROTECTION_FIELDS).
    """

    turnstile_token: Optional[str] = Field(None, max_length=4096)
    website: Optional[str] = Field(None, max_length=1024)


SPAM_PROTECTION_FIELDS = {"turnstile_token", "website"}


class ContactInquirySubmit(ContactInquiryCreate, SpamProtectionMixin):
    """Public contact form payload: inquiry fields + anti-spam fields."""


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


class NewsletterSubscribe(NewsletterCreate, SpamProtectionMixin):
    """Public newsletter form payload: subscription fields + anti-spam fields."""


class NewsletterResponse(NewsletterBase):
    """Schema for newsletter subscription response."""

    id: int
    name: Optional[str] = None
    is_active: bool
    source: Optional[str] = None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
