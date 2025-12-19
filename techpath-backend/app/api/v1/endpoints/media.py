"""Media library API endpoints."""
from typing import List, Optional

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import NotFoundError, ValidationError
from app.api.v1.dependencies import get_current_admin_user
from app.db.session import get_db
from app.services.storage_service import storage_service
from app.models.user import User
from app.crud.media import media_file_crud, media_usage_crud
from app.schemas.media import (
    MediaFileUpdate,
    MediaFileResponse,
    MediaFileDetailResponse,
    MediaFileListResponse,
    MediaFileUsageResponse,
)
from app.schemas.common import MessageResponse

router = APIRouter()


@router.get("/", response_model=List[MediaFileListResponse])
async def list_media_files(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    content_type: Optional[str] = Query(None, description="Filter by type: image, document, or specific MIME type"),
    search: Optional[str] = Query(None, description="Search by filename"),
    db: AsyncSession = Depends(get_db),
    current_admin: User = Depends(get_current_admin_user),
) -> List[MediaFileListResponse]:
    """
    List all media files with pagination and filtering (admin only).
    
    - **skip**: Number of records to skip
    - **limit**: Maximum records to return
    - **content_type**: Filter by 'image', 'document', or specific MIME type
    - **search**: Search by filename
    """
    files, total = await media_file_crud.get_multi(
        db,
        skip=skip,
        limit=limit,
        content_type=content_type,
        search=search,
    )

    result = []
    for f in files:
        # Get usage count
        usage_count = await media_file_crud.get_usage_count(db, f.id)
        # Get URL
        url = await storage_service.get_file_url(f.stored_path)
        
        result.append(
            MediaFileListResponse(
                id=f.id,
                filename=f.filename,
                stored_path=f.stored_path,
                content_type=f.content_type,
                size=f.size,
                width=f.width,
                height=f.height,
                alt_text=f.alt_text,
                url=url,
                usage_count=usage_count,
                created_at=f.created_at,
            )
        )

    return result


@router.get("/{media_id}", response_model=MediaFileDetailResponse)
async def get_media_file(
    media_id: int,
    db: AsyncSession = Depends(get_db),
    current_admin: User = Depends(get_current_admin_user),
) -> MediaFileDetailResponse:
    """Get a media file with usage details (admin only)."""
    media_file = await media_file_crud.get_with_usages(db, media_id)
    if not media_file:
        raise NotFoundError("Media file")

    url = await storage_service.get_file_url(media_file.stored_path)
    usage_count = len(media_file.usages)

    return MediaFileDetailResponse(
        id=media_file.id,
        filename=media_file.filename,
        stored_path=media_file.stored_path,
        file_hash=media_file.file_hash,
        content_type=media_file.content_type,
        size=media_file.size,
        width=media_file.width,
        height=media_file.height,
        alt_text=media_file.alt_text,
        url=url,
        created_at=media_file.created_at,
        updated_at=media_file.updated_at,
        usages=[
            MediaFileUsageResponse(
                id=u.id,
                file_id=u.file_id,
                entity_type=u.entity_type,
                entity_id=u.entity_id,
                field_name=u.field_name,
                created_at=u.created_at,
            )
            for u in media_file.usages
        ],
        usage_count=usage_count,
    )


@router.patch("/{media_id}", response_model=MediaFileResponse)
async def update_media_file(
    media_id: int,
    update_data: MediaFileUpdate,
    db: AsyncSession = Depends(get_db),
    current_admin: User = Depends(get_current_admin_user),
) -> MediaFileResponse:
    """Update a media file's metadata (admin only)."""
    media_file = await media_file_crud.get(db, media_id)
    if not media_file:
        raise NotFoundError("Media file")

    media_file = await media_file_crud.update(db, media_file, update_data)
    url = await storage_service.get_file_url(media_file.stored_path)

    return MediaFileResponse(
        id=media_file.id,
        filename=media_file.filename,
        stored_path=media_file.stored_path,
        file_hash=media_file.file_hash,
        content_type=media_file.content_type,
        size=media_file.size,
        width=media_file.width,
        height=media_file.height,
        alt_text=media_file.alt_text,
        url=url,
        created_at=media_file.created_at,
        updated_at=media_file.updated_at,
    )


@router.delete("/{media_id}", response_model=MessageResponse)
async def delete_media_file(
    media_id: int,
    db: AsyncSession = Depends(get_db),
    current_admin: User = Depends(get_current_admin_user),
) -> MessageResponse:
    """
    Delete a media file (admin only).
    
    Fails if the file is currently in use by any entity.
    """
    media_file = await media_file_crud.get(db, media_id)
    if not media_file:
        raise NotFoundError("Media file")

    # Check if file is in use
    if await media_file_crud.is_in_use(db, media_id):
        usage_count = await media_file_crud.get_usage_count(db, media_id)
        raise ValidationError(
            f"Cannot delete file. It is currently used in {usage_count} place(s). "
            "Remove all usages first."
        )

    # Delete from storage
    await storage_service.delete_file(media_file.stored_path)

    # Delete from database
    await media_file_crud.delete(db, media_id)

    return MessageResponse(message="Media file deleted successfully")


@router.get("/{media_id}/usages", response_model=List[MediaFileUsageResponse])
async def get_media_file_usages(
    media_id: int,
    db: AsyncSession = Depends(get_db),
    current_admin: User = Depends(get_current_admin_user),
) -> List[MediaFileUsageResponse]:
    """Get all usages of a media file (admin only)."""
    media_file = await media_file_crud.get(db, media_id)
    if not media_file:
        raise NotFoundError("Media file")

    usages = await media_usage_crud.get_by_file(db, media_id)

    return [
        MediaFileUsageResponse(
            id=u.id,
            file_id=u.file_id,
            entity_type=u.entity_type,
            entity_id=u.entity_id,
            field_name=u.field_name,
            created_at=u.created_at,
        )
        for u in usages
    ]


@router.delete("/{media_id}/usages/{usage_id}", response_model=MessageResponse)
async def remove_media_usage(
    media_id: int,
    usage_id: int,
    db: AsyncSession = Depends(get_db),
    current_admin: User = Depends(get_current_admin_user),
) -> MessageResponse:
    """Remove a specific usage record (admin only)."""
    usage = await media_usage_crud.get(db, usage_id)
    if not usage or usage.file_id != media_id:
        raise NotFoundError("Usage record")

    await media_usage_crud.delete(db, usage_id)

    return MessageResponse(message="Usage record removed successfully")

