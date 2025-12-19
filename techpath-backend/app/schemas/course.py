"""
Pydantic schemas for Course API validation and serialization.
"""

from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, ConfigDict, Field, field_validator
import json


# ----- Skill Schemas -----

class SkillBase(BaseModel):
    """Base skill schema."""
    name: str = Field(..., min_length=1, max_length=100)
    slug: str = Field(..., min_length=1, max_length=100, pattern="^[a-z0-9-]+$")


class SkillCreate(SkillBase):
    """Schema for creating a skill."""
    pass


class SkillResponse(SkillBase):
    """Schema for skill response."""
    id: int

    model_config = ConfigDict(from_attributes=True)


# ----- Course Category Schemas -----

class CourseCategoryBase(BaseModel):
    """Base course category schema."""
    name: str = Field(..., min_length=1, max_length=100)
    slug: str = Field(..., min_length=1, max_length=100, pattern="^[a-z0-9-]+$")
    description: Optional[str] = Field(None, max_length=500)
    icon: Optional[str] = Field(None, max_length=100)
    parent_id: Optional[int] = None
    display_order: int = 0
    is_active: bool = True


class CourseCategoryCreate(CourseCategoryBase):
    """Schema for creating a course category."""
    pass


class CourseCategoryUpdate(BaseModel):
    """Schema for updating a course category."""
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    slug: Optional[str] = Field(None, min_length=1, max_length=100, pattern="^[a-z0-9-]+$")
    description: Optional[str] = Field(None, max_length=500)
    icon: Optional[str] = Field(None, max_length=100)
    parent_id: Optional[int] = None
    display_order: Optional[int] = None
    is_active: Optional[bool] = None


class CourseCategoryResponse(CourseCategoryBase):
    """Schema for course category response."""
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class CourseCategoryTreeResponse(CourseCategoryResponse):
    """Schema for course category tree response with nested children."""
    children: List["CourseCategoryTreeResponse"] = []
    course_count: int = 0

    model_config = ConfigDict(from_attributes=True)


# ----- Curriculum & Project Schemas -----

class CurriculumModule(BaseModel):
    """Schema for a curriculum module."""
    title: str
    topics: List[str] = []
    duration: Optional[str] = None


class ProjectItem(BaseModel):
    """Schema for a project item."""
    title: str
    description: Optional[str] = None


# ----- Course Schemas -----

class CourseBase(BaseModel):
    """Base course schema."""
    title: str = Field(..., min_length=1, max_length=255)
    slug: str = Field(..., min_length=1, max_length=255, pattern="^[a-z0-9-]+$")
    category_id: int
    short_description: Optional[str] = Field(None, max_length=500)
    description: str = Field(..., min_length=10)
    
    # Pricing
    price: float = Field(..., ge=0)
    original_price: Optional[float] = Field(None, ge=0)
    emi_available: bool = True
    emi_amount: Optional[float] = Field(None, ge=0)
    currency: str = Field(default="INR", max_length=3)
    
    # Course Details
    duration: str = Field(..., max_length=50)
    duration_hours: Optional[int] = Field(None, ge=0)
    batch_size: int = Field(default=20, ge=1)
    level: str = Field(default="beginner", pattern="^(beginner|intermediate|advanced)$")
    
    # Stats
    rating: float = Field(default=0.0, ge=0, le=5)
    review_count: int = Field(default=0, ge=0)
    enrollment_count: int = Field(default=0, ge=0)
    placement_rate: Optional[int] = Field(None, ge=0, le=100)
    
    # Media
    featured_image: Optional[str] = None
    video_url: Optional[str] = None
    
    # Instructor
    instructor_name: Optional[str] = Field(None, max_length=255)
    instructor_title: Optional[str] = Field(None, max_length=255)
    instructor_bio: Optional[str] = None
    instructor_image: Optional[str] = None
    
    # Certification
    certification_name: Optional[str] = Field(None, max_length=255)
    certification_authority: Optional[str] = Field(None, max_length=255)
    
    # SEO
    meta_title: Optional[str] = Field(None, max_length=255)
    meta_description: Optional[str] = Field(None, max_length=500)
    
    # Batch info
    next_batch_date: Optional[datetime] = None
    
    # Status
    status: str = Field(default="draft", pattern="^(draft|published|archived)$")
    featured: bool = False
    is_active: bool = True


class CourseCreate(CourseBase):
    """Schema for creating a course."""
    # JSON fields as lists
    curriculum: Optional[List[CurriculumModule]] = None
    learning_outcomes: Optional[List[str]] = None
    prerequisites: Optional[List[str]] = None
    projects: Optional[List[ProjectItem]] = None
    skill_ids: Optional[List[int]] = None


class CourseUpdate(BaseModel):
    """Schema for updating a course."""
    title: Optional[str] = Field(None, min_length=1, max_length=255)
    slug: Optional[str] = Field(None, min_length=1, max_length=255, pattern="^[a-z0-9-]+$")
    category_id: Optional[int] = None
    short_description: Optional[str] = Field(None, max_length=500)
    description: Optional[str] = Field(None, min_length=10)
    
    # Pricing
    price: Optional[float] = Field(None, ge=0)
    original_price: Optional[float] = Field(None, ge=0)
    emi_available: Optional[bool] = None
    emi_amount: Optional[float] = Field(None, ge=0)
    currency: Optional[str] = Field(None, max_length=3)
    
    # Course Details
    duration: Optional[str] = Field(None, max_length=50)
    duration_hours: Optional[int] = Field(None, ge=0)
    batch_size: Optional[int] = Field(None, ge=1)
    level: Optional[str] = Field(None, pattern="^(beginner|intermediate|advanced)$")
    
    # Stats
    rating: Optional[float] = Field(None, ge=0, le=5)
    review_count: Optional[int] = Field(None, ge=0)
    enrollment_count: Optional[int] = Field(None, ge=0)
    placement_rate: Optional[int] = Field(None, ge=0, le=100)
    
    # Media
    featured_image: Optional[str] = None
    video_url: Optional[str] = None
    
    # Instructor
    instructor_name: Optional[str] = Field(None, max_length=255)
    instructor_title: Optional[str] = Field(None, max_length=255)
    instructor_bio: Optional[str] = None
    instructor_image: Optional[str] = None
    
    # JSON fields
    curriculum: Optional[List[CurriculumModule]] = None
    learning_outcomes: Optional[List[str]] = None
    prerequisites: Optional[List[str]] = None
    projects: Optional[List[ProjectItem]] = None
    
    # Certification
    certification_name: Optional[str] = Field(None, max_length=255)
    certification_authority: Optional[str] = Field(None, max_length=255)
    
    # SEO
    meta_title: Optional[str] = Field(None, max_length=255)
    meta_description: Optional[str] = Field(None, max_length=500)
    
    # Batch info
    next_batch_date: Optional[datetime] = None
    
    # Status
    status: Optional[str] = Field(None, pattern="^(draft|published|archived)$")
    featured: Optional[bool] = None
    is_active: Optional[bool] = None
    
    skill_ids: Optional[List[int]] = None


class CourseResponse(CourseBase):
    """Schema for full course response."""
    id: int
    category: CourseCategoryResponse
    skills: List[SkillResponse] = []
    curriculum: Optional[List[CurriculumModule]] = None
    learning_outcomes: Optional[List[str]] = None
    prerequisites: Optional[List[str]] = None
    projects: Optional[List[ProjectItem]] = None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)

    @field_validator('curriculum', 'learning_outcomes', 'prerequisites', 'projects', mode='before')
    @classmethod
    def parse_json_fields(cls, v):
        """Parse JSON string fields into Python objects."""
        if isinstance(v, str):
            try:
                return json.loads(v)
            except json.JSONDecodeError:
                return None
        return v


class CourseListResponse(BaseModel):
    """Schema for course list item (without full content)."""
    id: int
    title: str
    slug: str
    short_description: Optional[str] = None
    category: CourseCategoryResponse
    price: float
    original_price: Optional[float] = None
    emi_available: bool
    currency: str
    duration: str
    batch_size: int
    level: str
    rating: float
    review_count: int
    enrollment_count: int
    placement_rate: Optional[int] = None
    featured_image: Optional[str] = None
    skills: List[SkillResponse] = []
    next_batch_date: Optional[datetime] = None
    status: str
    featured: bool
    is_active: bool
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


# ----- Course Enrollment Schemas -----

class CourseEnrollmentBase(BaseModel):
    """Base course enrollment schema."""
    name: str = Field(..., min_length=1, max_length=255)
    email: str = Field(..., max_length=255)
    phone: str = Field(..., min_length=10, max_length=20)
    
    # Optional Info
    education: Optional[str] = Field(None, max_length=255)
    experience: Optional[str] = Field(None, max_length=100)
    current_role: Optional[str] = Field(None, max_length=255)
    linkedin_url: Optional[str] = Field(None, max_length=500)
    
    # Course Interest
    course_id: Optional[int] = None
    preferred_batch: Optional[str] = Field(None, max_length=100)
    
    # Source tracking
    source: Optional[str] = Field(None, max_length=100)
    utm_campaign: Optional[str] = Field(None, max_length=255)
    utm_source: Optional[str] = Field(None, max_length=100)
    utm_medium: Optional[str] = Field(None, max_length=100)
    
    # Message
    message: Optional[str] = None


class CourseEnrollmentCreate(CourseEnrollmentBase):
    """Schema for creating a course enrollment/inquiry."""
    pass


class CourseEnrollmentUpdate(BaseModel):
    """Schema for updating a course enrollment (admin only)."""
    status: Optional[str] = Field(None, pattern="^(new|contacted|interested|enrolled|not_interested|closed)$")
    notes: Optional[str] = None
    assigned_to: Optional[str] = Field(None, max_length=255)
    last_contacted_at: Optional[datetime] = None
    next_followup_at: Optional[datetime] = None


class CourseEnrollmentResponse(CourseEnrollmentBase):
    """Schema for course enrollment response."""
    id: int
    status: str
    notes: Optional[str] = None
    assigned_to: Optional[str] = None
    last_contacted_at: Optional[datetime] = None
    next_followup_at: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime
    course: Optional[CourseListResponse] = None

    model_config = ConfigDict(from_attributes=True)


class CourseEnrollmentListResponse(BaseModel):
    """Schema for course enrollment list (simplified)."""
    id: int
    name: str
    email: str
    phone: str
    course_id: Optional[int] = None
    course_title: Optional[str] = None
    status: str
    source: Optional[str] = None
    assigned_to: Optional[str] = None
    next_followup_at: Optional[datetime] = None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

