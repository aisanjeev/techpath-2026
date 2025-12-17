"""Blog-related Pydantic schemas."""
from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, ConfigDict, Field


class BlogTagBase(BaseModel):
    """Base blog tag schema."""

    name: str = Field(..., min_length=1, max_length=100)
    slug: str = Field(..., min_length=1, max_length=100, pattern="^[a-z0-9-]+$")


class BlogTagCreate(BlogTagBase):
    """Schema for creating a blog tag."""

    pass


class BlogTagResponse(BlogTagBase):
    """Schema for blog tag response."""

    id: int

    model_config = ConfigDict(from_attributes=True)


class BlogPostBase(BaseModel):
    """Base blog post schema."""

    title: str = Field(..., min_length=1, max_length=255)
    slug: str = Field(..., min_length=1, max_length=255, pattern="^[a-z0-9-]+$")
    content: str = Field(..., min_length=10)


class BlogPostCreate(BlogPostBase):
    """Schema for creating a blog post."""

    excerpt: Optional[str] = Field(None, max_length=500)
    featured_image: Optional[str] = None
    status: str = Field(default="draft", pattern="^(draft|published|archived)$")
    featured: bool = False
    reading_time: Optional[int] = None
    published_at: Optional[datetime] = None
    meta_title: Optional[str] = Field(None, max_length=255)
    meta_description: Optional[str] = Field(None, max_length=500)
    tag_ids: Optional[List[int]] = None


class BlogPostUpdate(BaseModel):
    """Schema for updating a blog post."""

    title: Optional[str] = Field(None, min_length=1, max_length=255)
    slug: Optional[str] = Field(None, min_length=1, max_length=255, pattern="^[a-z0-9-]+$")
    excerpt: Optional[str] = Field(None, max_length=500)
    content: Optional[str] = Field(None, min_length=10)
    featured_image: Optional[str] = None
    status: Optional[str] = Field(None, pattern="^(draft|published|archived)$")
    featured: Optional[bool] = None
    reading_time: Optional[int] = None
    published_at: Optional[datetime] = None
    meta_title: Optional[str] = Field(None, max_length=255)
    meta_description: Optional[str] = Field(None, max_length=500)
    tag_ids: Optional[List[int]] = None


class BlogPostResponse(BlogPostBase):
    """Schema for blog post response."""

    id: int
    excerpt: Optional[str] = None
    featured_image: Optional[str] = None
    author_id: Optional[int] = None
    status: str
    featured: bool
    reading_time: Optional[int] = None
    published_at: Optional[datetime] = None
    meta_title: Optional[str] = None
    meta_description: Optional[str] = None
    tags: List[BlogTagResponse] = []
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class BlogPostListResponse(BaseModel):
    """Schema for blog post list item (without full content)."""

    id: int
    title: str
    slug: str
    excerpt: Optional[str] = None
    featured_image: Optional[str] = None
    status: str
    featured: bool
    reading_time: Optional[int] = None
    published_at: Optional[datetime] = None
    tags: List[BlogTagResponse] = []
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

