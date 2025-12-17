"""Blog API endpoints."""
from typing import List, Optional

from fastapi import APIRouter, Depends, Query, UploadFile, File, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import NotFoundError, ConflictError, ValidationError
from app.core.constants import ALLOWED_IMAGE_TYPES, MAX_UPLOAD_SIZE_MB
from app.crud.blog import blog_crud, blog_tag_crud
from app.db.session import get_db
from app.schemas.blog import (
    BlogPostCreate,
    BlogPostUpdate,
    BlogPostResponse,
    BlogPostListResponse,
    BlogTagCreate,
    BlogTagResponse,
)
from app.schemas.common import MessageResponse, PaginatedResponse, PaginationMeta
from app.api.v1.dependencies import get_current_admin_user, get_optional_user
from app.services.storage_service import storage_service
from app.models.user import User

router = APIRouter()


# ----- Blog Posts -----

@router.get("/posts", response_model=List[BlogPostListResponse])
async def list_posts(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=50),
    featured: Optional[bool] = Query(None),
    tag: Optional[str] = Query(None, description="Filter by tag slug"),
    status: Optional[str] = Query(None, description="Filter by status (admin only)"),
    db: AsyncSession = Depends(get_db),
    current_user: Optional[User] = Depends(get_optional_user),
) -> List[BlogPostListResponse]:
    """
    List blog posts with pagination and filtering.

    - **skip**: Number of records to skip
    - **limit**: Maximum records to return
    - **featured**: Filter featured posts
    - **tag**: Filter by tag slug
    - **status**: Filter by status (admin only)
    """
    # Non-admins can only see published posts
    if current_user is None or current_user.role != "admin":
        posts = await blog_crud.get_published(
            db, skip=skip, limit=limit, featured=featured, tag_slug=tag
        )
    else:
        # Admin can see all posts
        filters = {}
        if status:
            filters["status"] = status
        if featured is not None:
            filters["featured"] = featured

        posts = await blog_crud.get_multi(
            db,
            skip=skip,
            limit=limit,
            filters=filters,
            order_by="created_at",
            order_desc=True,
        )

    return [BlogPostListResponse.model_validate(p) for p in posts]


@router.get("/posts/{slug}", response_model=BlogPostResponse)
async def get_post(
    slug: str,
    db: AsyncSession = Depends(get_db),
    current_user: Optional[User] = Depends(get_optional_user),
) -> BlogPostResponse:
    """Get a single blog post by slug."""
    post = await blog_crud.get_by_slug(db, slug=slug)
    if not post:
        raise NotFoundError("Blog post")

    # Non-admins can only see published posts
    if (current_user is None or current_user.role != "admin") and post.status != "published":
        raise NotFoundError("Blog post")

    return BlogPostResponse.model_validate(post)


@router.post("/posts", response_model=BlogPostResponse, status_code=status.HTTP_201_CREATED)
async def create_post(
    post_in: BlogPostCreate,
    db: AsyncSession = Depends(get_db),
    current_admin: User = Depends(get_current_admin_user),
) -> BlogPostResponse:
    """Create a new blog post (admin only)."""
    # Check slug uniqueness
    existing = await blog_crud.get_by_slug(db, slug=post_in.slug)
    if existing:
        raise ConflictError("Blog post with this slug already exists")

    post = await blog_crud.create(db, obj_in=post_in, author_id=current_admin.id)
    return BlogPostResponse.model_validate(post)


@router.put("/posts/{post_id}", response_model=BlogPostResponse)
async def update_post(
    post_id: int,
    post_in: BlogPostUpdate,
    db: AsyncSession = Depends(get_db),
    current_admin: User = Depends(get_current_admin_user),
) -> BlogPostResponse:
    """Update a blog post (admin only)."""
    post = await blog_crud.get_with_tags(db, id=post_id)
    if not post:
        raise NotFoundError("Blog post")

    # Check slug uniqueness if changing
    if post_in.slug and post_in.slug != post.slug:
        existing = await blog_crud.get_by_slug(db, slug=post_in.slug)
        if existing:
            raise ConflictError("Blog post with this slug already exists")

    post = await blog_crud.update(db, db_obj=post, obj_in=post_in)
    return BlogPostResponse.model_validate(post)


@router.delete("/posts/{post_id}", response_model=MessageResponse)
async def delete_post(
    post_id: int,
    db: AsyncSession = Depends(get_db),
    current_admin: User = Depends(get_current_admin_user),
) -> MessageResponse:
    """Delete a blog post (admin only)."""
    post = await blog_crud.get(db, id=post_id)
    if not post:
        raise NotFoundError("Blog post")

    await blog_crud.delete(db, id=post_id)
    return MessageResponse(message="Blog post deleted successfully")


@router.post("/posts/{post_id}/upload-image")
async def upload_post_image(
    post_id: int,
    file: UploadFile = File(...),
    db: AsyncSession = Depends(get_db),
    current_admin: User = Depends(get_current_admin_user),
) -> dict:
    """Upload an image for a blog post (admin only)."""
    # Verify post exists
    post = await blog_crud.get(db, id=post_id)
    if not post:
        raise NotFoundError("Blog post")

    # Validate file type
    if file.content_type not in ALLOWED_IMAGE_TYPES:
        raise ValidationError(
            f"Invalid file type. Allowed: {', '.join(ALLOWED_IMAGE_TYPES)}"
        )

    # Validate file size
    content = await file.read()
    if len(content) > MAX_UPLOAD_SIZE_MB * 1024 * 1024:
        raise ValidationError(f"File too large. Maximum size: {MAX_UPLOAD_SIZE_MB}MB")

    # Reset file position
    await file.seek(0)

    # Upload file
    file_path = await storage_service.upload_file(
        file.file,
        file.filename,
        folder="blog",
        content_type=file.content_type,
    )

    # Get URL
    file_url = await storage_service.get_file_url(file_path)

    return {
        "success": True,
        "data": {
            "path": file_path,
            "url": file_url,
        },
    }


# ----- Blog Tags -----

@router.get("/tags", response_model=List[BlogTagResponse])
async def list_tags(
    db: AsyncSession = Depends(get_db),
) -> List[BlogTagResponse]:
    """List all blog tags."""
    tags = await blog_tag_crud.get_multi(db, limit=100)
    return [BlogTagResponse.model_validate(t) for t in tags]


@router.post("/tags", response_model=BlogTagResponse, status_code=status.HTTP_201_CREATED)
async def create_tag(
    tag_in: BlogTagCreate,
    db: AsyncSession = Depends(get_db),
    current_admin: User = Depends(get_current_admin_user),
) -> BlogTagResponse:
    """Create a new blog tag (admin only)."""
    existing = await blog_tag_crud.get_by_slug(db, slug=tag_in.slug)
    if existing:
        raise ConflictError("Tag with this slug already exists")

    tag = await blog_tag_crud.create(db, obj_in=tag_in)
    return BlogTagResponse.model_validate(tag)


@router.delete("/tags/{tag_id}", response_model=MessageResponse)
async def delete_tag(
    tag_id: int,
    db: AsyncSession = Depends(get_db),
    current_admin: User = Depends(get_current_admin_user),
) -> MessageResponse:
    """Delete a blog tag (admin only)."""
    tag = await blog_tag_crud.get(db, id=tag_id)
    if not tag:
        raise NotFoundError("Tag")

    await blog_tag_crud.delete(db, id=tag_id)
    return MessageResponse(message="Tag deleted successfully")

