"""Case Study API endpoints."""
from typing import List, Optional

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import NotFoundError, ConflictError
from app.crud.case_study import case_study_crud, case_study_tag_crud
from app.db.session import get_db
from app.schemas.case_study import (
    CaseStudyCreate,
    CaseStudyUpdate,
    CaseStudyResponse,
    CaseStudyListResponse,
    CaseStudyTagCreate,
    CaseStudyTagResponse,
)
from app.schemas.common import MessageResponse
from app.api.v1.dependencies import get_current_admin_user, get_optional_user
from app.services.media_tracking_service import track_media_usage, remove_entity_media_usages
from app.models.user import User

router = APIRouter()


# ----- Case Studies -----

@router.get("/", response_model=List[CaseStudyListResponse])
async def list_case_studies(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=50),
    featured: Optional[bool] = Query(None),
    industry: Optional[str] = Query(None, description="Filter by industry"),
    tag: Optional[str] = Query(None, description="Filter by tag slug"),
    status: Optional[str] = Query(None, description="Filter by status (admin only)"),
    db: AsyncSession = Depends(get_db),
    current_user: Optional[User] = Depends(get_optional_user),
) -> List[CaseStudyListResponse]:
    """
    List case studies with pagination and filtering.

    - **skip**: Number of records to skip
    - **limit**: Maximum records to return
    - **featured**: Filter featured case studies
    - **industry**: Filter by industry
    - **tag**: Filter by tag slug
    - **status**: Filter by status (admin only)
    """
    # Non-admins can only see published case studies
    if current_user is None or current_user.role != "admin":
        case_studies = await case_study_crud.get_published(
            db, skip=skip, limit=limit, featured=featured, industry=industry, tag_slug=tag
        )
    else:
        # Admin can see all case studies
        filters = {}
        if status:
            filters["status"] = status
        if featured is not None:
            filters["featured"] = featured
        if industry:
            filters["industry"] = industry

        case_studies = await case_study_crud.get_multi(
            db,
            skip=skip,
            limit=limit,
            filters=filters,
            order_by="created_at",
            order_desc=True,
        )

    return [CaseStudyListResponse.model_validate(cs) for cs in case_studies]


@router.get("/{slug}", response_model=CaseStudyResponse)
async def get_case_study(
    slug: str,
    db: AsyncSession = Depends(get_db),
    current_user: Optional[User] = Depends(get_optional_user),
) -> CaseStudyResponse:
    """Get a single case study by slug."""
    case_study = await case_study_crud.get_by_slug(db, slug=slug)
    if not case_study:
        raise NotFoundError("Case study")

    # Non-admins can only see published case studies
    if (current_user is None or current_user.role != "admin") and case_study.status != "published":
        raise NotFoundError("Case study")

    return CaseStudyResponse.model_validate(case_study)


@router.post("/", response_model=CaseStudyResponse, status_code=status.HTTP_201_CREATED)
async def create_case_study(
    case_study_in: CaseStudyCreate,
    db: AsyncSession = Depends(get_db),
    current_admin: User = Depends(get_current_admin_user),
) -> CaseStudyResponse:
    """Create a new case study (admin only)."""
    # Check slug uniqueness
    existing = await case_study_crud.get_by_slug(db, slug=case_study_in.slug)
    if existing:
        raise ConflictError("Case study with this slug already exists")

    case_study = await case_study_crud.create(db, obj_in=case_study_in, author_id=current_admin.id)
    
    # Track media usage for featured image
    if case_study_in.featured_image:
        await track_media_usage(
            db,
            image_url=case_study_in.featured_image,
            entity_type="case_study",
            entity_id=case_study.id,
            field_name="featured_image",
        )
    
    return CaseStudyResponse.model_validate(case_study)


@router.put("/{case_study_id}", response_model=CaseStudyResponse)
async def update_case_study(
    case_study_id: int,
    case_study_in: CaseStudyUpdate,
    db: AsyncSession = Depends(get_db),
    current_admin: User = Depends(get_current_admin_user),
) -> CaseStudyResponse:
    """Update a case study (admin only)."""
    case_study = await case_study_crud.get_with_tags(db, id=case_study_id)
    if not case_study:
        raise NotFoundError("Case study")

    # Check slug uniqueness if changing
    if case_study_in.slug and case_study_in.slug != case_study.slug:
        existing = await case_study_crud.get_by_slug(db, slug=case_study_in.slug)
        if existing:
            raise ConflictError("Case study with this slug already exists")

    old_featured_image = case_study.featured_image
    case_study = await case_study_crud.update(db, db_obj=case_study, obj_in=case_study_in)
    
    # Track media usage for featured image (handles add/change/remove)
    await track_media_usage(
        db,
        image_url=case_study_in.featured_image,
        entity_type="case_study",
        entity_id=case_study.id,
        field_name="featured_image",
        old_image_url=old_featured_image,
    )
    
    return CaseStudyResponse.model_validate(case_study)


@router.delete("/{case_study_id}", response_model=MessageResponse)
async def delete_case_study(
    case_study_id: int,
    db: AsyncSession = Depends(get_db),
    current_admin: User = Depends(get_current_admin_user),
) -> MessageResponse:
    """Delete a case study (admin only)."""
    case_study = await case_study_crud.get(db, id=case_study_id)
    if not case_study:
        raise NotFoundError("Case study")

    # Remove media usage records before deleting
    await remove_entity_media_usages(db, "case_study", case_study_id)
    
    await case_study_crud.delete(db, id=case_study_id)
    return MessageResponse(message="Case study deleted successfully")


# ----- Case Study Tags -----

@router.get("/tags/", response_model=List[CaseStudyTagResponse])
async def list_tags(
    db: AsyncSession = Depends(get_db),
) -> List[CaseStudyTagResponse]:
    """List all case study tags."""
    tags = await case_study_tag_crud.get_multi(db, limit=100)
    return [CaseStudyTagResponse.model_validate(t) for t in tags]


@router.post("/tags/", response_model=CaseStudyTagResponse, status_code=status.HTTP_201_CREATED)
async def create_tag(
    tag_in: CaseStudyTagCreate,
    db: AsyncSession = Depends(get_db),
    current_admin: User = Depends(get_current_admin_user),
) -> CaseStudyTagResponse:
    """Create a new case study tag (admin only)."""
    existing = await case_study_tag_crud.get_by_slug(db, slug=tag_in.slug)
    if existing:
        raise ConflictError("Tag with this slug already exists")

    tag = await case_study_tag_crud.create(db, obj_in=tag_in)
    return CaseStudyTagResponse.model_validate(tag)


@router.delete("/tags/{tag_id}", response_model=MessageResponse)
async def delete_tag(
    tag_id: int,
    db: AsyncSession = Depends(get_db),
    current_admin: User = Depends(get_current_admin_user),
) -> MessageResponse:
    """Delete a case study tag (admin only)."""
    tag = await case_study_tag_crud.get(db, id=tag_id)
    if not tag:
        raise NotFoundError("Tag")

    await case_study_tag_crud.delete(db, id=tag_id)
    return MessageResponse(message="Tag deleted successfully")

