"""Pilot signup CRUD operations."""
from typing import List, Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models.pilot_signup import PilotSignup
from app.schemas.pilot_signup import PilotSignupCreate, PilotSignupUpdate


class CRUDPilotSignup(CRUDBase[PilotSignup, PilotSignupCreate, PilotSignupUpdate]):
    """CRUD operations for PilotSignup model."""

    async def get_by_status(
        self,
        db: AsyncSession,
        *,
        status: str,
        skip: int = 0,
        limit: int = 100,
    ) -> List[PilotSignup]:
        """Get pilot signups by status."""
        query = (
            select(PilotSignup)
            .where(PilotSignup.status == status)
            .order_by(PilotSignup.created_at.desc())
            .offset(skip)
            .limit(limit)
        )
        result = await db.execute(query)
        return list(result.scalars().all())

    async def get_by_industry(
        self,
        db: AsyncSession,
        *,
        industry: str,
        skip: int = 0,
        limit: int = 100,
    ) -> List[PilotSignup]:
        """Get pilot signups by industry."""
        query = (
            select(PilotSignup)
            .where(PilotSignup.industry == industry)
            .order_by(PilotSignup.created_at.desc())
            .offset(skip)
            .limit(limit)
        )
        result = await db.execute(query)
        return list(result.scalars().all())

    async def get_recent(
        self,
        db: AsyncSession,
        *,
        skip: int = 0,
        limit: int = 100,
    ) -> List[PilotSignup]:
        """Get recent pilot signups ordered by creation date."""
        query = (
            select(PilotSignup)
            .order_by(PilotSignup.created_at.desc())
            .offset(skip)
            .limit(limit)
        )
        result = await db.execute(query)
        return list(result.scalars().all())

    async def create_with_metadata(
        self,
        db: AsyncSession,
        *,
        obj_in: PilotSignupCreate,
        ip_address: Optional[str] = None,
        user_agent: Optional[str] = None,
    ) -> PilotSignup:
        """Create pilot signup with request metadata."""
        obj_data = obj_in.model_dump(by_alias=False)
        obj_data["ip_address"] = ip_address
        obj_data["user_agent"] = user_agent

        db_obj = PilotSignup(**obj_data)
        db.add(db_obj)
        await db.flush()
        await db.refresh(db_obj)
        return db_obj


pilot_signup_crud = CRUDPilotSignup(PilotSignup)
