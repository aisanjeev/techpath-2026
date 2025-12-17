"""Service-related Pydantic schemas."""
from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, ConfigDict, Field


class ServiceBase(BaseModel):
    """Base service schema."""

    title: str = Field(..., min_length=1, max_length=255)
    slug: str = Field(..., min_length=1, max_length=255, pattern="^[a-z0-9-]+$")
    description: str = Field(..., min_length=10)
    short_description: Optional[str] = Field(None, max_length=500)


class ServiceCreate(ServiceBase):
    """Schema for creating a service."""

    icon: Optional[str] = None
    image_url: Optional[str] = None
    features: Optional[List[str]] = None
    price: Optional[str] = None
    cta_text: str = Field(default="Learn More", max_length=100)
    cta_url: Optional[str] = None
    featured: bool = False
    display_order: int = 0
    is_active: bool = True


class ServiceUpdate(BaseModel):
    """Schema for updating a service."""

    title: Optional[str] = Field(None, min_length=1, max_length=255)
    slug: Optional[str] = Field(None, min_length=1, max_length=255, pattern="^[a-z0-9-]+$")
    description: Optional[str] = Field(None, min_length=10)
    short_description: Optional[str] = Field(None, max_length=500)
    icon: Optional[str] = None
    image_url: Optional[str] = None
    features: Optional[List[str]] = None
    price: Optional[str] = None
    cta_text: Optional[str] = Field(None, max_length=100)
    cta_url: Optional[str] = None
    featured: Optional[bool] = None
    display_order: Optional[int] = None
    is_active: Optional[bool] = None


class ServiceResponse(ServiceBase):
    """Schema for service response."""

    id: int
    icon: Optional[str] = None
    image_url: Optional[str] = None
    features: Optional[List[str]] = None
    price: Optional[str] = None
    cta_text: str
    cta_url: Optional[str] = None
    featured: bool
    display_order: int
    is_active: bool
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)

    @classmethod
    def model_validate(cls, obj, **kwargs):
        """Custom validation to parse features JSON string."""
        import json

        if hasattr(obj, "features") and isinstance(obj.features, str):
            try:
                obj_dict = {
                    "id": obj.id,
                    "title": obj.title,
                    "slug": obj.slug,
                    "description": obj.description,
                    "short_description": obj.short_description,
                    "icon": obj.icon,
                    "image_url": obj.image_url,
                    "features": json.loads(obj.features) if obj.features else None,
                    "price": obj.price,
                    "cta_text": obj.cta_text,
                    "cta_url": obj.cta_url,
                    "featured": obj.featured,
                    "display_order": obj.display_order,
                    "is_active": obj.is_active,
                    "created_at": obj.created_at,
                    "updated_at": obj.updated_at,
                }
                return super().model_validate(obj_dict, **kwargs)
            except json.JSONDecodeError:
                pass
        return super().model_validate(obj, **kwargs)

