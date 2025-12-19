"""API endpoints for app settings management."""
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.v1.dependencies import get_db, get_current_admin_user
from app.crud.app_setting import app_setting_crud
from app.models.user import User
from app.schemas.app_setting import (
    AppSettingResponse,
    AppSettingUpdate,
    AppSettingCategoryResponse,
    get_category_display_name,
)

router = APIRouter()


@router.get("", response_model=list[AppSettingCategoryResponse])
async def list_settings(
    category: Optional[str] = None,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_admin_user),
):
    """
    List all app settings grouped by category.
    
    Admin only.
    """
    settings = await app_setting_crud.get_all(db, category=category)
    
    # Group by category
    categories: dict[str, list] = {}
    for setting in settings:
        if setting.category not in categories:
            categories[setting.category] = []
        
        categories[setting.category].append(AppSettingResponse(
            id=setting.id,
            key=setting.key,
            value=setting.value,
            display_name=setting.display_name,
            description=setting.description,
            category=setting.category,
            value_type=setting.value_type,
            display_order=setting.display_order,
            updated_by_id=setting.updated_by_id,
            updated_by_name=setting.updated_by.name if setting.updated_by else None,
            created_at=setting.created_at,
            updated_at=setting.updated_at,
        ))
    
    # Build response
    return [
        AppSettingCategoryResponse(
            category=cat,
            display_name=get_category_display_name(cat),
            settings=settings_list,
        )
        for cat, settings_list in categories.items()
    ]


@router.get("/{key}", response_model=AppSettingResponse)
async def get_setting(
    key: str,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_admin_user),
):
    """
    Get a specific setting by key.
    
    Admin only.
    """
    setting = await app_setting_crud.get_by_key(db, key)
    
    if not setting:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Setting '{key}' not found",
        )
    
    return AppSettingResponse(
        id=setting.id,
        key=setting.key,
        value=setting.value,
        display_name=setting.display_name,
        description=setting.description,
        category=setting.category,
        value_type=setting.value_type,
        display_order=setting.display_order,
        updated_by_id=setting.updated_by_id,
        updated_by_name=setting.updated_by.name if setting.updated_by else None,
        created_at=setting.created_at,
        updated_at=setting.updated_at,
    )


@router.put("/{key}", response_model=AppSettingResponse)
async def update_setting(
    key: str,
    data: AppSettingUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_admin_user),
):
    """
    Update a setting value.
    
    Admin only.
    """
    # Check if setting exists
    existing = await app_setting_crud.get_by_key(db, key)
    if not existing:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Setting '{key}' not found",
        )
    
    # Update the setting
    setting = await app_setting_crud.update_value(
        db,
        key=key,
        value=data.value,
        updated_by_id=current_user.id,
    )
    
    return AppSettingResponse(
        id=setting.id,
        key=setting.key,
        value=setting.value,
        display_name=setting.display_name,
        description=setting.description,
        category=setting.category,
        value_type=setting.value_type,
        display_order=setting.display_order,
        updated_by_id=setting.updated_by_id,
        updated_by_name=setting.updated_by.name if setting.updated_by else None,
        created_at=setting.created_at,
        updated_at=setting.updated_at,
    )


# Whitelist of public settings (accessible without auth)
PUBLIC_KEYS = {
    # Company info
    "company_name",
    "company_email",
    "company_phone",
    "company_address",
    # Social media
    "social_twitter",
    "social_linkedin",
    "social_facebook",
    # SEO settings
    "seo_default_title",
    "seo_default_description",
    "google_analytics_id",
}


# Public endpoint for frontend to get all public settings
@router.get("/public/all")
async def get_all_public_settings(
    db: AsyncSession = Depends(get_db),
):
    """
    Get all public settings (no auth required).
    
    Returns all publicly accessible settings for the frontend.
    """
    settings = await app_setting_crud.get_all(db)
    
    result = {}
    for setting in settings:
        if setting.key in PUBLIC_KEYS:
            result[setting.key] = setting.value
    
    return {"success": True, "data": result}


# Public endpoint for frontend to get specific settings
@router.get("/public/{key}")
async def get_public_setting(
    key: str,
    db: AsyncSession = Depends(get_db),
):
    """
    Get a public setting value (no auth required).
    
    Only returns the value, not metadata.
    Only certain keys are allowed.
    """
    if key not in PUBLIC_KEYS:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="This setting is not publicly accessible",
        )
    
    value = await app_setting_crud.get_value(db, key)
    return {"key": key, "value": value}

