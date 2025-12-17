"""Case Study model for showcasing client success stories."""
from datetime import datetime
from typing import List, Optional

from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, String, Table, Text, Column
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin


# Association table for case study tags
case_study_tags = Table(
    "case_study_tags",
    Base.metadata,
    Column("case_study_id", Integer, ForeignKey("case_studies.id", ondelete="CASCADE"), primary_key=True),
    Column("tag_id", Integer, ForeignKey("case_study_tag.id", ondelete="CASCADE"), primary_key=True),
)


class CaseStudyTag(Base):
    """Tag model for case study categorization."""

    __tablename__ = "case_study_tag"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    slug: Mapped[str] = mapped_column(String(100), unique=True, index=True, nullable=False)

    # Relationships
    case_studies: Mapped[List["CaseStudy"]] = relationship(
        "CaseStudy",
        secondary=case_study_tags,
        back_populates="tags",
    )

    def __repr__(self) -> str:
        return f"<CaseStudyTag(id={self.id}, name='{self.name}')>"


class CaseStudy(Base, TimestampMixin):
    """Case study model for client success stories."""

    __tablename__ = "case_studies"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    slug: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
    client_name: Mapped[str] = mapped_column(String(255), nullable=False)
    industry: Mapped[str] = mapped_column(String(100), nullable=False)
    excerpt: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    challenge: Mapped[str] = mapped_column(Text, nullable=False)  # The problem/challenge
    solution: Mapped[str] = mapped_column(Text, nullable=False)  # Our solution
    results: Mapped[str] = mapped_column(Text, nullable=False)  # The outcomes
    content: Mapped[Optional[str]] = mapped_column(Text, nullable=True)  # Full content/story
    featured_image: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    
    # Key statistics
    stat_value: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)  # e.g., "85%"
    stat_label: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)  # e.g., "Fraud reduction"
    
    # Additional stats (JSON string for flexibility)
    additional_stats: Mapped[Optional[str]] = mapped_column(Text, nullable=True)  # JSON string
    
    # Testimonial
    testimonial_quote: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    testimonial_author: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    testimonial_role: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    
    # Meta
    author_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True
    )
    status: Mapped[str] = mapped_column(String(50), default="draft", nullable=False)
    featured: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    published_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    meta_title: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    meta_description: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)

    # Relationships
    tags: Mapped[List[CaseStudyTag]] = relationship(
        "CaseStudyTag",
        secondary=case_study_tags,
        back_populates="case_studies",
    )

    def __repr__(self) -> str:
        return f"<CaseStudy(id={self.id}, title='{self.title}', client='{self.client_name}')>"

