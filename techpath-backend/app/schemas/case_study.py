"""Case Study-related Pydantic schemas."""
from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, ConfigDict, Field


class CaseStudyTagBase(BaseModel):
    """Base case study tag schema."""

    name: str = Field(..., min_length=1, max_length=100)
    slug: str = Field(..., min_length=1, max_length=100, pattern="^[a-z0-9-]+$")


class CaseStudyTagCreate(CaseStudyTagBase):
    """Schema for creating a case study tag."""

    pass


class CaseStudyTagResponse(CaseStudyTagBase):
    """Schema for case study tag response."""

    id: int

    model_config = ConfigDict(from_attributes=True)


class CaseStudyBase(BaseModel):
    """Base case study schema."""

    title: str = Field(..., min_length=1, max_length=255)
    slug: str = Field(..., min_length=1, max_length=255, pattern="^[a-z0-9-]+$")
    client_name: str = Field(..., min_length=1, max_length=255)
    industry: str = Field(..., min_length=1, max_length=100)
    challenge: str = Field(..., min_length=10)
    solution: str = Field(..., min_length=10)
    results: str = Field(..., min_length=10)


class CaseStudyCreate(CaseStudyBase):
    """Schema for creating a case study."""

    excerpt: Optional[str] = Field(None, max_length=500)
    content: Optional[str] = None
    featured_image: Optional[str] = None
    stat_value: Optional[str] = Field(None, max_length=50)
    stat_label: Optional[str] = Field(None, max_length=100)
    additional_stats: Optional[str] = None  # JSON string
    testimonial_quote: Optional[str] = None
    testimonial_author: Optional[str] = Field(None, max_length=255)
    testimonial_role: Optional[str] = Field(None, max_length=255)
    status: str = Field(default="draft", pattern="^(draft|published|archived)$")
    featured: bool = False
    published_at: Optional[datetime] = None
    meta_title: Optional[str] = Field(None, max_length=255)
    meta_description: Optional[str] = Field(None, max_length=500)
    tag_ids: Optional[List[int]] = None


class CaseStudyUpdate(BaseModel):
    """Schema for updating a case study."""

    title: Optional[str] = Field(None, min_length=1, max_length=255)
    slug: Optional[str] = Field(None, min_length=1, max_length=255, pattern="^[a-z0-9-]+$")
    client_name: Optional[str] = Field(None, min_length=1, max_length=255)
    industry: Optional[str] = Field(None, min_length=1, max_length=100)
    excerpt: Optional[str] = Field(None, max_length=500)
    challenge: Optional[str] = Field(None, min_length=10)
    solution: Optional[str] = Field(None, min_length=10)
    results: Optional[str] = Field(None, min_length=10)
    content: Optional[str] = None
    featured_image: Optional[str] = None
    stat_value: Optional[str] = Field(None, max_length=50)
    stat_label: Optional[str] = Field(None, max_length=100)
    additional_stats: Optional[str] = None
    testimonial_quote: Optional[str] = None
    testimonial_author: Optional[str] = Field(None, max_length=255)
    testimonial_role: Optional[str] = Field(None, max_length=255)
    status: Optional[str] = Field(None, pattern="^(draft|published|archived)$")
    featured: Optional[bool] = None
    published_at: Optional[datetime] = None
    meta_title: Optional[str] = Field(None, max_length=255)
    meta_description: Optional[str] = Field(None, max_length=500)
    tag_ids: Optional[List[int]] = None


class CaseStudyResponse(CaseStudyBase):
    """Schema for case study response."""

    id: int
    excerpt: Optional[str] = None
    content: Optional[str] = None
    featured_image: Optional[str] = None
    stat_value: Optional[str] = None
    stat_label: Optional[str] = None
    additional_stats: Optional[str] = None
    testimonial_quote: Optional[str] = None
    testimonial_author: Optional[str] = None
    testimonial_role: Optional[str] = None
    author_id: Optional[int] = None
    status: str
    featured: bool
    published_at: Optional[datetime] = None
    meta_title: Optional[str] = None
    meta_description: Optional[str] = None
    tags: List[CaseStudyTagResponse] = []
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class CaseStudyListResponse(BaseModel):
    """Schema for case study list item (without full content)."""

    id: int
    title: str
    slug: str
    client_name: str
    industry: str
    excerpt: Optional[str] = None
    featured_image: Optional[str] = None
    stat_value: Optional[str] = None
    stat_label: Optional[str] = None
    status: str
    featured: bool
    published_at: Optional[datetime] = None
    tags: List[CaseStudyTagResponse] = []
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

