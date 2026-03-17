"""Service CRUD operations."""
import json
from typing import List, Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models.service import Service
from app.schemas.service import ServiceCreate, ServiceUpdate


class CRUDService(CRUDBase[Service, ServiceCreate, ServiceUpdate]):
    """CRUD operations for Service model."""

    async def get_by_slug(self, db: AsyncSession, slug: str) -> Optional[Service]:
        """Get service by slug."""
        result = await db.execute(select(Service).where(Service.slug == slug))
        return result.scalar_one_or_none()

    async def get_active(
        self,
        db: AsyncSession,
        *,
        skip: int = 0,
        limit: int = 100,
        featured: Optional[bool] = None,
    ) -> List[Service]:
        """Get active services with optional featured filter."""
        query = select(Service).where(Service.is_active == True)

        if featured is not None:
            query = query.where(Service.featured == featured)

        query = query.order_by(Service.display_order, Service.created_at.desc())
        query = query.offset(skip).limit(limit)

        result = await db.execute(query)
        return list(result.scalars().all())

    async def create(self, db: AsyncSession, *, obj_in: ServiceCreate) -> Service:
        """Create a new service, converting features, pricing_plans, and faqs to JSON."""
        obj_data = obj_in.model_dump(exclude_unset=True)

        if "features" in obj_data and obj_data["features"] is not None:
            obj_data["features"] = json.dumps(obj_data["features"])
        if "pricing_plans" in obj_data and obj_data["pricing_plans"] is not None:
            obj_data["pricing_plans"] = json.dumps(obj_data["pricing_plans"])
        if "faqs" in obj_data and obj_data["faqs"] is not None:
            obj_data["faqs"] = json.dumps(obj_data["faqs"])

        db_obj = Service(**obj_data)
        db.add(db_obj)
        await db.flush()
        await db.refresh(db_obj)
        return db_obj

    async def update(
        self, db: AsyncSession, *, db_obj: Service, obj_in: ServiceUpdate
    ) -> Service:
        """Update a service, converting features, pricing_plans, and faqs to JSON."""
        update_data = obj_in.model_dump(exclude_unset=True)

        if "features" in update_data and update_data["features"] is not None:
            update_data["features"] = json.dumps(update_data["features"])
        if "pricing_plans" in update_data and update_data["pricing_plans"] is not None:
            update_data["pricing_plans"] = json.dumps(update_data["pricing_plans"])
        if "faqs" in update_data and update_data["faqs"] is not None:
            update_data["faqs"] = json.dumps(update_data["faqs"])

        for field, value in update_data.items():
            setattr(db_obj, field, value)

        db.add(db_obj)
        await db.flush()
        await db.refresh(db_obj)
        return db_obj


service_crud = CRUDService(Service)

