"""User CRUD operations."""
from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import get_password_hash, verify_password
from app.crud.base import CRUDBase
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate


class CRUDUser(CRUDBase[User, UserCreate, UserUpdate]):
    """CRUD operations for User model."""

    async def get_by_email(self, db: AsyncSession, email: str) -> Optional[User]:
        """Get user by email."""
        result = await db.execute(select(User).where(User.email == email))
        return result.scalar_one_or_none()

    async def get_by_firebase_uid(self, db: AsyncSession, firebase_uid: str) -> Optional[User]:
        """Get user by Firebase UID."""
        result = await db.execute(select(User).where(User.firebase_uid == firebase_uid))
        return result.scalar_one_or_none()

    async def get_or_create_from_firebase(
        self, db: AsyncSession, firebase_uid: str, email: str, name: str = ""
    ) -> User:
        """Return existing user matched by Firebase UID, migrating by email if needed.

        Creates a new admin user on first login if none exists.
        """
        # Primary lookup: by firebase_uid
        user = await self.get_by_firebase_uid(db, firebase_uid)
        if user:
            return user

        # Migration path: existing user created before Firebase had no firebase_uid
        user = await self.get_by_email(db, email)
        if user:
            user.firebase_uid = firebase_uid
            db.add(user)
            await db.flush()
            await db.refresh(user)
            return user

        # Auto-provision: new Firebase user gets an admin DB record
        display_name = name or email.split("@")[0]
        new_user = User(
            email=email,
            name=display_name,
            firebase_uid=firebase_uid,
            password_hash=None,
            role="admin",
            is_active=True,
        )
        db.add(new_user)
        await db.flush()
        await db.refresh(new_user)
        return new_user

    async def create(self, db: AsyncSession, *, obj_in: UserCreate) -> User:
        """Create a new user with hashed password."""
        db_obj = User(
            email=obj_in.email,
            name=obj_in.name,
            password_hash=get_password_hash(obj_in.password),
            role=obj_in.role,
        )
        db.add(db_obj)
        await db.flush()
        await db.refresh(db_obj)
        return db_obj

    async def update(self, db: AsyncSession, *, db_obj: User, obj_in: UserUpdate) -> User:
        """Update user, hashing password if provided."""
        update_data = obj_in.model_dump(exclude_unset=True)

        if "password" in update_data:
            update_data["password_hash"] = get_password_hash(update_data.pop("password"))

        for field, value in update_data.items():
            setattr(db_obj, field, value)

        db.add(db_obj)
        await db.flush()
        await db.refresh(db_obj)
        return db_obj

    async def authenticate(
        self, db: AsyncSession, *, email: str, password: str
    ) -> Optional[User]:
        """Authenticate user by email and password (legacy, not used with Firebase)."""
        user = await self.get_by_email(db, email=email)
        if not user or not user.password_hash:
            return None
        if not verify_password(password, user.password_hash):
            return None
        return user

    async def is_active(self, user: User) -> bool:
        return user.is_active

    async def is_admin(self, user: User) -> bool:
        return user.role == "admin"


user_crud = CRUDUser(User)
