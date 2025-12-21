"""CRUD operations for app settings."""
from typing import Optional, Sequence

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.app_setting import AppSetting
from app.schemas.app_setting import AppSettingCreate


class AppSettingCRUD:
    """CRUD operations for app settings."""

    async def get_all(
        self,
        db: AsyncSession,
        category: Optional[str] = None,
    ) -> Sequence[AppSetting]:
        """Get all app settings, optionally filtered by category."""
        query = select(AppSetting).options(
            selectinload(AppSetting.updated_by)
        ).order_by(AppSetting.category, AppSetting.display_order)
        
        if category:
            query = query.where(AppSetting.category == category)
        
        result = await db.execute(query)
        return result.scalars().all()

    async def get_by_key(
        self,
        db: AsyncSession,
        key: str,
    ) -> Optional[AppSetting]:
        """Get a setting by key."""
        query = select(AppSetting).options(
            selectinload(AppSetting.updated_by)
        ).where(AppSetting.key == key)
        
        result = await db.execute(query)
        return result.scalar_one_or_none()

    async def get_value(
        self,
        db: AsyncSession,
        key: str,
        default: Optional[str] = None,
    ) -> Optional[str]:
        """Get just the value of a setting."""
        setting = await self.get_by_key(db, key)
        return setting.value if setting else default

    async def update_value(
        self,
        db: AsyncSession,
        key: str,
        value: Optional[str],
        updated_by_id: Optional[int] = None,
    ) -> Optional[AppSetting]:
        """Update a setting value."""
        stmt = (
            update(AppSetting)
            .where(AppSetting.key == key)
            .values(value=value, updated_by_id=updated_by_id)
        )
        await db.execute(stmt)
        await db.commit()
        
        return await self.get_by_key(db, key)

    async def create(
        self,
        db: AsyncSession,
        obj_in: AppSettingCreate,
    ) -> AppSetting:
        """Create a new setting."""
        setting = AppSetting(**obj_in.model_dump())
        db.add(setting)
        await db.commit()
        await db.refresh(setting)
        return setting

    async def get_categories(
        self,
        db: AsyncSession,
    ) -> list[str]:
        """Get all unique categories."""
        query = select(AppSetting.category).distinct().order_by(AppSetting.category)
        result = await db.execute(query)
        return [row[0] for row in result.all()]

    async def get_by_category(
        self,
        db: AsyncSession,
        category: str,
    ) -> Sequence[AppSetting]:
        """Get all settings in a category."""
        query = (
            select(AppSetting)
            .options(selectinload(AppSetting.updated_by))
            .where(AppSetting.category == category)
            .order_by(AppSetting.display_order)
        )
        result = await db.execute(query)
        return result.scalars().all()


# Global instance
app_setting_crud = AppSettingCRUD()


# Helper function for easy access
async def get_setting(db: AsyncSession, key: str, default: Optional[str] = None) -> Optional[str]:
    """Convenience function to get a setting value."""
    return await app_setting_crud.get_value(db, key, default)

