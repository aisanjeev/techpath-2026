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
    pricing_plans: Mapped[Optional[str]] = mapped_column(Text, nullable=True)  # JSON array of plan objects
    price: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    cta_text: Mapped[str] = mapped_column(String(100), default="Learn More", nullable=False)
    cta_url: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    featured: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    display_order: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    
    # SEO fields
    meta_title: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    meta_description: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    og_image: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    canonical_url: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    no_index: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    
    # FAQs (JSON string)
    faqs: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    # Bento layout (homepage)
    layout_size: Mapped[str] = mapped_column(String(20), default="small", nullable=False)
    badge_label: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    tags: Mapped[Optional[str]] = mapped_column(Text, nullable=True)  # JSON array string
    stat_label: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    stat_value: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    accent_color: Mapped[str] = mapped_column(String(20), default="blue", nullable=False)
    graphic_variant: Mapped[str] = mapped_column(String(20), default="none", nullable=False)

    def __repr__(self) -> str:
        return f"<Service(id={self.id}, title='{self.title}', slug='{self.slug}')>"

