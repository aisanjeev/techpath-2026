"""Service-related Pydantic schemas."""
from datetime import datetime
from typing import List, Literal, Optional

from pydantic import BaseModel, ConfigDict, Field

LayoutSize = Literal["large", "small", "wide"]
AccentColor = Literal["purple", "cyan", "green", "amber", "blue"]
GraphicVariant = Literal["orbital", "code-window", "bar-chart", "none"]


class ServicePricingPlanItem(BaseModel):
    """One pricing tier for a service (same shape as pricing page plan)."""

    name: str = ""
    description: str = ""
    price: str = ""
    period: str = ""
    features: List[str] = Field(default_factory=list)
    cta: str = "Get Started"
    highlighted: bool = False


class ServiceFAQItem(BaseModel):
    """FAQ item for a service."""

    question: str = Field(..., min_length=1)
    answer: str = Field(..., min_length=1)


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
    pricing_plans: Optional[List[ServicePricingPlanItem]] = None
    faqs: Optional[List[ServiceFAQItem]] = None
    price: Optional[str] = None
    cta_text: str = Field(default="Learn More", max_length=100)
    cta_url: Optional[str] = None
    featured: bool = False
    display_order: int = 0
    is_active: bool = True
    
    # SEO fields
    meta_title: Optional[str] = Field(None, max_length=255)
    meta_description: Optional[str] = Field(None, max_length=500)
    og_image: Optional[str] = Field(None, max_length=500)
    canonical_url: Optional[str] = Field(None, max_length=500)
    no_index: bool = False

    # Bento layout
    layout_size: LayoutSize = "small"
    badge_label: Optional[str] = Field(None, max_length=50)
    tags: Optional[List[str]] = None
    stat_label: Optional[str] = Field(None, max_length=100)
    stat_value: Optional[str] = Field(None, max_length=50)
    accent_color: AccentColor = "blue"
    graphic_variant: GraphicVariant = "none"


class ServiceUpdate(BaseModel):
    """Schema for updating a service."""

    title: Optional[str] = Field(None, min_length=1, max_length=255)
    slug: Optional[str] = Field(None, min_length=1, max_length=255, pattern="^[a-z0-9-]+$")
    description: Optional[str] = Field(None, min_length=10)
    short_description: Optional[str] = Field(None, max_length=500)
    icon: Optional[str] = None
    image_url: Optional[str] = None
    features: Optional[List[str]] = None
    pricing_plans: Optional[List[ServicePricingPlanItem]] = None
    faqs: Optional[List[ServiceFAQItem]] = None
    price: Optional[str] = None
    cta_text: Optional[str] = Field(None, max_length=100)
    cta_url: Optional[str] = None
    featured: Optional[bool] = None
    display_order: Optional[int] = None
    is_active: Optional[bool] = None
    
    # SEO fields
    meta_title: Optional[str] = Field(None, max_length=255)
    meta_description: Optional[str] = Field(None, max_length=500)
    og_image: Optional[str] = Field(None, max_length=500)
    canonical_url: Optional[str] = Field(None, max_length=500)
    no_index: Optional[bool] = None

    # Bento layout
    layout_size: Optional[LayoutSize] = None
    badge_label: Optional[str] = Field(None, max_length=50)
    tags: Optional[List[str]] = None
    stat_label: Optional[str] = Field(None, max_length=100)
    stat_value: Optional[str] = Field(None, max_length=50)
    accent_color: Optional[AccentColor] = None
    graphic_variant: Optional[GraphicVariant] = None


class ServiceResponse(ServiceBase):
    """Schema for service response."""

    id: int
    icon: Optional[str] = None
    image_url: Optional[str] = None
    features: Optional[List[str]] = None
    pricing_plans: Optional[List[ServicePricingPlanItem]] = None
    faqs: Optional[List[ServiceFAQItem]] = None
    price: Optional[str] = None
    cta_text: str
    cta_url: Optional[str] = None
    featured: bool
    display_order: int
    is_active: bool
    created_at: datetime
    updated_at: datetime
    
    # SEO fields
    meta_title: Optional[str] = None
    meta_description: Optional[str] = None
    og_image: Optional[str] = None
    canonical_url: Optional[str] = None
    no_index: bool = False

    # Bento layout
    layout_size: LayoutSize = "small"
    badge_label: Optional[str] = None
    tags: Optional[List[str]] = None
    stat_label: Optional[str] = None
    stat_value: Optional[str] = None
    accent_color: AccentColor = "blue"
    graphic_variant: GraphicVariant = "none"

    model_config = ConfigDict(from_attributes=True)

    @classmethod
    def model_validate(cls, obj, **kwargs):
        """Custom validation to parse features and pricing_plans JSON strings."""
        import json

        try:
            obj_dict = {
                "id": obj.id,
                "title": obj.title,
                "slug": obj.slug,
                "description": obj.description,
                "short_description": obj.short_description,
                "icon": obj.icon,
                "image_url": obj.image_url,
                "features": (
                    json.loads(obj.features) if isinstance(obj.features, str) and obj.features else getattr(obj, "features", None)
                ),
                "price": obj.price,
                "cta_text": obj.cta_text,
                "cta_url": obj.cta_url,
                "featured": obj.featured,
                "display_order": obj.display_order,
                "is_active": obj.is_active,
                "created_at": obj.created_at,
                "updated_at": obj.updated_at,
                "meta_title": obj.meta_title if hasattr(obj, "meta_title") else None,
                "meta_description": obj.meta_description if hasattr(obj, "meta_description") else None,
                "og_image": obj.og_image if hasattr(obj, "og_image") else None,
                "canonical_url": obj.canonical_url if hasattr(obj, "canonical_url") else None,
                "no_index": obj.no_index if hasattr(obj, "no_index") else False,
                "layout_size": getattr(obj, "layout_size", "small") or "small",
                "badge_label": getattr(obj, "badge_label", None),
                "tags": (
                    json.loads(obj.tags) if isinstance(getattr(obj, "tags", None), str) and obj.tags
                    else getattr(obj, "tags", None)
                ),
                "stat_label": getattr(obj, "stat_label", None),
                "stat_value": getattr(obj, "stat_value", None),
                "accent_color": getattr(obj, "accent_color", "blue") or "blue",
                "graphic_variant": getattr(obj, "graphic_variant", "none") or "none",
            }
            if hasattr(obj, "pricing_plans"):
                obj_dict["pricing_plans"] = (
                    json.loads(obj.pricing_plans) if isinstance(obj.pricing_plans, str) and obj.pricing_plans else getattr(obj, "pricing_plans", None)
                )
            if hasattr(obj, "faqs"):
                obj_dict["faqs"] = (
                    json.loads(obj.faqs) if isinstance(obj.faqs, str) and obj.faqs else getattr(obj, "faqs", None)
                )
            return super().model_validate(obj_dict, **kwargs)
        except json.JSONDecodeError:
            pass
        return super().model_validate(obj, **kwargs)

