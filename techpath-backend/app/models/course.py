"""
Course models for TechPath training platform.
Includes Course, CourseCategory, and CourseEnrollment models.
"""

from datetime import datetime
from typing import List, Optional

from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    Float,
    ForeignKey,
    Integer,
    String,
    Table,
    Text,
)
from sqlalchemy.dialects.postgresql import ARRAY, JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin


# Association table for many-to-many relationship between courses and skills/tags
course_skills = Table(
    "course_skills",
    Base.metadata,
    Column("course_id", Integer, ForeignKey("courses.id", ondelete="CASCADE"), primary_key=True),
    Column("skill_id", Integer, ForeignKey("skills.id", ondelete="CASCADE"), primary_key=True),
)


class Skill(Base):
    """Skill/Tag model for courses."""

    __tablename__ = "skills"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    slug: Mapped[str] = mapped_column(String(100), unique=True, index=True, nullable=False)

    # Relationship to courses
    courses: Mapped[List["Course"]] = relationship(
        "Course",
        secondary=course_skills,
        back_populates="skills",
    )

    def __repr__(self) -> str:
        return f"<Skill(id={self.id}, name='{self.name}')>"


class CourseCategory(Base, TimestampMixin):
    """Course category model with hierarchical support."""

    __tablename__ = "course_categories"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    slug: Mapped[str] = mapped_column(String(100), unique=True, index=True, nullable=False)
    description: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    icon: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)  # Icon name or URL
    parent_id: Mapped[Optional[int]] = mapped_column(
        Integer, ForeignKey("course_categories.id", ondelete="SET NULL"), nullable=True
    )
    display_order: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    # Self-referential relationships
    parent: Mapped[Optional["CourseCategory"]] = relationship(
        "CourseCategory", remote_side=[id], back_populates="children"
    )
    children: Mapped[List["CourseCategory"]] = relationship(
        "CourseCategory", back_populates="parent", cascade="all, delete-orphan"
    )

    # Courses in this category
    courses: Mapped[List["Course"]] = relationship(
        "Course", back_populates="category", cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"<CourseCategory(id={self.id}, name='{self.name}')>"


class Course(Base, TimestampMixin):
    """Main course model with comprehensive training course information."""

    __tablename__ = "courses"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    
    # Basic Info
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    slug: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
    short_description: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    
    # Category
    category_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("course_categories.id", ondelete="RESTRICT"), nullable=False
    )
    
    # Pricing
    price: Mapped[float] = mapped_column(Float, nullable=False)
    original_price: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    emi_available: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    emi_amount: Mapped[Optional[float]] = mapped_column(Float, nullable=True)  # Monthly EMI
    currency: Mapped[str] = mapped_column(String(3), default="INR", nullable=False)
    
    # Course Details
    duration: Mapped[str] = mapped_column(String(50), nullable=False)  # e.g., "4 months", "8 weeks"
    duration_hours: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)  # Total hours
    batch_size: Mapped[int] = mapped_column(Integer, default=20, nullable=False)
    level: Mapped[str] = mapped_column(String(20), default="beginner", nullable=False)  # beginner, intermediate, advanced
    
    # Stats & Ratings
    rating: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    review_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    enrollment_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    placement_rate: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)  # Percentage
    
    # Media
    featured_image: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    video_url: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)  # Intro video
    
    # Instructor
    instructor_name: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    instructor_title: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    instructor_bio: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    instructor_image: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    
    # Curriculum (stored as JSON)
    # Format: [{"title": "Module 1", "topics": ["Topic 1", "Topic 2"], "duration": "2 weeks"}]
    curriculum: Mapped[Optional[str]] = mapped_column(Text, nullable=True)  # JSON string
    
    # Learning Outcomes (stored as JSON array)
    learning_outcomes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)  # JSON string
    
    # Prerequisites (stored as JSON array)
    prerequisites: Mapped[Optional[str]] = mapped_column(Text, nullable=True)  # JSON string
    
    # Projects (stored as JSON)
    # Format: [{"title": "Project 1", "description": "..."}]
    projects: Mapped[Optional[str]] = mapped_column(Text, nullable=True)  # JSON string

    # FAQs (stored as JSON)
    # Format: [{"question": "...", "answer": "..."}]
    faqs: Mapped[Optional[str]] = mapped_column(Text, nullable=True)  # JSON string

    # Certification
    certification_name: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    certification_authority: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    
    # SEO
    meta_title: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    meta_description: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    
    # Batch info
    next_batch_date: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    
    # Status
    status: Mapped[str] = mapped_column(String(50), default="draft", nullable=False)  # draft, published, archived
    featured: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    
    # Relationships
    category: Mapped["CourseCategory"] = relationship("CourseCategory", back_populates="courses")
    skills: Mapped[List[Skill]] = relationship(
        "Skill",
        secondary=course_skills,
        back_populates="courses",
    )
    enrollments: Mapped[List["CourseEnrollment"]] = relationship(
        "CourseEnrollment", back_populates="course", cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"<Course(id={self.id}, title='{self.title}', status='{self.status}')>"


class CourseEnrollment(Base, TimestampMixin):
    """Course enrollment/inquiry model for tracking student interest."""

    __tablename__ = "course_enrollments"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    
    # Student Info
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    email: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    phone: Mapped[str] = mapped_column(String(20), nullable=False)
    
    # Optional Info
    education: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    experience: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)  # e.g., "2-5 years"
    current_role: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    linkedin_url: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    
    # Course Interest
    course_id: Mapped[Optional[int]] = mapped_column(
        Integer, ForeignKey("courses.id", ondelete="SET NULL"), nullable=True
    )
    preferred_batch: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)  # weekday, weekend
    
    # Source tracking
    source: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)  # organic, google, facebook, etc.
    utm_campaign: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    utm_source: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    utm_medium: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    
    # Message/Notes
    message: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    
    # Status tracking
    status: Mapped[str] = mapped_column(String(50), default="new", nullable=False)
    # new, contacted, interested, enrolled, not_interested, closed
    
    # Admin notes
    notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    
    # Counselor assignment
    assigned_to: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    
    # Follow-up tracking
    last_contacted_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    next_followup_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    
    # Relationships
    course: Mapped[Optional["Course"]] = relationship("Course", back_populates="enrollments")

    def __repr__(self) -> str:
        return f"<CourseEnrollment(id={self.id}, name='{self.name}', status='{self.status}')>"

