"""Service model for IT services."""
from typing import Optional

from sqlalchemy import Boolean, String, Text, Integer
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base, TimestampMixin


class Service(Base, TimestampMixin):
    """Service model for IT services offered."""

    __tablename__ = "services"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    slug: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    short_description: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    icon: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    image_url: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    features: Mapped[Optional[str]] = mapped_column(Text, nullable=True)  # JSON string of features
    price: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    cta_text: Mapped[str] = mapped_column(String(100), default="Learn More", nullable=False)
    cta_url: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    featured: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    display_order: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    def __repr__(self) -> str:
        return f"<Service(id={self.id}, title='{self.title}', slug='{self.slug}')>"

