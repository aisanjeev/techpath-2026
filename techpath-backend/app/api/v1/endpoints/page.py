"""API endpoints for standalone CMS pages."""
from datetime import datetime, timezone
from typing import Optional

from fastapi import APIRouter, Depends, File, Query, UploadFile, status
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.v1.dependencies import get_current_admin_user, get_optional_user
from app.core.constants import ALLOWED_IMAGE_TYPES, MAX_UPLOAD_SIZE_MB
from app.core.exceptions import ConflictError, NotFoundError, ValidationError
from app.crud.page import page_crud
from app.db.session import get_db
from app.models.user import User
from app.schemas.common import MessageResponse
from app.schemas.page import (
    PageCreate,
    PageListResponse,
    PageResponse,
    PageUpdate,
)
from app.services.media_tracking_service import (
    remove_entity_media_usages,
    track_media_usage,
)
from app.services.storage_service import storage_service

router = APIRouter()


@router.get("")
async def list_pages(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    status_filter: Optional[str] = Query(None, alias="status"),
    search: Optional[str] = Query(None),
    db: AsyncSession = Depends(get_db),
    current_user: Optional[User] = Depends(get_optional_user),
) -> JSONResponse:
    """List pages. Non-admins see only published, scheduled-visible pages."""
    is_admin = current_user is not None and current_user.role == "admin"

    if not is_admin:
        total = await page_crud.get_published_count(db)
        pages = await page_crud.get_published(db, skip=skip, limit=limit)
    else:
        filters: dict = {}
        if status_filter:
            filters["status"] = status_filter
        total = await page_crud.get_multi_count(
            db, filters=filters or None, search=search
        )
        pages = await page_crud.get_multi(
            db,
            skip=skip,
            limit=limit,
            filters=filters,
            search=search,
            order_by="updated_at",
            order_desc=True,
        )

    data = [
        PageListResponse.model_validate(p).model_dump(mode="json") for p in pages
    ]
    return JSONResponse(content=data, headers={"X-Total-Count": str(total)})


@router.get("/{slug}", response_model=PageResponse)
async def get_page(
    slug: str,
    db: AsyncSession = Depends(get_db),
    current_user: Optional[User] = Depends(get_optional_user),
) -> PageResponse:
    """Get a single page by slug. Non-admins see only published, live pages."""
    page = await page_crud.get_by_slug(db, slug=slug)
    if not page:
        raise NotFoundError("Page")

    is_admin = current_user is not None and current_user.role == "admin"
    if not is_admin:
        if page.status != "published":
            raise NotFoundError("Page")
        if page.published_at:
            # MySQL returns naive datetimes; normalise both sides to UTC-naive for comparison
            pub_at = page.published_at.replace(tzinfo=None) if page.published_at.tzinfo else page.published_at
            now = datetime.now(timezone.utc).replace(tzinfo=None)
            if pub_at > now:
                raise NotFoundError("Page")

    return PageResponse.model_validate(page)


@router.post("", response_model=PageResponse, status_code=status.HTTP_201_CREATED)
async def create_page(
    page_in: PageCreate,
    db: AsyncSession = Depends(get_db),
    current_admin: User = Depends(get_current_admin_user),
) -> PageResponse:
    """Create a new page (admin only)."""
    existing = await page_crud.get_by_slug(db, slug=page_in.slug)
    if existing:
        raise ConflictError("A page with this slug already exists")

    page = await page_crud.create(db, obj_in=page_in, author_id=current_admin.id)

    if page_in.featured_image:
        await track_media_usage(
            db,
            image_url=page_in.featured_image,
            entity_type="page",
            entity_id=page.id,
            field_name="featured_image",
        )

    return PageResponse.model_validate(page)


@router.put("/{page_id}", response_model=PageResponse)
async def update_page(
    page_id: int,
    page_in: PageUpdate,
    db: AsyncSession = Depends(get_db),
    current_admin: User = Depends(get_current_admin_user),
) -> PageResponse:
    """Update a page (admin only)."""
    page = await page_crud.get(db, id=page_id)
    if not page:
        raise NotFoundError("Page")

    if page_in.slug and page_in.slug != page.slug:
        existing = await page_crud.get_by_slug(db, slug=page_in.slug)
        if existing:
            raise ConflictError("A page with this slug already exists")

    old_featured_image = page.featured_image
    page = await page_crud.update(db, db_obj=page, obj_in=page_in)

    # Featured image lifecycle: only touch if the field was explicitly provided.
    if "featured_image" in page_in.model_dump(exclude_unset=True):
        await track_media_usage(
            db,
            image_url=page_in.featured_image,
            entity_type="page",
            entity_id=page.id,
            field_name="featured_image",
            old_image_url=old_featured_image,
        )

    return PageResponse.model_validate(page)


@router.delete("/{page_id}", response_model=MessageResponse)
async def delete_page(
    page_id: int,
    db: AsyncSession = Depends(get_db),
    current_admin: User = Depends(get_current_admin_user),
) -> MessageResponse:
    """Delete a page (admin only)."""
    page = await page_crud.get(db, id=page_id)
    if not page:
        raise NotFoundError("Page")

    await remove_entity_media_usages(db, "page", page_id)
    await page_crud.delete(db, id=page_id)
    return MessageResponse(message="Page deleted successfully")


@router.post("/{page_id}/upload-image")
async def upload_page_image(
    page_id: int,
    file: UploadFile = File(...),
    db: AsyncSession = Depends(get_db),
    current_admin: User = Depends(get_current_admin_user),
) -> dict:
    """Upload an image for a page (admin only)."""
    page = await page_crud.get(db, id=page_id)
    if not page:
        raise NotFoundError("Page")

    if file.content_type not in ALLOWED_IMAGE_TYPES:
        raise ValidationError(
            f"Invalid file type. Allowed: {', '.join(ALLOWED_IMAGE_TYPES)}"
        )

    content = await file.read()
    if len(content) > MAX_UPLOAD_SIZE_MB * 1024 * 1024:
        raise ValidationError(f"File too large. Maximum size: {MAX_UPLOAD_SIZE_MB}MB")

    await file.seek(0)

    file_path = await storage_service.upload_file(
        file.file,
        file.filename,
        folder="pages",
        content_type=file.content_type,
    )
    file_url = await storage_service.get_file_url(file_path)

    return {
        "success": True,
        "data": {
            "path": file_path,
            "url": file_url,
        },
    }
