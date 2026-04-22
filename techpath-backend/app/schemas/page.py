"""Pydantic schemas for standalone CMS pages."""
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field, field_validator


# Slugs that collide with existing static routes or directories in
# techpath-frontend/src/pages/. Keep in sync with the admin-side list in
# techpath-admin/src/lib/validations.ts (RESERVED_PAGE_SLUGS).
RESERVED_PAGE_SLUGS = {
    "about",
    "blog",
    "careers",
    "case-studies",
    "contact",
    "cookies",
    "faq",
    "pricing",
    "privacy",
    "services",
    "solutions",
    "support",
    "terms",
    "testimonials",
    "training",
    "api",
    "404",
    "index",
    "robots",
    "sitemap",
    "sitemap-index",
}


def _validate_slug_not_reserved(slug: Optional[str]) -> Optional[str]:
    if slug is None:
        return slug
    if slug.lower() in RESERVED_PAGE_SLUGS:
        raise ValueError(
            f"Slug '{slug}' is reserved by an existing site route. Choose another."
        )
    return slug


class PageBase(BaseModel):
    """Base page schema."""

    title: str = Field(..., min_length=1, max_length=255)
    slug: str = Field(..., min_length=1, max_length=255, pattern="^[a-z0-9-]+$")
    content: str = Field(..., min_length=1)


class PageCreate(PageBase):
    """Schema for creating a page."""

    content_type: str = Field(default="html", pattern="^(html|markdown)$")
    excerpt: Optional[str] = Field(None, max_length=500)
    featured_image: Optional[str] = None
    status: str = Field(default="draft", pattern="^(draft|published|archived)$")
    published_at: Optional[datetime] = None
    meta_title: Optional[str] = Field(None, max_length=255)
    meta_description: Optional[str] = Field(None, max_length=500)

    @field_validator("slug")
    @classmethod
    def slug_not_reserved(cls, v: str) -> str:
        return _validate_slug_not_reserved(v)  # type: ignore[return-value]


class PageUpdate(BaseModel):
    """Schema for updating a page. All fields optional."""

    title: Optional[str] = Field(None, min_length=1, max_length=255)
    slug: Optional[str] = Field(None, min_length=1, max_length=255, pattern="^[a-z0-9-]+$")
    content: Optional[str] = Field(None, min_length=1)
    content_type: Optional[str] = Field(None, pattern="^(html|markdown)$")
    excerpt: Optional[str] = Field(None, max_length=500)
    featured_image: Optional[str] = None
    status: Optional[str] = Field(None, pattern="^(draft|published|archived)$")
    published_at: Optional[datetime] = None
    meta_title: Optional[str] = Field(None, max_length=255)
    meta_description: Optional[str] = Field(None, max_length=500)

    @field_validator("slug")
    @classmethod
    def slug_not_reserved(cls, v: Optional[str]) -> Optional[str]:
        return _validate_slug_not_reserved(v)


class PageResponse(PageBase):
    """Full page response."""

    id: int
    content_type: str = "html"
    excerpt: Optional[str] = None
    featured_image: Optional[str] = None
    status: str
    published_at: Optional[datetime] = None
    meta_title: Optional[str] = None
    meta_description: Optional[str] = None
    author_id: Optional[int] = None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class PageListResponse(BaseModel):
    """Lighter page response for list endpoints (excludes full content)."""

    id: int
    title: str
    slug: str
    excerpt: Optional[str] = None
    featured_image: Optional[str] = None
    status: str
    published_at: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
