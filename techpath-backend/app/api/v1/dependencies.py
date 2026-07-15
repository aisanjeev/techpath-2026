"""Shared API dependencies."""
from typing import Optional

from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.firebase_admin import verify_firebase_token
from app.core.exceptions import UnauthorizedError, ForbiddenError
from app.crud.user import user_crud
from app.db.session import get_db
from app.models.user import User

security = HTTPBearer(auto_error=False)


async def get_current_user(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security),
    db: AsyncSession = Depends(get_db),
) -> User:
    """Verify Firebase ID token and return the corresponding DB user.

    Auto-provisions a new admin user on first login.
    """
    if credentials is None:
        raise UnauthorizedError("Not authenticated")

    try:
        decoded = verify_firebase_token(credentials.credentials)
        firebase_uid: str = decoded.get("uid", "")
        email: str = decoded.get("email", "")
        name: str = decoded.get("name", "")

        if not firebase_uid or not email:
            raise UnauthorizedError("Invalid token claims")
    except (UnauthorizedError, ForbiddenError):
        raise
    except Exception:
        raise UnauthorizedError("Invalid or expired token")

    user = await user_crud.get_or_create_from_firebase(db, firebase_uid, email, name)

    if not user.is_active:
        raise UnauthorizedError("User account is inactive")

    return user


async def get_current_active_user(
    current_user: User = Depends(get_current_user),
) -> User:
    """Get current active user."""
    if not current_user.is_active:
        raise UnauthorizedError("Inactive user")
    return current_user


async def get_current_admin_user(
    current_user: User = Depends(get_current_user),
) -> User:
    """Get current user, asserting they have the admin role."""
    if current_user.role != "admin":
        raise ForbiddenError("Admin access required")
    return current_user


async def get_optional_user(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security),
    db: AsyncSession = Depends(get_db),
) -> Optional[User]:
    """Return the current user if authenticated, None otherwise."""
    if credentials is None:
        return None

    try:
        decoded = verify_firebase_token(credentials.credentials)
        firebase_uid: str = decoded.get("uid", "")
        email: str = decoded.get("email", "")
        name: str = decoded.get("name", "")

        if not firebase_uid or not email:
            return None

        user = await user_crud.get_or_create_from_firebase(db, firebase_uid, email, name)
        if user and user.is_active:
            return user
    except Exception:
        pass

    return None
