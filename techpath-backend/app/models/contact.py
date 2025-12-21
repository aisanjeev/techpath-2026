"""Contact and newsletter models."""
from typing import Optional

from sqlalchemy import Boolean, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base, TimestampMixin


class ContactInquiry(Base, TimestampMixin):
    """Contact inquiry model for form submissions."""

    __tablename__ = "contact_inquiries"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    email: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    phone: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    company: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    subject: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    message: Mapped[str] = mapped_column(Text, nullable=False)
    service_interest: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    status: Mapped[str] = mapped_column(String(50), default="new", nullable=False, index=True)
    notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)  # Admin notes
    ip_address: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    user_agent: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)

    def __repr__(self) -> str:
        return f"<ContactInquiry(id={self.id}, email='{self.email}', status='{self.status}')>"


class NewsletterSubscriber(Base, TimestampMixin):
    """Newsletter subscriber model."""

    __tablename__ = "newsletter_subscribers"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
    name: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    source: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)  # e.g., "footer", "popup"
    ip_address: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)

    def __repr__(self) -> str:
        return f"<NewsletterSubscriber(id={self.id}, email='{self.email}', is_active={self.is_active})>"

