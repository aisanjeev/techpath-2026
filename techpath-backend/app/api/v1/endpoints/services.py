"""Services API endpoints."""
from typing import List, Optional

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import NotFoundError, ConflictError
from app.services.storage_service import storage_service
from app.crud.service import service_crud
from app.db.session import get_db
from app.schemas.service import ServiceCreate, ServiceUpdate, ServiceResponse
from app.schemas.common import MessageResponse, PaginatedResponse, PaginationMeta
from app.api.v1.dependencies import get_current_admin_user
from app.services.media_tracking_service import track_media_usage, remove_entity_media_usages
from app.models.user import User

router = APIRouter()


@router.get("/", response_model=List[ServiceResponse])
async def list_services(
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(20, ge=1, le=100, description="Maximum records to return"),
    featured: Optional[bool] = Query(None, description="Filter by featured status"),
    active_only: bool = Query(True, description="Only return active services"),
    db: AsyncSession = Depends(get_db),
) -> List[ServiceResponse]:
    """
    List all services with optional filtering.

    - **skip**: Number of records to skip (pagination)
    - **limit**: Maximum records to return
    - **featured**: Filter featured services only
    - **active_only**: Only return active services (default: true)
    """
    if active_only:
        services = await service_crud.get_active(
            db, skip=skip, limit=limit, featured=featured
        )
    else:
        filters = {}
        if featured is not None:
            filters["featured"] = featured
        services = await service_crud.get_multi(
            db,
            skip=skip,
            limit=limit,
            filters=filters,
            order_by="display_order",
        )

    result = []
    for s in services:
        r = ServiceResponse.model_validate(s)
        if r.image_url:
            r.image_url = await storage_service.resolve_url(r.image_url)
        result.append(r)
    return result


@router.get("/{slug}", response_model=ServiceResponse)
async def get_service(
    slug: str,
    db: AsyncSession = Depends(get_db),
) -> ServiceResponse:
    """Get a single service by slug."""
    service = await service_crud.get_by_slug(db, slug=slug)
    if not service:
        raise NotFoundError("Service")
    response = ServiceResponse.model_validate(service)
    if response.image_url:
        response.image_url = await storage_service.resolve_url(response.image_url)
    return response


@router.post("/", response_model=ServiceResponse, status_code=status.HTTP_201_CREATED)
async def create_service(
    service_in: ServiceCreate,
    db: AsyncSession = Depends(get_db),
    current_admin: User = Depends(get_current_admin_user),
) -> ServiceResponse:
    """
    Create a new service (admin only).

    - **title**: Service title
    - **slug**: URL-friendly slug (unique)
    - **description**: Full description
    - **features**: List of feature strings
    """
    # Check if slug already exists
    existing = await service_crud.get_by_slug(db, slug=service_in.slug)
    if existing:
        raise ConflictError("Service with this slug already exists")

    service = await service_crud.create(db, obj_in=service_in)
    
    # Track media usage for image
    if service_in.image_url:
        await track_media_usage(
            db,
            image_url=service_in.image_url,
            entity_type="service",
            entity_id=service.id,
            field_name="image_url",
        )
    
    return ServiceResponse.model_validate(service)


@router.put("/{service_id}", response_model=ServiceResponse)
async def update_service(
    service_id: int,
    service_in: ServiceUpdate,
    db: AsyncSession = Depends(get_db),
    current_admin: User = Depends(get_current_admin_user),
) -> ServiceResponse:
    """Update a service (admin only)."""
    service = await service_crud.get(db, id=service_id)
    if not service:
        raise NotFoundError("Service")

    # Check slug uniqueness if changing
    if service_in.slug and service_in.slug != service.slug:
        existing = await service_crud.get_by_slug(db, slug=service_in.slug)
        if existing:
            raise ConflictError("Service with this slug already exists")

    old_image_url = service.image_url
    service = await service_crud.update(db, db_obj=service, obj_in=service_in)
    
    # Track media usage for image (handles add/change/remove)
    await track_media_usage(
        db,
        image_url=service_in.image_url,
        entity_type="service",
        entity_id=service.id,
        field_name="image_url",
        old_image_url=old_image_url,
    )
    
    return ServiceResponse.model_validate(service)


@router.delete("/{service_id}", response_model=MessageResponse)
async def delete_service(
    service_id: int,
    db: AsyncSession = Depends(get_db),
    current_admin: User = Depends(get_current_admin_user),
) -> MessageResponse:
    """Delete a service (admin only)."""
    service = await service_crud.get(db, id=service_id)
    if not service:
        raise NotFoundError("Service")

    # Remove media usage records before deleting
    await remove_entity_media_usages(db, "service", service_id)
    
    await service_crud.delete(db, id=service_id)
    return MessageResponse(message="Service deleted successfully")

