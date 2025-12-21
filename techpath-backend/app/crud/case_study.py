"""Case Study CRUD operations."""
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.crud.base import CRUDBase
from app.models.case_study import CaseStudy, CaseStudyTag
from app.schemas.case_study import CaseStudyCreate, CaseStudyUpdate, CaseStudyTagCreate


class CRUDCaseStudyTag(CRUDBase[CaseStudyTag, CaseStudyTagCreate, CaseStudyTagCreate]):
    """CRUD operations for CaseStudyTag model."""

    async def get_by_slug(self, db: AsyncSession, slug: str) -> Optional[CaseStudyTag]:
        """Get tag by slug."""
        result = await db.execute(select(CaseStudyTag).where(CaseStudyTag.slug == slug))
        return result.scalar_one_or_none()

    async def get_or_create(
        self, db: AsyncSession, *, name: str, slug: str
    ) -> CaseStudyTag:
        """Get existing tag or create new one."""
        tag = await self.get_by_slug(db, slug=slug)
        if tag:
            return tag

        tag = CaseStudyTag(name=name, slug=slug)
        db.add(tag)
        await db.flush()
        await db.refresh(tag)
        return tag


class CRUDCaseStudy(CRUDBase[CaseStudy, CaseStudyCreate, CaseStudyUpdate]):
    """CRUD operations for CaseStudy model."""

    async def get_multi(
        self,
        db: AsyncSession,
        *,
        skip: int = 0,
        limit: int = 100,
        order_by: Optional[str] = None,
        order_desc: bool = False,
        filters: Optional[Dict[str, Any]] = None,
    ) -> List[CaseStudy]:
        """Get multiple case studies with tags eagerly loaded."""
        query = select(CaseStudy).options(selectinload(CaseStudy.tags))

        # Apply filters
        if filters:
            for field, value in filters.items():
                if hasattr(CaseStudy, field) and value is not None:
                    query = query.where(getattr(CaseStudy, field) == value)

        # Apply ordering
        if order_by and hasattr(CaseStudy, order_by):
            order_column = getattr(CaseStudy, order_by)
            query = query.order_by(order_column.desc() if order_desc else order_column)

        # Apply pagination
        query = query.offset(skip).limit(limit)

        result = await db.execute(query)
        return list(result.scalars().all())

    async def get_by_slug(self, db: AsyncSession, slug: str) -> Optional[CaseStudy]:
        """Get case study by slug with tags loaded."""
        result = await db.execute(
            select(CaseStudy)
            .where(CaseStudy.slug == slug)
            .options(selectinload(CaseStudy.tags))
        )
        return result.scalar_one_or_none()

    async def get_with_tags(self, db: AsyncSession, id: int) -> Optional[CaseStudy]:
        """Get case study by ID with tags loaded."""
        result = await db.execute(
            select(CaseStudy)
            .where(CaseStudy.id == id)
            .options(selectinload(CaseStudy.tags))
        )
        return result.scalar_one_or_none()

    async def get_published(
        self,
        db: AsyncSession,
        *,
        skip: int = 0,
        limit: int = 10,
        featured: Optional[bool] = None,
        industry: Optional[str] = None,
        tag_slug: Optional[str] = None,
    ) -> List[CaseStudy]:
        """Get published case studies with optional filters."""
        query = (
            select(CaseStudy)
            .where(CaseStudy.status == "published")
            .options(selectinload(CaseStudy.tags))
        )

        if featured is not None:
            query = query.where(CaseStudy.featured == featured)

        if industry:
            query = query.where(CaseStudy.industry == industry)

        if tag_slug:
            query = query.join(CaseStudy.tags).where(CaseStudyTag.slug == tag_slug)

        query = query.order_by(CaseStudy.published_at.desc())
        query = query.offset(skip).limit(limit)

        result = await db.execute(query)
        return list(result.scalars().unique().all())

    async def create(
        self, db: AsyncSession, *, obj_in: CaseStudyCreate, author_id: Optional[int] = None
    ) -> CaseStudy:
        """Create a new case study."""
        obj_data = obj_in.model_dump(exclude={"tag_ids"})
        obj_data["author_id"] = author_id

        # Set published_at if status is published
        if obj_data.get("status") == "published" and not obj_data.get("published_at"):
            obj_data["published_at"] = datetime.now(timezone.utc)

        db_obj = CaseStudy(**obj_data)
        db.add(db_obj)
        await db.flush()

        # Add tags if provided
        if obj_in.tag_ids:
            for tag_id in obj_in.tag_ids:
                result = await db.execute(select(CaseStudyTag).where(CaseStudyTag.id == tag_id))
                tag = result.scalar_one_or_none()
                if tag:
                    db_obj.tags.append(tag)

        await db.commit()
        
        # Reload with tags eagerly loaded
        return await self.get_with_tags(db, id=db_obj.id)

    async def update(
        self, db: AsyncSession, *, db_obj: CaseStudy, obj_in: CaseStudyUpdate
    ) -> CaseStudy:
        """Update a case study."""
        update_data = obj_in.model_dump(exclude={"tag_ids"}, exclude_unset=True)

        # Set published_at if status changed to published
        if update_data.get("status") == "published" and not db_obj.published_at:
            update_data["published_at"] = datetime.now(timezone.utc)

        for field, value in update_data.items():
            setattr(db_obj, field, value)

        # Update tags if provided
        if obj_in.tag_ids is not None:
            db_obj.tags.clear()
            for tag_id in obj_in.tag_ids:
                result = await db.execute(select(CaseStudyTag).where(CaseStudyTag.id == tag_id))
                tag = result.scalar_one_or_none()
                if tag:
                    db_obj.tags.append(tag)

        db.add(db_obj)
        await db.flush()
        await db.refresh(db_obj)
        return db_obj


case_study_tag_crud = CRUDCaseStudyTag(CaseStudyTag)
case_study_crud = CRUDCaseStudy(CaseStudy)

