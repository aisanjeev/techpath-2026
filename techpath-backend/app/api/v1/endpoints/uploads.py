"""File upload API endpoints with deduplication support."""
import hashlib
import os
from io import BytesIO
from tempfile import SpooledTemporaryFile
from typing import BinaryIO, Optional

from fastapi import APIRouter, Depends, UploadFile, File, Query
from sqlalchemy.ext.asyncio import AsyncSession
from PIL import Image

from app.core.exceptions import ValidationError
from app.core.constants import (
    ALLOWED_IMAGE_TYPES,
    ASSET_TYPES_ENABLED,
    MAX_UPLOAD_SIZE_MB,
    AssetStorageKind,
    AssetType,
    asset_rule,
)
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

# Read the body in chunks rather than in one gulp, and keep it off the heap once it
# gets big. Lecture assets go up to 500MB and production runs multiple workers, so
# `await file.read()` on this path would be an out-of-memory waiting to happen.
CHUNK_SIZE = 1024 * 1024
SPOOL_MAX_MEMORY = 8 * 1024 * 1024

# Leading bytes we can actually verify. A browser-supplied content type is a hint, not
# evidence — it is trivially forged, so anything container-based gets sniffed.
_MAGIC_PREFIXES: dict[str, tuple[bytes, ...]] = {
    ".pdf": (b"%PDF-",),
    ".zip": (b"PK\x03\x04", b"PK\x05\x06"),
    ".pptx": (b"PK\x03\x04",),
    ".xlsx": (b"PK\x03\x04",),
}


def calculate_file_hash(content: bytes) -> str:
    """Calculate SHA-256 hash of file content."""
    return hashlib.sha256(content).hexdigest()


async def _spool_and_hash(file: UploadFile, max_bytes: int) -> tuple[BinaryIO, str, int, bytes]:
    """Stream an upload to a spooled temp file, hashing as we go.

    Aborts the moment the size cap is passed rather than buffering the whole body first,
    so an oversized upload costs one chunk of memory instead of all of it.

    Returns the rewound spool, its SHA-256, its size, and its first chunk (for sniffing).
    """
    spool: BinaryIO = SpooledTemporaryFile(max_size=SPOOL_MAX_MEMORY)
    digest = hashlib.sha256()
    size = 0
    head = b""

    while True:
        chunk = await file.read(CHUNK_SIZE)
        if not chunk:
            break
        if not head:
            head = chunk[:16]
        size += len(chunk)
        if size > max_bytes:
            spool.close()
            raise ValidationError(
                f"File too large. Maximum size: {max_bytes // (1024 * 1024)}MB"
            )
        digest.update(chunk)
        spool.write(chunk)

    if size == 0:
        spool.close()
        raise ValidationError("Uploaded file is empty")

    spool.seek(0)
    return spool, digest.hexdigest(), size, head


def _validate_asset_file(file: UploadFile, asset_type: AssetType, head: bytes) -> None:
    """Check the declared type, the extension, and the bytes themselves agree."""
    rule = asset_rule(asset_type)

    if rule.allowed_content_types and file.content_type not in rule.allowed_content_types:
        raise ValidationError(
            f"Invalid content type '{file.content_type}' for {rule.label}. "
            f"Allowed: {', '.join(rule.allowed_content_types)}"
        )

    ext = os.path.splitext(file.filename or "")[1].lower()
    if rule.allowed_extensions and ext not in rule.allowed_extensions:
        raise ValidationError(
            f"Invalid file extension '{ext or 'none'}' for {rule.label}. "
            f"Allowed: {', '.join(rule.allowed_extensions)}"
        )

    expected = _MAGIC_PREFIXES.get(ext)
    if expected and not any(head.startswith(prefix) for prefix in expected):
        raise ValidationError(
            f"File contents do not look like a valid {ext} file"
        )


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
    Maximum size: MAX_UPLOAD_SIZE_MB (10MB)

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


@router.post("/lecture-asset", response_model=MediaUploadResponse)
async def upload_lecture_asset(
    asset_type: AssetType = Query(..., description="Which lecture asset type this file is for"),
    file: UploadFile = File(...),
    folder: str = Query("lectures", description="Folder to store the file"),
    db: AsyncSession = Depends(get_db),
    current_admin: User = Depends(get_current_admin_user),
) -> MediaUploadResponse:
    """Upload a file for a file-backed lecture asset (admin only).

    Type rules come from the asset registry in ``app.core.constants``, so the limits
    enforced here are the same ones the admin UI advertises. The body is streamed and
    hashed in chunks, never buffered whole.
    """
    if asset_type not in ASSET_TYPES_ENABLED:
        raise ValidationError(f"Asset type '{asset_type.value}' is not available yet")

    rule = asset_rule(asset_type)
    if rule.kind is not AssetStorageKind.FILE:
        raise ValidationError(
            f"{rule.label} assets are not file-backed — they take "
            f"{rule.kind.value.replace('_', ' ')} content instead of an upload"
        )

    spool, file_hash, size, head = await _spool_and_hash(file, rule.max_size_mb * 1024 * 1024)
    try:
        _validate_asset_file(file, asset_type, head)

        existing = await media_file_crud.get_by_hash(db, file_hash)
        if existing:
            return MediaUploadResponse(
                success=True,
                data=MediaFileResponse(
                    id=existing.id,
                    filename=existing.filename,
                    stored_path=existing.stored_path,
                    file_hash=existing.file_hash,
                    content_type=existing.content_type,
                    size=existing.size,
                    width=existing.width,
                    height=existing.height,
                    alt_text=existing.alt_text,
                    url=await storage_service.get_file_url(existing.stored_path),
                    created_at=existing.created_at,
                    updated_at=existing.updated_at,
                ),
                is_duplicate=True,
                message="File already exists, reusing",
            )

        stored_path = await storage_service.upload_file(
            spool,
            file.filename or f"{asset_type.value}",
            folder=folder,
            content_type=file.content_type,
        )
        media_file = await media_file_crud.create(
            db,
            MediaFileCreate(
                filename=file.filename or asset_type.value,
                stored_path=stored_path,
                file_hash=file_hash,
                content_type=file.content_type,
                size=size,
                width=None,
                height=None,
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
                url=await storage_service.get_file_url(stored_path),
                created_at=media_file.created_at,
                updated_at=media_file.updated_at,
            ),
            is_duplicate=False,
            message="File uploaded successfully",
        )
    finally:
        spool.close()


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
