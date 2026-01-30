"""
CRUD operations for Course, CourseCategory, CourseEnrollment, and Skill models.
"""

import json
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.crud.base import CRUDBase
from app.models.course import Course, CourseCategory, CourseEnrollment, Skill
from app.schemas.course import (
    CourseCategoryCreate,
    CourseCategoryUpdate,
    CourseCreate,
    CourseEnrollmentCreate,
    CourseEnrollmentUpdate,
    CourseUpdate,
    SkillCreate,
)


class CRUDSkill(CRUDBase[Skill, SkillCreate, SkillCreate]):
    """CRUD operations for Skill model."""

    async def get_by_slug(self, db: AsyncSession, slug: str) -> Optional[Skill]:
        """Get skill by slug."""
        result = await db.execute(select(Skill).where(Skill.slug == slug))
        return result.scalar_one_or_none()

    async def get_or_create(self, db: AsyncSession, *, name: str, slug: str) -> Skill:
        """Get existing skill or create new one."""
        skill = await self.get_by_slug(db, slug=slug)
        if skill:
            return skill

        skill = Skill(name=name, slug=slug)
        db.add(skill)
        await db.flush()
        await db.refresh(skill)
        return skill


class CRUDCourseCategory(CRUDBase[CourseCategory, CourseCategoryCreate, CourseCategoryUpdate]):
    """CRUD operations for CourseCategory model."""

    async def get_by_slug(self, db: AsyncSession, slug: str) -> Optional[CourseCategory]:
        """Get category by slug."""
        result = await db.execute(select(CourseCategory).where(CourseCategory.slug == slug))
        return result.scalar_one_or_none()

    async def get_root_categories(
        self, db: AsyncSession, *, active_only: bool = True
    ) -> List[CourseCategory]:
        """Get all root categories (no parent) with children eagerly loaded."""
        query = select(CourseCategory).where(CourseCategory.parent_id.is_(None))

        if active_only:
            query = query.where(CourseCategory.is_active == True)

        # Eagerly load children up to 2 levels
        query = query.options(
            selectinload(CourseCategory.children).selectinload(CourseCategory.children)
        ).order_by(CourseCategory.display_order, CourseCategory.name)

        result = await db.execute(query)
        return list(result.scalars().all())

    async def get_all_active(self, db: AsyncSession) -> List[CourseCategory]:
        """Get all active categories."""
        query = (
            select(CourseCategory)
            .where(CourseCategory.is_active == True)
            .order_by(CourseCategory.display_order, CourseCategory.name)
        )
        result = await db.execute(query)
        return list(result.scalars().all())

    async def get_course_count(self, db: AsyncSession, category_id: int) -> int:
        """Get the number of courses in a category."""
        result = await db.execute(
            select(func.count(Course.id)).filter(Course.category_id == category_id)
        )
        return result.scalar_one()

    async def has_courses(self, db: AsyncSession, category_id: int) -> bool:
        """Check if a category has any associated courses."""
        count = await self.get_course_count(db, category_id)
        return count > 0


class CRUDCourse(CRUDBase[Course, CourseCreate, CourseUpdate]):
    """CRUD operations for Course model."""

    def _serialize_json_fields(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Convert list/dict fields to JSON strings for storage."""
        json_fields = ['curriculum', 'learning_outcomes', 'prerequisites', 'projects', 'faqs']
        for field in json_fields:
            if field in data and data[field] is not None:
                if isinstance(data[field], (list, dict)):
                    # Convert Pydantic models to dicts
                    if data[field] and hasattr(data[field][0], 'model_dump'):
                        data[field] = json.dumps([item.model_dump() for item in data[field]])
                    else:
                        data[field] = json.dumps(data[field])
        return data

    async def get_multi(
        self,
        db: AsyncSession,
        *,
        skip: int = 0,
        limit: int = 100,
        order_by: Optional[str] = None,
        order_desc: bool = False,
        filters: Optional[Dict[str, Any]] = None,
        category_slug: Optional[str] = None,
    ) -> List[Course]:
        """Get multiple courses with skills and category eagerly loaded."""
        query = select(Course).options(
            selectinload(Course.skills),
            selectinload(Course.category)
        )

        # Apply filters
        if filters:
            for field, value in filters.items():
                if hasattr(Course, field) and value is not None:
                    query = query.where(getattr(Course, field) == value)

        if category_slug:
            query = query.join(Course.category).where(CourseCategory.slug == category_slug)

        # Apply ordering
        if order_by and hasattr(Course, order_by):
            order_column = getattr(Course, order_by)
            query = query.order_by(order_column.desc() if order_desc else order_column)
        else:
            query = query.order_by(Course.display_order if hasattr(Course, 'display_order') else Course.created_at.desc())

        # Apply pagination
        query = query.offset(skip).limit(limit)

        result = await db.execute(query)
        return list(result.scalars().all())

    async def get_by_slug(self, db: AsyncSession, slug: str) -> Optional[Course]:
        """Get course by slug with skills and category loaded."""
        result = await db.execute(
            select(Course)
            .where(Course.slug == slug)
            .options(selectinload(Course.skills), selectinload(Course.category))
        )
        return result.scalar_one_or_none()

    async def get_with_relations(self, db: AsyncSession, id: int) -> Optional[Course]:
        """Get course by ID with skills and category loaded."""
        result = await db.execute(
            select(Course)
            .where(Course.id == id)
            .options(selectinload(Course.skills), selectinload(Course.category))
        )
        return result.scalar_one_or_none()

    async def get_published(
        self,
        db: AsyncSession,
        *,
        skip: int = 0,
        limit: int = 20,
        featured: Optional[bool] = None,
        category_slug: Optional[str] = None,
        level: Optional[str] = None,
    ) -> List[Course]:
        """Get published courses with optional filters."""
        query = (
            select(Course)
            .where(Course.status == "published")
            .where(Course.is_active == True)
            .options(selectinload(Course.skills), selectinload(Course.category))
        )

        if featured is not None:
            query = query.where(Course.featured == featured)

        if category_slug:
            query = query.join(Course.category).where(CourseCategory.slug == category_slug)

        if level:
            query = query.where(Course.level == level)

        query = query.order_by(Course.featured.desc(), Course.created_at.desc())
        query = query.offset(skip).limit(limit)

        result = await db.execute(query)
        return list(result.scalars().all())

    async def create(
        self, db: AsyncSession, *, obj_in: CourseCreate
    ) -> Course:
        """Create a new course."""
        obj_data = obj_in.model_dump(exclude={"skill_ids"})
        obj_data = self._serialize_json_fields(obj_data)

        db_obj = Course(**obj_data)
        db.add(db_obj)
        await db.flush()

        # Add skills if provided
        if obj_in.skill_ids:
            for skill_id in obj_in.skill_ids:
                result = await db.execute(select(Skill).where(Skill.id == skill_id))
                skill = result.scalar_one_or_none()
                if skill:
                    db_obj.skills.append(skill)

        await db.commit()
        return await self.get_with_relations(db, id=db_obj.id)

    async def update(
        self, db: AsyncSession, *, db_obj: Course, obj_in: CourseUpdate
    ) -> Course:
        """Update a course."""
        update_data = obj_in.model_dump(exclude={"skill_ids"}, exclude_unset=True)
        update_data = self._serialize_json_fields(update_data)

        for field, value in update_data.items():
            setattr(db_obj, field, value)

        # Update skills if provided
        if obj_in.skill_ids is not None:
            db_obj.skills.clear()
            for skill_id in obj_in.skill_ids:
                result = await db.execute(select(Skill).where(Skill.id == skill_id))
                skill = result.scalar_one_or_none()
                if skill:
                    db_obj.skills.append(skill)

        db.add(db_obj)
        await db.flush()
        await db.refresh(db_obj)
        return db_obj

    async def count_published(self, db: AsyncSession) -> int:
        """Count total published courses."""
        result = await db.execute(
            select(func.count(Course.id))
            .where(Course.status == "published")
            .where(Course.is_active == True)
        )
        return result.scalar_one()


class CRUDCourseEnrollment(CRUDBase[CourseEnrollment, CourseEnrollmentCreate, CourseEnrollmentUpdate]):
    """CRUD operations for CourseEnrollment model."""

    async def get_multi(
        self,
        db: AsyncSession,
        *,
        skip: int = 0,
        limit: int = 100,
        status: Optional[str] = None,
        course_id: Optional[int] = None,
        assigned_to: Optional[str] = None,
    ) -> List[CourseEnrollment]:
        """Get multiple enrollments with optional filters."""
        query = select(CourseEnrollment).options(selectinload(CourseEnrollment.course))

        if status:
            query = query.where(CourseEnrollment.status == status)

        if course_id:
            query = query.where(CourseEnrollment.course_id == course_id)

        if assigned_to:
            query = query.where(CourseEnrollment.assigned_to == assigned_to)

        query = query.order_by(CourseEnrollment.created_at.desc())
        query = query.offset(skip).limit(limit)

        result = await db.execute(query)
        return list(result.scalars().all())

    async def get_with_course(self, db: AsyncSession, id: int) -> Optional[CourseEnrollment]:
        """Get enrollment by ID with course loaded."""
        result = await db.execute(
            select(CourseEnrollment)
            .where(CourseEnrollment.id == id)
            .options(selectinload(CourseEnrollment.course))
        )
        return result.scalar_one_or_none()

    async def get_by_email(
        self, db: AsyncSession, email: str, course_id: Optional[int] = None
    ) -> Optional[CourseEnrollment]:
        """Get enrollment by email (and optionally course)."""
        query = select(CourseEnrollment).where(CourseEnrollment.email == email)
        if course_id:
            query = query.where(CourseEnrollment.course_id == course_id)
        query = query.order_by(CourseEnrollment.created_at.desc())
        result = await db.execute(query)
        return result.scalar_one_or_none()

    async def count_by_status(self, db: AsyncSession) -> Dict[str, int]:
        """Get count of enrollments by status."""
        result = await db.execute(
            select(CourseEnrollment.status, func.count(CourseEnrollment.id))
            .group_by(CourseEnrollment.status)
        )
        return dict(result.all())

    async def get_pending_followups(
        self, db: AsyncSession, *, limit: int = 50
    ) -> List[CourseEnrollment]:
        """Get enrollments that need follow-up (next_followup_at is in the past)."""
        now = datetime.now(timezone.utc)
        query = (
            select(CourseEnrollment)
            .where(CourseEnrollment.next_followup_at <= now)
            .where(CourseEnrollment.status.in_(["new", "contacted", "interested"]))
            .options(selectinload(CourseEnrollment.course))
            .order_by(CourseEnrollment.next_followup_at)
            .limit(limit)
        )
        result = await db.execute(query)
        return list(result.scalars().all())


# Singleton instances
skill_crud = CRUDSkill(Skill)
course_category_crud = CRUDCourseCategory(CourseCategory)
course_crud = CRUDCourse(Course)
course_enrollment_crud = CRUDCourseEnrollment(CourseEnrollment)

