"""Base CRUD operations class."""
from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union

from pydantic import BaseModel
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.base import Base

ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    """Base class for CRUD operations."""

    def __init__(self, model: Type[ModelType]) -> None:
        """Initialize CRUD with a model class."""
        self.model = model

    async def get(self, db: AsyncSession, id: int) -> Optional[ModelType]:
        """Get a single record by ID."""
        result = await db.execute(select(self.model).where(self.model.id == id))
        return result.scalar_one_or_none()

    async def get_by_field(
        self, db: AsyncSession, field: str, value: Any
    ) -> Optional[ModelType]:
        """Get a single record by a specific field."""
        result = await db.execute(
            select(self.model).where(getattr(self.model, field) == value)
        )
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
    ) -> List[ModelType]:
        """Get multiple records with pagination and optional filtering."""
        query = select(self.model)

        # Apply filters
        if filters:
            for field, value in filters.items():
                if hasattr(self.model, field) and value is not None:
                    query = query.where(getattr(self.model, field) == value)

        # Apply ordering
        if order_by and hasattr(self.model, order_by):
            order_column = getattr(self.model, order_by)
            query = query.order_by(order_column.desc() if order_desc else order_column)

        # Apply pagination
        query = query.offset(skip).limit(limit)

        result = await db.execute(query)
        return list(result.scalars().all())

    async def count(
        self, db: AsyncSession, filters: Optional[Dict[str, Any]] = None
    ) -> int:
        """Count records with optional filtering."""
        query = select(func.count(self.model.id))

        if filters:
            for field, value in filters.items():
                if hasattr(self.model, field) and value is not None:
                    query = query.where(getattr(self.model, field) == value)

        result = await db.execute(query)
        return result.scalar() or 0

    async def create(
        self, db: AsyncSession, *, obj_in: Union[CreateSchemaType, Dict[str, Any]]
    ) -> ModelType:
        """Create a new record."""
        if isinstance(obj_in, dict):
            obj_data = obj_in
        else:
            obj_data = obj_in.model_dump(exclude_unset=True)

        db_obj = self.model(**obj_data)
        db.add(db_obj)
        await db.flush()
        await db.refresh(db_obj)
        return db_obj

    async def update(
        self,
        db: AsyncSession,
        *,
        db_obj: ModelType,
        obj_in: Union[UpdateSchemaType, Dict[str, Any]],
    ) -> ModelType:
        """Update an existing record."""
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.model_dump(exclude_unset=True)

        for field, value in update_data.items():
            if hasattr(db_obj, field):
                setattr(db_obj, field, value)

        db.add(db_obj)
        await db.flush()
        await db.refresh(db_obj)
        return db_obj

    async def delete(self, db: AsyncSession, *, id: int) -> Optional[ModelType]:
        """Delete a record by ID."""
        obj = await self.get(db, id=id)
        if obj:
            await db.delete(obj)
            await db.flush()
        return obj

