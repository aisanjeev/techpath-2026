"""Contact and newsletter CRUD operations."""
from typing import List, Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models.contact import ContactInquiry, NewsletterSubscriber
from app.schemas.contact import (
    ContactInquiryCreate,
    ContactInquiryUpdate,
    NewsletterCreate,
)


class CRUDContactInquiry(CRUDBase[ContactInquiry, ContactInquiryCreate, ContactInquiryUpdate]):
    """CRUD operations for ContactInquiry model."""

    async def get_by_status(
        self,
        db: AsyncSession,
        *,
        status: str,
        skip: int = 0,
        limit: int = 100,
    ) -> List[ContactInquiry]:
        """Get inquiries by status."""
        query = (
            select(ContactInquiry)
            .where(ContactInquiry.status == status)
            .order_by(ContactInquiry.created_at.desc())
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
    ) -> List[ContactInquiry]:
        """Get recent inquiries ordered by creation date."""
        query = (
            select(ContactInquiry)
            .order_by(ContactInquiry.created_at.desc())
            .offset(skip)
            .limit(limit)
        )
        result = await db.execute(query)
        return list(result.scalars().all())

    async def create_with_metadata(
        self,
        db: AsyncSession,
        *,
        obj_in: ContactInquiryCreate,
        ip_address: Optional[str] = None,
        user_agent: Optional[str] = None,
    ) -> ContactInquiry:
        """Create inquiry with request metadata."""
        obj_data = obj_in.model_dump()
        obj_data["ip_address"] = ip_address
        obj_data["user_agent"] = user_agent

        db_obj = ContactInquiry(**obj_data)
        db.add(db_obj)
        await db.flush()
        await db.refresh(db_obj)
        return db_obj


class CRUDNewsletterSubscriber(CRUDBase[NewsletterSubscriber, NewsletterCreate, NewsletterCreate]):
    """CRUD operations for NewsletterSubscriber model."""

    async def get_by_email(
        self, db: AsyncSession, email: str
    ) -> Optional[NewsletterSubscriber]:
        """Get subscriber by email."""
        result = await db.execute(
            select(NewsletterSubscriber).where(NewsletterSubscriber.email == email)
        )
        return result.scalar_one_or_none()

    async def get_active(
        self,
        db: AsyncSession,
        *,
        skip: int = 0,
        limit: int = 1000,
    ) -> List[NewsletterSubscriber]:
        """Get active subscribers."""
        query = (
            select(NewsletterSubscriber)
            .where(NewsletterSubscriber.is_active == True)
            .order_by(NewsletterSubscriber.created_at.desc())
            .offset(skip)
            .limit(limit)
        )
        result = await db.execute(query)
        return list(result.scalars().all())

    async def subscribe(
        self,
        db: AsyncSession,
        *,
        obj_in: NewsletterCreate,
        ip_address: Optional[str] = None,
    ) -> NewsletterSubscriber:
        """Subscribe to newsletter, reactivating if previously unsubscribed."""
        existing = await self.get_by_email(db, email=obj_in.email)

        if existing:
            # Reactivate if previously unsubscribed
            existing.is_active = True
            if obj_in.name:
                existing.name = obj_in.name
            db.add(existing)
            await db.flush()
            await db.refresh(existing)
            return existing

        # Create new subscriber
        obj_data = obj_in.model_dump()
        obj_data["ip_address"] = ip_address

        db_obj = NewsletterSubscriber(**obj_data)
        db.add(db_obj)
        await db.flush()
        await db.refresh(db_obj)
        return db_obj

    async def unsubscribe(
        self, db: AsyncSession, email: str
    ) -> Optional[NewsletterSubscriber]:
        """Unsubscribe from newsletter."""
        subscriber = await self.get_by_email(db, email=email)
        if subscriber:
            subscriber.is_active = False
            db.add(subscriber)
            await db.flush()
            await db.refresh(subscriber)
        return subscriber


contact_crud = CRUDContactInquiry(ContactInquiry)
newsletter_crud = CRUDNewsletterSubscriber(NewsletterSubscriber)

