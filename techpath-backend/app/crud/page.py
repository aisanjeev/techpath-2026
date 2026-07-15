"""CRUD operations for standalone CMS pages."""
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

from sqlalchemy import case, func, or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models.page import Page
from app.schemas.page import PageCreate, PageUpdate


class CRUDPage(CRUDBase[Page, PageCreate, PageUpdate]):
    """CRUD operations for the Page model."""

    async def get_by_slug(self, db: AsyncSession, slug: str) -> Optional[Page]:
        """Get a page by its slug."""
        result = await db.execute(select(Page).where(Page.slug == slug))
        return result.scalar_one_or_none()

    async def get_multi(
        self,
        db: AsyncSession,
        *,
        skip: int = 0,
        limit: int = 100,
        order_by: Optional[str] = None,
        order_desc: bool = False,
        filters: Optional[Dict[str, Any]] = None,
        search: Optional[str] = None,
    ) -> List[Page]:
        """List pages with optional search + filters."""
        query = select(Page)

        if filters:
            for field, value in filters.items():
                if hasattr(Page, field) and value is not None:
                    query = query.where(getattr(Page, field) == value)

        if search:
            like = f"%{search}%"
            query = query.where(or_(Page.title.ilike(like), Page.slug.ilike(like)))

        if order_by and hasattr(Page, order_by):
            col = getattr(Page, order_by)
            query = query.order_by(col.desc() if order_desc else col)

        query = query.offset(skip).limit(limit)
        result = await db.execute(query)
        return list(result.scalars().all())

    async def get_multi_count(
        self,
        db: AsyncSession,
        *,
        filters: Optional[Dict[str, Any]] = None,
        search: Optional[str] = None,
    ) -> int:
        """Count pages matching filters + search."""
        query = select(func.count()).select_from(Page)
        if filters:
            for field, value in filters.items():
                if hasattr(Page, field) and value is not None:
                    query = query.where(getattr(Page, field) == value)
        if search:
            like = f"%{search}%"
            query = query.where(or_(Page.title.ilike(like), Page.slug.ilike(like)))
        result = await db.execute(query)
        return result.scalar() or 0

    async def get_published(
        self,
        db: AsyncSession,
        *,
        skip: int = 0,
        limit: int = 50,
    ) -> List[Page]:
        """Fetch published pages whose published_at is null or in the past."""
        now = datetime.now(timezone.utc).replace(tzinfo=None)
        query = (
            select(Page)
            .where(Page.status == "published")
            .where(or_(Page.published_at.is_(None), Page.published_at <= now))
            .order_by(
                case((Page.published_at.is_(None), 1), else_=0),
                Page.published_at.desc(),
                Page.updated_at.desc(),
            )
            .offset(skip)
            .limit(limit)
        )
        result = await db.execute(query)
        return list(result.scalars().all())

    async def get_published_count(self, db: AsyncSession) -> int:
        """Count pages visible to public."""
        now = datetime.now(timezone.utc).replace(tzinfo=None)
        query = (
            select(func.count())
            .select_from(Page)
            .where(Page.status == "published")
            .where(or_(Page.published_at.is_(None), Page.published_at <= now))
        )
        result = await db.execute(query)
        return result.scalar() or 0

    async def create(
        self, db: AsyncSession, *, obj_in: PageCreate, author_id: Optional[int] = None
    ) -> Page:
        """Create a page, setting author + auto-filling published_at on publish."""
        obj_data = obj_in.model_dump()
        obj_data["author_id"] = author_id

        if obj_data.get("status") == "published" and not obj_data.get("published_at"):
            obj_data["published_at"] = datetime.now(timezone.utc).replace(tzinfo=None)

        db_obj = Page(**obj_data)
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def update(
        self, db: AsyncSession, *, db_obj: Page, obj_in: PageUpdate
    ) -> Page:
        """Update a page; auto-fill published_at when flipping to published."""
        update_data = obj_in.model_dump(exclude_unset=True)

        if (
            update_data.get("status") == "published"
            and not db_obj.published_at
            and not update_data.get("published_at")
        ):
            update_data["published_at"] = datetime.now(timezone.utc).replace(tzinfo=None)

        for field, value in update_data.items():
            setattr(db_obj, field, value)

        db.add(db_obj)
        await db.flush()
        await db.refresh(db_obj)
        return db_obj


page_crud = CRUDPage(Page)
