"""
Course API endpoints for TechPath training platform.
Includes endpoints for courses, categories, skills, and enrollments.
"""

from typing import List, Optional

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import NotFoundError, ConflictError, ValidationError
from app.crud.course import (
    course_crud,
    course_category_crud,
    course_enrollment_crud,
    skill_crud,
)
from app.db.session import get_db
from app.schemas.course import (
    CourseCreate,
    CourseUpdate,
    CourseResponse,
    CourseListResponse,
    CourseCategoryCreate,
    CourseCategoryUpdate,
    CourseCategoryResponse,
    CourseCategoryTreeResponse,
    CourseEnrollmentCreate,
    CourseEnrollmentUpdate,
    CourseEnrollmentResponse,
    CourseEnrollmentListResponse,
    SkillCreate,
    SkillResponse,
)
from app.schemas.common import MessageResponse, PaginatedResponse, PaginationMeta
from app.api.v1.dependencies import get_current_admin_user, get_optional_user
from app.models.user import User

router = APIRouter()


# ----- Skills -----

@router.get("/skills", response_model=List[SkillResponse])
async def list_skills(
    db: AsyncSession = Depends(get_db),
) -> List[SkillResponse]:
    """List all skills/tags."""
    skills = await skill_crud.get_multi(db, limit=200)
    return [SkillResponse.model_validate(s) for s in skills]


@router.post("/skills", response_model=SkillResponse, status_code=status.HTTP_201_CREATED)
async def create_skill(
    skill_in: SkillCreate,
    db: AsyncSession = Depends(get_db),
    current_admin: User = Depends(get_current_admin_user),
) -> SkillResponse:
    """Create a new skill (admin only)."""
    existing = await skill_crud.get_by_slug(db, slug=skill_in.slug)
    if existing:
        raise ConflictError("Skill with this slug already exists")
    skill = await skill_crud.create(db, obj_in=skill_in)
    return SkillResponse.model_validate(skill)


@router.delete("/skills/{skill_id}", response_model=MessageResponse)
async def delete_skill(
    skill_id: int,
    db: AsyncSession = Depends(get_db),
    current_admin: User = Depends(get_current_admin_user),
) -> MessageResponse:
    """Delete a skill (admin only)."""
    skill = await skill_crud.get(db, id=skill_id)
    if not skill:
        raise NotFoundError("Skill")
    await skill_crud.delete(db, id=skill_id)
    return MessageResponse(message="Skill deleted successfully")


# ----- Course Categories -----

@router.get("/categories", response_model=List[CourseCategoryResponse])
async def list_categories(
    active_only: bool = Query(True, description="Only return active categories"),
    db: AsyncSession = Depends(get_db),
) -> List[CourseCategoryResponse]:
    """List all course categories."""
    if active_only:
        categories = await course_category_crud.get_all_active(db)
    else:
        categories = await course_category_crud.get_multi(db, limit=100)
    return [CourseCategoryResponse.model_validate(c) for c in categories]


@router.get("/categories/tree", response_model=List[CourseCategoryTreeResponse])
async def get_category_tree(
    active_only: bool = Query(True, description="Only return active categories"),
    db: AsyncSession = Depends(get_db),
) -> List[CourseCategoryTreeResponse]:
    """Get categories as a hierarchical tree."""
    root_categories = await course_category_crud.get_root_categories(db, active_only=active_only)

    async def build_tree_node(category_obj, current_db):
        node = CourseCategoryTreeResponse.model_validate(category_obj)
        node.course_count = await course_category_crud.get_course_count(current_db, category_obj.id)
        node.children = []
        for child_obj in category_obj.children:
            if active_only and not child_obj.is_active:
                continue
            node.children.append(await build_tree_node(child_obj, current_db))
        return node

    result = []
    for cat in root_categories:
        result.append(await build_tree_node(cat, db))

    return result


@router.get("/categories/{category_id}", response_model=CourseCategoryResponse)
async def get_category(
    category_id: int,
    db: AsyncSession = Depends(get_db),
) -> CourseCategoryResponse:
    """Get a single category by ID."""
    category = await course_category_crud.get(db, id=category_id)
    if not category:
        raise NotFoundError("Category")
    return CourseCategoryResponse.model_validate(category)


@router.post("/categories", response_model=CourseCategoryResponse, status_code=status.HTTP_201_CREATED)
async def create_category(
    category_in: CourseCategoryCreate,
    db: AsyncSession = Depends(get_db),
    current_admin: User = Depends(get_current_admin_user),
) -> CourseCategoryResponse:
    """Create a new course category (admin only)."""
    existing = await course_category_crud.get_by_slug(db, slug=category_in.slug)
    if existing:
        raise ConflictError("Category with this slug already exists")
    category = await course_category_crud.create(db, obj_in=category_in)
    return CourseCategoryResponse.model_validate(category)


@router.put("/categories/{category_id}", response_model=CourseCategoryResponse)
async def update_category(
    category_id: int,
    category_in: CourseCategoryUpdate,
    db: AsyncSession = Depends(get_db),
    current_admin: User = Depends(get_current_admin_user),
) -> CourseCategoryResponse:
    """Update a course category (admin only)."""
    category = await course_category_crud.get(db, id=category_id)
    if not category:
        raise NotFoundError("Category")

    if category_in.slug and category_in.slug != category.slug:
        existing = await course_category_crud.get_by_slug(db, slug=category_in.slug)
        if existing:
            raise ConflictError("Category with this slug already exists")

    category = await course_category_crud.update(db, db_obj=category, obj_in=category_in)
    return CourseCategoryResponse.model_validate(category)


@router.delete("/categories/{category_id}", response_model=MessageResponse)
async def delete_category(
    category_id: int,
    db: AsyncSession = Depends(get_db),
    current_admin: User = Depends(get_current_admin_user),
) -> MessageResponse:
    """Delete a course category (admin only). Fails if category has courses."""
    category = await course_category_crud.get(db, id=category_id)
    if not category:
        raise NotFoundError("Category")

    if await course_category_crud.has_courses(db, category_id):
        raise ValidationError("Cannot delete category with associated courses. Reassign courses first.")

    await course_category_crud.delete(db, id=category_id)
    return MessageResponse(message="Category deleted successfully")


# ----- Courses -----

@router.get("/", response_model=PaginatedResponse[CourseListResponse])
async def list_courses(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=50),
    featured: Optional[bool] = Query(None),
    category: Optional[str] = Query(None, description="Filter by category slug"),
    level: Optional[str] = Query(None, description="Filter by level (beginner, intermediate, advanced)"),
    status_filter: Optional[str] = Query(None, alias="status", description="Filter by status (admin only)"),
    db: AsyncSession = Depends(get_db),
    current_user: Optional[User] = Depends(get_optional_user),
) -> PaginatedResponse[CourseListResponse]:
    """
    List courses with pagination and filtering.
    
    - **skip**: Number of records to skip
    - **limit**: Maximum records to return
    - **featured**: Filter featured courses
    - **category**: Filter by category slug
    - **level**: Filter by level
    - **status**: Filter by status (admin only)
    """
    # Non-admins can only see published courses
    if current_user is None or current_user.role != "admin":
        courses = await course_crud.get_published(
            db, skip=skip, limit=limit, featured=featured, category_slug=category, level=level
        )
        total = await course_crud.count_published(db)
    else:
        # Admin can see all courses
        filters = {}
        if status_filter:
            filters["status"] = status_filter
        if featured is not None:
            filters["featured"] = featured
        if level:
            filters["level"] = level

        courses = await course_crud.get_multi(
            db,
            skip=skip,
            limit=limit,
            filters=filters,
            order_by="created_at",
            order_desc=True,
            category_slug=category,
        )
        total = await course_crud.count(db, filters=filters)

    page = (skip // limit) + 1
    pages = (total + limit - 1) // limit
    return PaginatedResponse(
        data=[CourseListResponse.model_validate(c) for c in courses],
        pagination=PaginationMeta(total=total, page=page, per_page=limit, pages=pages)
    )


@router.get("/{slug}", response_model=CourseResponse)
async def get_course(
    slug: str,
    db: AsyncSession = Depends(get_db),
    current_user: Optional[User] = Depends(get_optional_user),
) -> CourseResponse:
    """Get a single course by slug."""
    course = await course_crud.get_by_slug(db, slug=slug)
    if not course:
        raise NotFoundError("Course")

    # Non-admins can only see published courses
    if (current_user is None or current_user.role != "admin") and course.status != "published":
        raise NotFoundError("Course")

    return CourseResponse.model_validate(course)


@router.post("/", response_model=CourseResponse, status_code=status.HTTP_201_CREATED)
async def create_course(
    course_in: CourseCreate,
    db: AsyncSession = Depends(get_db),
    current_admin: User = Depends(get_current_admin_user),
) -> CourseResponse:
    """Create a new course (admin only)."""
    # Check slug uniqueness
    existing = await course_crud.get_by_slug(db, slug=course_in.slug)
    if existing:
        raise ConflictError("Course with this slug already exists")

    # Verify category exists
    category = await course_category_crud.get(db, id=course_in.category_id)
    if not category:
        raise ValidationError("Invalid category_id")

    course = await course_crud.create(db, obj_in=course_in)
    return CourseResponse.model_validate(course)


@router.put("/{course_id}", response_model=CourseResponse)
async def update_course(
    course_id: int,
    course_in: CourseUpdate,
    db: AsyncSession = Depends(get_db),
    current_admin: User = Depends(get_current_admin_user),
) -> CourseResponse:
    """Update a course (admin only)."""
    course = await course_crud.get_with_relations(db, id=course_id)
    if not course:
        raise NotFoundError("Course")

    # Check slug uniqueness if changing
    if course_in.slug and course_in.slug != course.slug:
        existing = await course_crud.get_by_slug(db, slug=course_in.slug)
        if existing:
            raise ConflictError("Course with this slug already exists")

    # Verify category exists if changing
    if course_in.category_id and course_in.category_id != course.category_id:
        category = await course_category_crud.get(db, id=course_in.category_id)
        if not category:
            raise ValidationError("Invalid category_id")

    course = await course_crud.update(db, db_obj=course, obj_in=course_in)
    return CourseResponse.model_validate(course)


@router.delete("/{course_id}", response_model=MessageResponse)
async def delete_course(
    course_id: int,
    db: AsyncSession = Depends(get_db),
    current_admin: User = Depends(get_current_admin_user),
) -> MessageResponse:
    """Delete a course (admin only)."""
    course = await course_crud.get(db, id=course_id)
    if not course:
        raise NotFoundError("Course")

    await course_crud.delete(db, id=course_id)
    return MessageResponse(message="Course deleted successfully")


# ----- Course Enrollments -----

@router.get("/enrollments/", response_model=PaginatedResponse[CourseEnrollmentListResponse])
async def list_enrollments(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=50),
    status_filter: Optional[str] = Query(None, alias="status"),
    course_id: Optional[int] = Query(None),
    assigned_to: Optional[str] = Query(None),
    db: AsyncSession = Depends(get_db),
    current_admin: User = Depends(get_current_admin_user),
) -> PaginatedResponse[CourseEnrollmentListResponse]:
    """List course enrollments (admin only)."""
    enrollments = await course_enrollment_crud.get_multi(
        db,
        skip=skip,
        limit=limit,
        status=status_filter,
        course_id=course_id,
        assigned_to=assigned_to,
    )
    total = await course_enrollment_crud.count(db)

    items = []
    for e in enrollments:
        item = CourseEnrollmentListResponse(
            id=e.id,
            name=e.name,
            email=e.email,
            phone=e.phone,
            course_id=e.course_id,
            course_title=e.course.title if e.course else None,
            status=e.status,
            source=e.source,
            assigned_to=e.assigned_to,
            next_followup_at=e.next_followup_at,
            created_at=e.created_at,
        )
        items.append(item)

    page = (skip // limit) + 1
    pages = (total + limit - 1) // limit
    return PaginatedResponse(
        data=items,
        pagination=PaginationMeta(total=total, page=page, per_page=limit, pages=pages)
    )


@router.get("/enrollments/stats")
async def get_enrollment_stats(
    db: AsyncSession = Depends(get_db),
    current_admin: User = Depends(get_current_admin_user),
) -> dict:
    """Get enrollment statistics (admin only)."""
    stats = await course_enrollment_crud.count_by_status(db)
    total = sum(stats.values())
    return {
        "total": total,
        "by_status": stats,
    }


@router.get("/enrollments/{enrollment_id}", response_model=CourseEnrollmentResponse)
async def get_enrollment(
    enrollment_id: int,
    db: AsyncSession = Depends(get_db),
    current_admin: User = Depends(get_current_admin_user),
) -> CourseEnrollmentResponse:
    """Get a single enrollment by ID (admin only)."""
    enrollment = await course_enrollment_crud.get_with_course(db, id=enrollment_id)
    if not enrollment:
        raise NotFoundError("Enrollment")
    return CourseEnrollmentResponse.model_validate(enrollment)


@router.post("/enrollments/", response_model=CourseEnrollmentResponse, status_code=status.HTTP_201_CREATED)
async def create_enrollment(
    enrollment_in: CourseEnrollmentCreate,
    db: AsyncSession = Depends(get_db),
) -> CourseEnrollmentResponse:
    """
    Create a new course enrollment/inquiry.
    This is a public endpoint for the training enquiry form.
    """
    # Verify course exists if provided
    if enrollment_in.course_id:
        course = await course_crud.get(db, id=enrollment_in.course_id)
        if not course:
            raise ValidationError("Invalid course_id")

    enrollment = await course_enrollment_crud.create(db, obj_in=enrollment_in)
    return CourseEnrollmentResponse.model_validate(enrollment)


@router.put("/enrollments/{enrollment_id}", response_model=CourseEnrollmentResponse)
async def update_enrollment(
    enrollment_id: int,
    enrollment_in: CourseEnrollmentUpdate,
    db: AsyncSession = Depends(get_db),
    current_admin: User = Depends(get_current_admin_user),
) -> CourseEnrollmentResponse:
    """Update a course enrollment (admin only)."""
    enrollment = await course_enrollment_crud.get_with_course(db, id=enrollment_id)
    if not enrollment:
        raise NotFoundError("Enrollment")

    enrollment = await course_enrollment_crud.update(db, db_obj=enrollment, obj_in=enrollment_in)
    return CourseEnrollmentResponse.model_validate(enrollment)


@router.delete("/enrollments/{enrollment_id}", response_model=MessageResponse)
async def delete_enrollment(
    enrollment_id: int,
    db: AsyncSession = Depends(get_db),
    current_admin: User = Depends(get_current_admin_user),
) -> MessageResponse:
    """Delete a course enrollment (admin only)."""
    enrollment = await course_enrollment_crud.get(db, id=enrollment_id)
    if not enrollment:
        raise NotFoundError("Enrollment")

    await course_enrollment_crud.delete(db, id=enrollment_id)
    return MessageResponse(message="Enrollment deleted successfully")

