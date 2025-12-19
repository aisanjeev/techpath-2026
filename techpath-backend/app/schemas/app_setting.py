"""Pydantic schemas for app settings."""
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class AppSettingBase(BaseModel):
    """Base schema for app settings."""
    
    key: str = Field(..., max_length=100)
    display_name: str = Field(..., max_length=200)
    description: Optional[str] = None
    category: str = Field(..., max_length=50)
    value_type: str = Field(default="string", pattern="^(string|email|number|boolean|json)$")
    display_order: int = Field(default=0)


class AppSettingCreate(AppSettingBase):
    """Schema for creating an app setting."""
    value: Optional[str] = None


class AppSettingUpdate(BaseModel):
    """Schema for updating an app setting value."""
    value: Optional[str] = None


class AppSettingResponse(AppSettingBase):
    """Response schema for app settings."""
    
    id: int
    value: Optional[str] = None
    updated_by_id: Optional[int] = None
    updated_by_name: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class AppSettingCategoryResponse(BaseModel):
    """Response schema for grouped settings."""
    
    category: str
    display_name: str
    settings: list[AppSettingResponse]


# Category display names
CATEGORY_DISPLAY_NAMES = {
    "email": "Email Notifications",
    "general": "General Settings",
    "notifications": "Notification Settings",
    "seo": "SEO Settings",
}


def get_category_display_name(category: str) -> str:
    """Get human-readable category name."""
    return CATEGORY_DISPLAY_NAMES.get(category, category.replace("_", " ").title())

