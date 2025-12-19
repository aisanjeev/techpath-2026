"""CRUD operations for secret metadata."""
from typing import Optional, Sequence

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.secret import SecretMetadata


class SecretMetadataCRUD:
    """CRUD operations for secret metadata."""

    async def get_all(
        self,
        db: AsyncSession,
        category: Optional[str] = None,
    ) -> Sequence[SecretMetadata]:
        """
        Get all secret metadata, optionally filtered by category.
        
        Args:
            db: Database session
            category: Optional category filter
            
        Returns:
            List of SecretMetadata records
        """
        query = select(SecretMetadata).options(
            selectinload(SecretMetadata.updated_by)
        ).order_by(SecretMetadata.category, SecretMetadata.display_order)
        
        if category:
            query = query.where(SecretMetadata.category == category)
        
        result = await db.execute(query)
        return result.scalars().all()

    async def get_by_key(
        self,
        db: AsyncSession,
        key_name: str,
    ) -> Optional[SecretMetadata]:
        """
        Get secret metadata by key name.
        
        Args:
            db: Database session
            key_name: The key name to look up
            
        Returns:
            SecretMetadata or None if not found
        """
        query = select(SecretMetadata).options(
            selectinload(SecretMetadata.updated_by)
        ).where(SecretMetadata.key_name == key_name)
        
        result = await db.execute(query)
        return result.scalar_one_or_none()

    async def get_by_id(
        self,
        db: AsyncSession,
        secret_id: int,
    ) -> Optional[SecretMetadata]:
        """
        Get secret metadata by ID.
        
        Args:
            db: Database session
            secret_id: The secret ID
            
        Returns:
            SecretMetadata or None if not found
        """
        query = select(SecretMetadata).options(
            selectinload(SecretMetadata.updated_by)
        ).where(SecretMetadata.id == secret_id)
        
        result = await db.execute(query)
        return result.scalar_one_or_none()

    async def update_is_set(
        self,
        db: AsyncSession,
        key_name: str,
        is_set: bool,
        updated_by_id: Optional[int] = None,
    ) -> Optional[SecretMetadata]:
        """
        Update the is_set flag for a secret.
        
        Args:
            db: Database session
            key_name: The key name
            is_set: Whether the secret is set in Key Vault
            updated_by_id: User ID who made the update
            
        Returns:
            Updated SecretMetadata or None if not found
        """
        stmt = (
            update(SecretMetadata)
            .where(SecretMetadata.key_name == key_name)
            .values(is_set=is_set, updated_by_id=updated_by_id)
        )
        await db.execute(stmt)
        await db.commit()
        
        return await self.get_by_key(db, key_name)

    async def get_categories(
        self,
        db: AsyncSession,
    ) -> list[str]:
        """
        Get all unique categories.
        
        Args:
            db: Database session
            
        Returns:
            List of category names
        """
        query = select(SecretMetadata.category).distinct().order_by(SecretMetadata.category)
        result = await db.execute(query)
        return [row[0] for row in result.all()]

    async def get_by_category(
        self,
        db: AsyncSession,
        category: str,
    ) -> Sequence[SecretMetadata]:
        """
        Get all secrets in a category.
        
        Args:
            db: Database session
            category: Category name
            
        Returns:
            List of SecretMetadata in the category
        """
        query = (
            select(SecretMetadata)
            .options(selectinload(SecretMetadata.updated_by))
            .where(SecretMetadata.category == category)
            .order_by(SecretMetadata.display_order)
        )
        result = await db.execute(query)
        return result.scalars().all()

    async def get_required_unset(
        self,
        db: AsyncSession,
    ) -> Sequence[SecretMetadata]:
        """
        Get all required secrets that are not set.
        
        Args:
            db: Database session
            
        Returns:
            List of required but unset secrets
        """
        query = (
            select(SecretMetadata)
            .where(SecretMetadata.is_required == True)  # noqa: E712
            .where(SecretMetadata.is_set == False)  # noqa: E712
            .order_by(SecretMetadata.category, SecretMetadata.display_order)
        )
        result = await db.execute(query)
        return result.scalars().all()


# Global instance
secret_metadata_crud = SecretMetadataCRUD()

