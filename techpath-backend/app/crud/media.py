"""CRUD operations for media files."""
from typing import List, Optional, Tuple

from sqlalchemy import select, func, delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.media import MediaFile, MediaFileUsage
from app.schemas.media import MediaFileCreate, MediaFileUpdate, MediaFileUsageCreate


class MediaFileCRUD:
    """CRUD operations for MediaFile model."""

    async def get(self, db: AsyncSession, id: int) -> Optional[MediaFile]:
        """Get a media file by ID."""
        result = await db.execute(
            select(MediaFile).where(MediaFile.id == id)
        )
        return result.scalar_one_or_none()

    async def get_with_usages(self, db: AsyncSession, id: int) -> Optional[MediaFile]:
        """Get a media file by ID with usage records."""
        result = await db.execute(
            select(MediaFile)
            .options(selectinload(MediaFile.usages))
            .where(MediaFile.id == id)
        )
        return result.scalar_one_or_none()

    async def get_by_hash(self, db: AsyncSession, file_hash: str) -> Optional[MediaFile]:
        """Get a media file by its hash for deduplication."""
        result = await db.execute(
            select(MediaFile).where(MediaFile.file_hash == file_hash)
        )
        return result.scalar_one_or_none()

    async def get_by_path(self, db: AsyncSession, stored_path: str) -> Optional[MediaFile]:
        """Get a media file by its stored path."""
        result = await db.execute(
            select(MediaFile).where(MediaFile.stored_path == stored_path)
        )
        return result.scalar_one_or_none()

    async def get_multi(
        self,
        db: AsyncSession,
        skip: int = 0,
        limit: int = 20,
        content_type: Optional[str] = None,
        search: Optional[str] = None,
    ) -> Tuple[List[MediaFile], int]:
        """Get multiple media files with pagination and filtering."""
        query = select(MediaFile)

        # Apply filters
        if content_type:
            if content_type == "image":
                query = query.where(MediaFile.content_type.like("image/%"))
            elif content_type == "document":
                query = query.where(
                    MediaFile.content_type.in_([
                        "application/pdf",
                        "application/msword",
                        "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                        "text/plain",
                    ])
                )
            else:
                query = query.where(MediaFile.content_type == content_type)

        if search:
            query = query.where(MediaFile.filename.ilike(f"%{search}%"))

        # Get total count
        count_query = select(func.count()).select_from(query.subquery())
        total_result = await db.execute(count_query)
        total = total_result.scalar() or 0

        # Apply pagination and ordering
        query = query.order_by(MediaFile.created_at.desc()).offset(skip).limit(limit)

        result = await db.execute(query)
        files = list(result.scalars().all())

        return files, total

    async def create(self, db: AsyncSession, obj_in: MediaFileCreate) -> MediaFile:
        """Create a new media file record."""
        db_obj = MediaFile(
            filename=obj_in.filename,
            stored_path=obj_in.stored_path,
            file_hash=obj_in.file_hash,
            content_type=obj_in.content_type,
            size=obj_in.size,
            width=obj_in.width,
            height=obj_in.height,
            alt_text=obj_in.alt_text,
        )
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def update(
        self, db: AsyncSession, db_obj: MediaFile, obj_in: MediaFileUpdate
    ) -> MediaFile:
        """Update a media file record."""
        update_data = obj_in.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_obj, field, value)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def delete(self, db: AsyncSession, id: int) -> bool:
        """Delete a media file record."""
        result = await db.execute(delete(MediaFile).where(MediaFile.id == id))
        await db.commit()
        return result.rowcount > 0

    async def get_usage_count(self, db: AsyncSession, id: int) -> int:
        """Get the number of usages for a media file."""
        result = await db.execute(
            select(func.count())
            .select_from(MediaFileUsage)
            .where(MediaFileUsage.file_id == id)
        )
        return result.scalar() or 0

    async def is_in_use(self, db: AsyncSession, id: int) -> bool:
        """Check if a media file is being used anywhere."""
        count = await self.get_usage_count(db, id)
        return count > 0


class MediaFileUsageCRUD:
    """CRUD operations for MediaFileUsage model."""

    async def get(self, db: AsyncSession, id: int) -> Optional[MediaFileUsage]:
        """Get a usage record by ID."""
        result = await db.execute(
            select(MediaFileUsage).where(MediaFileUsage.id == id)
        )
        return result.scalar_one_or_none()

    async def get_by_entity(
        self,
        db: AsyncSession,
        entity_type: str,
        entity_id: int,
        field_name: Optional[str] = None,
    ) -> List[MediaFileUsage]:
        """Get all usage records for an entity."""
        query = select(MediaFileUsage).where(
            MediaFileUsage.entity_type == entity_type,
            MediaFileUsage.entity_id == entity_id,
        )
        if field_name:
            query = query.where(MediaFileUsage.field_name == field_name)

        result = await db.execute(query)
        return list(result.scalars().all())

    async def get_by_file(self, db: AsyncSession, file_id: int) -> List[MediaFileUsage]:
        """Get all usage records for a file."""
        result = await db.execute(
            select(MediaFileUsage)
            .where(MediaFileUsage.file_id == file_id)
            .order_by(MediaFileUsage.created_at.desc())
        )
        return list(result.scalars().all())

    async def create(
        self, db: AsyncSession, file_id: int, obj_in: MediaFileUsageCreate
    ) -> MediaFileUsage:
        """Create a new usage record."""
        db_obj = MediaFileUsage(
            file_id=file_id,
            entity_type=obj_in.entity_type,
            entity_id=obj_in.entity_id,
            field_name=obj_in.field_name,
        )
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def delete(self, db: AsyncSession, id: int) -> bool:
        """Delete a usage record."""
        result = await db.execute(
            delete(MediaFileUsage).where(MediaFileUsage.id == id)
        )
        await db.commit()
        return result.rowcount > 0

    async def delete_by_entity(
        self,
        db: AsyncSession,
        entity_type: str,
        entity_id: int,
        field_name: Optional[str] = None,
    ) -> int:
        """Delete all usage records for an entity."""
        query = delete(MediaFileUsage).where(
            MediaFileUsage.entity_type == entity_type,
            MediaFileUsage.entity_id == entity_id,
        )
        if field_name:
            query = query.where(MediaFileUsage.field_name == field_name)

        result = await db.execute(query)
        await db.commit()
        return result.rowcount

    async def find_existing(
        self,
        db: AsyncSession,
        file_id: int,
        entity_type: str,
        entity_id: int,
        field_name: str,
    ) -> Optional[MediaFileUsage]:
        """Find an existing usage record."""
        result = await db.execute(
            select(MediaFileUsage).where(
                MediaFileUsage.file_id == file_id,
                MediaFileUsage.entity_type == entity_type,
                MediaFileUsage.entity_id == entity_id,
                MediaFileUsage.field_name == field_name,
            )
        )
        return result.scalar_one_or_none()


# Singleton instances
media_file_crud = MediaFileCRUD()
media_usage_crud = MediaFileUsageCRUD()

