"""Blog API endpoints."""
from typing import List, Optional

from fastapi import APIRouter, Depends, Query, UploadFile, File, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import NotFoundError, ConflictError, ValidationError
from app.core.constants import ALLOWED_IMAGE_TYPES, MAX_UPLOAD_SIZE_MB
from app.crud.blog import blog_crud, blog_tag_crud, blog_category_crud
from app.db.session import get_db
from app.schemas.blog import (
    BlogPostCreate,
    BlogPostUpdate,
    BlogPostResponse,
    BlogPostListResponse,
    BlogTagCreate,
    BlogTagResponse,
    BlogCategoryCreate,
    BlogCategoryUpdate,
    BlogCategoryResponse,
    BlogCategoryTreeResponse,
)
from app.schemas.common import MessageResponse, PaginatedResponse, PaginationMeta
from app.api.v1.dependencies import get_current_admin_user, get_optional_user
from app.services.storage_service import storage_service
from app.services.media_tracking_service import track_media_usage, remove_entity_media_usages
from app.models.user import User
from app.models.blog import BlogCategory

router = APIRouter()


# ----- Blog Categories -----

@router.get("/categories", response_model=List[BlogCategoryResponse])
async def list_categories(
    active_only: bool = Query(True, description="Only return active categories"),
    db: AsyncSession = Depends(get_db),
) -> List[BlogCategoryResponse]:
    """List all blog categories."""
    categories = await blog_category_crud.get_all_with_hierarchy(db, active_only=active_only)
    return [BlogCategoryResponse.model_validate(c) for c in categories]


@router.get("/categories/tree", response_model=List[BlogCategoryTreeResponse])
async def get_category_tree(
    active_only: bool = Query(True, description="Only return active categories"),
    db: AsyncSession = Depends(get_db),
) -> List[BlogCategoryTreeResponse]:
    """Get categories as a hierarchical tree (root categories with nested children)."""
    root_categories = await blog_category_crud.get_root_categories(db, active_only=active_only)
    
    async def build_tree_response(category: "BlogCategory") -> BlogCategoryTreeResponse:
        """Recursively build tree response with post counts."""
        post_count = await blog_category_crud.get_post_count(db, category.id)
        
        # Build children recursively (children are already loaded by selectinload)
        children_responses = []
        for child in category.children:
            if active_only and not child.is_active:
                continue
            child_response = await build_tree_response(child)
            children_responses.append(child_response)
        
        return BlogCategoryTreeResponse(
            id=category.id,
            name=category.name,
            slug=category.slug,
            description=category.description,
            parent_id=category.parent_id,
            display_order=category.display_order,
            is_active=category.is_active,
            created_at=category.created_at,
            updated_at=category.updated_at,
            children=children_responses,
            post_count=post_count,
        )
    
    result = []
    for cat in root_categories:
        cat_response = await build_tree_response(cat)
        result.append(cat_response)
    
    return result


@router.get("/categories/{category_id}", response_model=BlogCategoryResponse)
async def get_category(
    category_id: int,
    db: AsyncSession = Depends(get_db),
) -> BlogCategoryResponse:
    """Get a single category by ID."""
    category = await blog_category_crud.get(db, id=category_id)
    if not category:
        raise NotFoundError("Category")
    return BlogCategoryResponse.model_validate(category)


@router.post("/categories", response_model=BlogCategoryResponse, status_code=status.HTTP_201_CREATED)
async def create_category(
    category_in: BlogCategoryCreate,
    db: AsyncSession = Depends(get_db),
    current_admin: User = Depends(get_current_admin_user),
) -> BlogCategoryResponse:
    """Create a new blog category (admin only)."""
    # Check slug uniqueness
    existing = await blog_category_crud.get_by_slug(db, slug=category_in.slug)
    if existing:
        raise ConflictError("Category with this slug already exists")
    
    # Validate parent if provided
    if category_in.parent_id:
        parent = await blog_category_crud.get(db, id=category_in.parent_id)
        if not parent:
            raise NotFoundError("Parent category")
        # Check depth (max 3 levels: 0, 1, 2)
        if parent.level >= 2:
            raise ValidationError("Maximum category depth is 3 levels")
    
    try:
        category = await blog_category_crud.create(db, obj_in=category_in)
    except ValueError as e:
        raise ValidationError(str(e))
    
    return BlogCategoryResponse.model_validate(category)


@router.put("/categories/{category_id}", response_model=BlogCategoryResponse)
async def update_category(
    category_id: int,
    category_in: BlogCategoryUpdate,
    db: AsyncSession = Depends(get_db),
    current_admin: User = Depends(get_current_admin_user),
) -> BlogCategoryResponse:
    """Update a blog category (admin only)."""
    category = await blog_category_crud.get(db, id=category_id)
    if not category:
        raise NotFoundError("Category")
    
    # Check slug uniqueness if changing
    if category_in.slug and category_in.slug != category.slug:
        existing = await blog_category_crud.get_by_slug(db, slug=category_in.slug)
        if existing:
            raise ConflictError("Category with this slug already exists")
    
    # Validate parent change
    if category_in.parent_id is not None:
        if category_in.parent_id == category_id:
            raise ValidationError("Category cannot be its own parent")
        if category_in.parent_id:
            parent = await blog_category_crud.get(db, id=category_in.parent_id)
            if not parent:
                raise NotFoundError("Parent category")
            if parent.level >= 2:
                raise ValidationError("Maximum category depth is 3 levels")
    
    category = await blog_category_crud.update(db, db_obj=category, obj_in=category_in)
    return BlogCategoryResponse.model_validate(category)


@router.delete("/categories/{category_id}", response_model=MessageResponse)
async def delete_category(
    category_id: int,
    db: AsyncSession = Depends(get_db),
    current_admin: User = Depends(get_current_admin_user),
) -> MessageResponse:
    """Delete a blog category (admin only). Fails if category has posts."""
    category = await blog_category_crud.get(db, id=category_id)
    if not category:
        raise NotFoundError("Category")
    
    # Check if category has posts
    if await blog_category_crud.has_posts(db, category_id):
        raise ValidationError("Cannot delete category with posts. Reassign posts first.")
    
    # Check for "Uncategorized" category protection
    if category.slug == "uncategorized":
        raise ValidationError("Cannot delete the default 'Uncategorized' category")
    
    await blog_category_crud.delete(db, id=category_id)
    return MessageResponse(message="Category deleted successfully")


# ----- Blog Posts -----

@router.get("/posts", response_model=List[BlogPostListResponse])
async def list_posts(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=50),
    featured: Optional[bool] = Query(None),
    tag: Optional[str] = Query(None, description="Filter by tag slug"),
    category: Optional[str] = Query(None, description="Filter by category slug"),
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
    - **category**: Filter by category slug
    - **status**: Filter by status (admin only)
    """
    # Non-admins can only see published posts
    if current_user is None or current_user.role != "admin":
        posts = await blog_crud.get_published(
            db, skip=skip, limit=limit, featured=featured, tag_slug=tag, category_slug=category
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
    
    # Verify category exists
    category = await blog_category_crud.get(db, id=post_in.category_id)
    if not category:
        raise NotFoundError("Category")

    post = await blog_crud.create(db, obj_in=post_in, author_id=current_admin.id)
    
    # Track media usage for featured image
    if post_in.featured_image:
        await track_media_usage(
            db,
            image_url=post_in.featured_image,
            entity_type="blog_post",
            entity_id=post.id,
            field_name="featured_image",
        )
    
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
    
    # Verify category exists if changing
    if post_in.category_id:
        category = await blog_category_crud.get(db, id=post_in.category_id)
        if not category:
            raise NotFoundError("Category")

    old_featured_image = post.featured_image
    post = await blog_crud.update(db, db_obj=post, obj_in=post_in)
    
    # Track media usage for featured image (handles add/change/remove)
    await track_media_usage(
        db,
        image_url=post_in.featured_image,
        entity_type="blog_post",
        entity_id=post.id,
        field_name="featured_image",
        old_image_url=old_featured_image,
    )
    
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

    # Remove media usage records before deleting post
    await remove_entity_media_usages(db, "blog_post", post_id)
    
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
