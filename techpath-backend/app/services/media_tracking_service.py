"""Service for tracking media file usage across entities."""
import re
from typing import Optional
from urllib.parse import urlparse

from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.media import media_file_crud, media_usage_crud
from app.schemas.media import MediaFileUsageCreate


async def extract_file_path_from_url(url: str) -> Optional[str]:
    """Extract the stored file path from a URL."""
    if not url:
        return None
    
    # Handle full URLs (e.g., http://localhost:8000/uploads/images/abc.jpg)
    parsed = urlparse(url)
    path = parsed.path
    
    # Remove /uploads/ prefix if present
    if '/uploads/' in path:
        path = path.split('/uploads/', 1)[1]
    elif path.startswith('/'):
        path = path[1:]
    
    return path if path else None


async def track_media_usage(
    db: AsyncSession,
    image_url: Optional[str],
    entity_type: str,
    entity_id: int,
    field_name: str = "featured_image",
    old_image_url: Optional[str] = None,
) -> None:
    """
    Track media file usage for an entity.
    
    - If image_url is provided, creates a usage record
    - If old_image_url was different, removes the old usage record
    """
    # Remove old usage if image changed
    if old_image_url and old_image_url != image_url:
        old_path = await extract_file_path_from_url(old_image_url)
        if old_path:
            old_file = await media_file_crud.get_by_path(db, old_path)
            if old_file:
                # Find and remove the usage record
                usages = await media_usage_crud.get_by_entity(
                    db, entity_type, entity_id, field_name
                )
                for usage in usages:
                    if usage.file_id == old_file.id:
                        await media_usage_crud.delete(db, usage.id)
    
    # Create new usage if image provided
    if image_url:
        file_path = await extract_file_path_from_url(image_url)
        if file_path:
            media_file = await media_file_crud.get_by_path(db, file_path)
            if media_file:
                # Check if usage already exists
                existing = await media_usage_crud.find_existing(
                    db, media_file.id, entity_type, entity_id, field_name
                )
                if not existing:
                    await media_usage_crud.create(
                        db,
                        media_file.id,
                        MediaFileUsageCreate(
                            entity_type=entity_type,
                            entity_id=entity_id,
                            field_name=field_name,
                        ),
                    )


async def remove_entity_media_usages(
    db: AsyncSession,
    entity_type: str,
    entity_id: int,
) -> None:
    """Remove all media usage records for an entity (when entity is deleted)."""
    await media_usage_crud.delete_by_entity(db, entity_type, entity_id)

