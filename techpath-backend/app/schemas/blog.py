"""Blog-related Pydantic schemas."""
from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, ConfigDict, Field


# ----- Blog Categories -----

class BlogCategoryBase(BaseModel):
    """Base blog category schema."""

    name: str = Field(..., min_length=1, max_length=100)
    slug: str = Field(..., min_length=1, max_length=100, pattern="^[a-z0-9-]+$")


class BlogCategoryCreate(BlogCategoryBase):
    """Schema for creating a blog category."""

    description: Optional[str] = Field(None, max_length=500)
    parent_id: Optional[int] = None
    display_order: int = 0
    is_active: bool = True


class BlogCategoryUpdate(BaseModel):
    """Schema for updating a blog category."""

    name: Optional[str] = Field(None, min_length=1, max_length=100)
    slug: Optional[str] = Field(None, min_length=1, max_length=100, pattern="^[a-z0-9-]+$")
    description: Optional[str] = Field(None, max_length=500)
    parent_id: Optional[int] = None
    display_order: Optional[int] = None
    is_active: Optional[bool] = None


class BlogCategoryResponse(BlogCategoryBase):
    """Schema for blog category response."""

    id: int
    description: Optional[str] = None
    parent_id: Optional[int] = None
    display_order: int
    is_active: bool
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class BlogCategoryTreeResponse(BlogCategoryResponse):
    """Schema for blog category with children (tree structure)."""

    children: List["BlogCategoryTreeResponse"] = []
    post_count: int = 0

    model_config = ConfigDict(from_attributes=True)


class BlogCategorySimpleResponse(BaseModel):
    """Simple category response for embedding in posts."""

    id: int
    name: str
    slug: str

    model_config = ConfigDict(from_attributes=True)


# ----- Blog Tags -----

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


# ----- Blog Posts -----

class BlogPostBase(BaseModel):
    """Base blog post schema."""

    title: str = Field(..., min_length=1, max_length=255)
    slug: str = Field(..., min_length=1, max_length=255, pattern="^[a-z0-9-]+$")
    content: str = Field(..., min_length=10)


class BlogPostCreate(BlogPostBase):
    """Schema for creating a blog post."""

    category_id: int = Field(..., description="Category ID (required)")
    excerpt: Optional[str] = Field(None, max_length=500)
    content_type: str = Field(default="html", pattern="^(html|markdown)$")
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
    category_id: Optional[int] = None
    excerpt: Optional[str] = Field(None, max_length=500)
    content: Optional[str] = Field(None, min_length=10)
    content_type: Optional[str] = Field(None, pattern="^(html|markdown)$")
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
    category_id: int
    category: BlogCategorySimpleResponse
    excerpt: Optional[str] = None
    content_type: str = "html"
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
    category_id: int
    category: BlogCategorySimpleResponse
    excerpt: Optional[str] = None
    featured_image: Optional[str] = None
    status: str
    featured: bool
    reading_time: Optional[int] = None
    published_at: Optional[datetime] = None
    tags: List[BlogTagResponse] = []
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
