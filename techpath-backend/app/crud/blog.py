"""Blog CRUD operations."""
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.crud.base import CRUDBase
from app.models.blog import BlogPost, BlogTag
from app.schemas.blog import BlogPostCreate, BlogPostUpdate, BlogTagCreate


class CRUDBlogTag(CRUDBase[BlogTag, BlogTagCreate, BlogTagCreate]):
    """CRUD operations for BlogTag model."""

    async def get_by_slug(self, db: AsyncSession, slug: str) -> Optional[BlogTag]:
        """Get tag by slug."""
        result = await db.execute(select(BlogTag).where(BlogTag.slug == slug))
        return result.scalar_one_or_none()

    async def get_or_create(
        self, db: AsyncSession, *, name: str, slug: str
    ) -> BlogTag:
        """Get existing tag or create new one."""
        tag = await self.get_by_slug(db, slug=slug)
        if tag:
            return tag

        tag = BlogTag(name=name, slug=slug)
        db.add(tag)
        await db.flush()
        await db.refresh(tag)
        return tag


class CRUDBlogPost(CRUDBase[BlogPost, BlogPostCreate, BlogPostUpdate]):
    """CRUD operations for BlogPost model."""

    async def get_multi(
        self,
        db: AsyncSession,
        *,
        skip: int = 0,
        limit: int = 100,
        order_by: Optional[str] = None,
        order_desc: bool = False,
        filters: Optional[Dict[str, Any]] = None,
    ) -> List[BlogPost]:
        """Get multiple posts with tags eagerly loaded."""
        query = select(BlogPost).options(selectinload(BlogPost.tags))

        # Apply filters
        if filters:
            for field, value in filters.items():
                if hasattr(BlogPost, field) and value is not None:
                    query = query.where(getattr(BlogPost, field) == value)

        # Apply ordering
        if order_by and hasattr(BlogPost, order_by):
            order_column = getattr(BlogPost, order_by)
            query = query.order_by(order_column.desc() if order_desc else order_column)

        # Apply pagination
        query = query.offset(skip).limit(limit)

        result = await db.execute(query)
        return list(result.scalars().all())

    async def get_by_slug(self, db: AsyncSession, slug: str) -> Optional[BlogPost]:
        """Get post by slug with tags loaded."""
        result = await db.execute(
            select(BlogPost)
            .where(BlogPost.slug == slug)
            .options(selectinload(BlogPost.tags))
        )
        return result.scalar_one_or_none()

    async def get_with_tags(self, db: AsyncSession, id: int) -> Optional[BlogPost]:
        """Get post by ID with tags loaded."""
        result = await db.execute(
            select(BlogPost)
            .where(BlogPost.id == id)
            .options(selectinload(BlogPost.tags))
        )
        return result.scalar_one_or_none()

    async def get_published(
        self,
        db: AsyncSession,
        *,
        skip: int = 0,
        limit: int = 10,
        featured: Optional[bool] = None,
        tag_slug: Optional[str] = None,
    ) -> List[BlogPost]:
        """Get published posts with optional filters."""
        query = (
            select(BlogPost)
            .where(BlogPost.status == "published")
            .options(selectinload(BlogPost.tags))
        )

        if featured is not None:
            query = query.where(BlogPost.featured == featured)

        if tag_slug:
            query = query.join(BlogPost.tags).where(BlogTag.slug == tag_slug)

        query = query.order_by(BlogPost.published_at.desc())
        query = query.offset(skip).limit(limit)

        result = await db.execute(query)
        return list(result.scalars().unique().all())

    async def create(
        self, db: AsyncSession, *, obj_in: BlogPostCreate, author_id: Optional[int] = None
    ) -> BlogPost:
        """Create a new blog post."""
        obj_data = obj_in.model_dump(exclude={"tag_ids"})
        obj_data["author_id"] = author_id

        # Set published_at if status is published
        if obj_data.get("status") == "published" and not obj_data.get("published_at"):
            obj_data["published_at"] = datetime.now(timezone.utc)

        db_obj = BlogPost(**obj_data)
        db.add(db_obj)
        await db.flush()

        # Add tags if provided
        if obj_in.tag_ids:
            for tag_id in obj_in.tag_ids:
                result = await db.execute(select(BlogTag).where(BlogTag.id == tag_id))
                tag = result.scalar_one_or_none()
                if tag:
                    db_obj.tags.append(tag)

        await db.commit()
        
        # Reload with tags eagerly loaded
        return await self.get_with_tags(db, id=db_obj.id)

    async def update(
        self, db: AsyncSession, *, db_obj: BlogPost, obj_in: BlogPostUpdate
    ) -> BlogPost:
        """Update a blog post."""
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
                result = await db.execute(select(BlogTag).where(BlogTag.id == tag_id))
                tag = result.scalar_one_or_none()
                if tag:
                    db_obj.tags.append(tag)

        db.add(db_obj)
        await db.flush()
        await db.refresh(db_obj)
        return db_obj


blog_tag_crud = CRUDBlogTag(BlogTag)
blog_crud = CRUDBlogPost(BlogPost)

