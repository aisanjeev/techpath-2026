"""File upload API endpoints with deduplication support."""
import hashlib
from io import BytesIO
from typing import Optional

from fastapi import APIRouter, Depends, UploadFile, File, Query
from sqlalchemy.ext.asyncio import AsyncSession
from PIL import Image

from app.core.exceptions import ValidationError
from app.core.constants import ALLOWED_IMAGE_TYPES, MAX_UPLOAD_SIZE_MB
from app.api.v1.dependencies import get_current_admin_user
from app.db.session import get_db
from app.services.storage_service import storage_service
from app.models.user import User
from app.crud.media import media_file_crud, media_usage_crud
from app.schemas.media import (
    MediaFileCreate,
    MediaFileResponse,
    MediaFileUsageCreate,
    MediaUploadResponse,
)

router = APIRouter()


def calculate_file_hash(content: bytes) -> str:
    """Calculate SHA-256 hash of file content."""
    return hashlib.sha256(content).hexdigest()


def get_image_dimensions(content: bytes, content_type: str) -> tuple[Optional[int], Optional[int]]:
    """Get image dimensions if the file is an image."""
    if not content_type.startswith("image/"):
        return None, None
    
    try:
        with Image.open(BytesIO(content)) as img:
            return img.width, img.height
    except Exception:
        return None, None


@router.post("/image", response_model=MediaUploadResponse)
async def upload_image(
    file: UploadFile = File(...),
    folder: str = Query("images", description="Folder to store the image"),
    entity_type: Optional[str] = Query(None, description="Entity type for usage tracking"),
    entity_id: Optional[int] = Query(None, description="Entity ID for usage tracking"),
    field_name: str = Query("featured_image", description="Field name for usage tracking"),
    db: AsyncSession = Depends(get_db),
    current_admin: User = Depends(get_current_admin_user),
) -> MediaUploadResponse:
    """
    Upload an image file with deduplication (admin only).
    
    Supported formats: JPEG, PNG, GIF, WebP
    Maximum size: 5MB
    
    If the same file already exists (based on hash), reuses the existing file.
    Optionally tracks usage by specifying entity_type, entity_id, and field_name.
    """
    # Validate file type
    if file.content_type not in ALLOWED_IMAGE_TYPES:
        raise ValidationError(
            f"Invalid file type. Allowed: {', '.join(ALLOWED_IMAGE_TYPES)}"
        )

    # Read and validate file size
    content = await file.read()
    if len(content) > MAX_UPLOAD_SIZE_MB * 1024 * 1024:
        raise ValidationError(f"File too large. Maximum size: {MAX_UPLOAD_SIZE_MB}MB")

    # Calculate file hash for deduplication
    file_hash = calculate_file_hash(content)

    # Check if file already exists
    existing_file = await media_file_crud.get_by_hash(db, file_hash)
    is_duplicate = existing_file is not None

    if existing_file:
        # File already exists, reuse it
        media_file = existing_file
        file_url = await storage_service.get_file_url(media_file.stored_path)
    else:
        # Upload new file
        await file.seek(0)
        file_path = await storage_service.upload_file(
            file.file,
            file.filename or "image",
            folder=folder,
            content_type=file.content_type,
        )

        # Get image dimensions
        width, height = get_image_dimensions(content, file.content_type)

        # Create media file record
        media_file = await media_file_crud.create(
            db,
            MediaFileCreate(
                filename=file.filename or "image",
                stored_path=file_path,
                file_hash=file_hash,
                content_type=file.content_type,
                size=len(content),
                width=width,
                height=height,
            ),
        )

        file_url = await storage_service.get_file_url(file_path)

    # Track usage if entity info provided
    if entity_type and entity_id:
        # Check if usage already exists
        existing_usage = await media_usage_crud.find_existing(
            db, media_file.id, entity_type, entity_id, field_name
        )
        if not existing_usage:
            await media_usage_crud.create(
                db,
                media_file.id,
                MediaFileUsageCreate(
                    entity_type=entity_type,
                    entity_id=entity_id,
                    field_name=field_name,
                ),
            )

    return MediaUploadResponse(
        success=True,
        data=MediaFileResponse(
            id=media_file.id,
            filename=media_file.filename,
            stored_path=media_file.stored_path,
            file_hash=media_file.file_hash,
            content_type=media_file.content_type,
            size=media_file.size,
            width=media_file.width,
            height=media_file.height,
            alt_text=media_file.alt_text,
            url=file_url,
            created_at=media_file.created_at,
            updated_at=media_file.updated_at,
        ),
        is_duplicate=is_duplicate,
        message="File already exists, reusing" if is_duplicate else "File uploaded successfully",
    )


@router.post("/file", response_model=MediaUploadResponse)
async def upload_file(
    file: UploadFile = File(...),
    folder: str = Query("files", description="Folder to store the file"),
    entity_type: Optional[str] = Query(None, description="Entity type for usage tracking"),
    entity_id: Optional[int] = Query(None, description="Entity ID for usage tracking"),
    field_name: str = Query("attachment", description="Field name for usage tracking"),
    db: AsyncSession = Depends(get_db),
    current_admin: User = Depends(get_current_admin_user),
) -> MediaUploadResponse:
    """
    Upload a general file with deduplication (admin only).
    
    Allowed types: Images, PDFs, Documents
    Maximum size: 10MB
    """
    # Define allowed file types
    ALLOWED_FILE_TYPES = [
        "image/jpeg",
        "image/png",
        "image/gif",
        "image/webp",
        "application/pdf",
        "application/msword",
        "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        "text/plain",
    ]
    MAX_FILE_SIZE_MB = 10

    # Validate file type
    if file.content_type not in ALLOWED_FILE_TYPES:
        raise ValidationError(
            f"Invalid file type. Allowed: images, PDF, Word documents"
        )

    # Read and validate file size
    content = await file.read()
    if len(content) > MAX_FILE_SIZE_MB * 1024 * 1024:
        raise ValidationError(f"File too large. Maximum size: {MAX_FILE_SIZE_MB}MB")

    # Calculate file hash for deduplication
    file_hash = calculate_file_hash(content)

    # Check if file already exists
    existing_file = await media_file_crud.get_by_hash(db, file_hash)
    is_duplicate = existing_file is not None

    if existing_file:
        # File already exists, reuse it
        media_file = existing_file
        file_url = await storage_service.get_file_url(media_file.stored_path)
    else:
        # Upload new file
        await file.seek(0)
        file_path = await storage_service.upload_file(
            file.file,
            file.filename or "file",
            folder=folder,
            content_type=file.content_type,
        )

        # Get image dimensions if applicable
        width, height = get_image_dimensions(content, file.content_type)

        # Create media file record
        media_file = await media_file_crud.create(
            db,
            MediaFileCreate(
                filename=file.filename or "file",
                stored_path=file_path,
                file_hash=file_hash,
                content_type=file.content_type,
                size=len(content),
                width=width,
                height=height,
            ),
        )

        file_url = await storage_service.get_file_url(file_path)

    # Track usage if entity info provided
    if entity_type and entity_id:
        existing_usage = await media_usage_crud.find_existing(
            db, media_file.id, entity_type, entity_id, field_name
        )
        if not existing_usage:
            await media_usage_crud.create(
                db,
                media_file.id,
                MediaFileUsageCreate(
                    entity_type=entity_type,
                    entity_id=entity_id,
                    field_name=field_name,
                ),
            )

    return MediaUploadResponse(
        success=True,
        data=MediaFileResponse(
            id=media_file.id,
            filename=media_file.filename,
            stored_path=media_file.stored_path,
            file_hash=media_file.file_hash,
            content_type=media_file.content_type,
            size=media_file.size,
            width=media_file.width,
            height=media_file.height,
            alt_text=media_file.alt_text,
            url=file_url,
            created_at=media_file.created_at,
            updated_at=media_file.updated_at,
        ),
        is_duplicate=is_duplicate,
        message="File already exists, reusing" if is_duplicate else "File uploaded successfully",
    )


@router.delete("/{file_path:path}")
async def delete_file(
    file_path: str,
    current_admin: User = Depends(get_current_admin_user),
) -> dict:
    """Delete an uploaded file (admin only). Use /media/{id} endpoint for tracked files."""
    success = await storage_service.delete_file(file_path)
    
    if not success:
        raise ValidationError("File not found or could not be deleted")
    
    return {
        "success": True,
        "message": "File deleted successfully",
    }
