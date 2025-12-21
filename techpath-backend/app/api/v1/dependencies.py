"""Shared API dependencies."""
from typing import Optional

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import decode_access_token
from app.core.exceptions import UnauthorizedError, ForbiddenError
from app.crud.user import user_crud
from app.db.session import get_db
from app.models.user import User

# Security scheme
security = HTTPBearer(auto_error=False)


async def get_current_user(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security),
    db: AsyncSession = Depends(get_db),
) -> User:
    """
    Get the current authenticated user from JWT token.

    Raises:
        UnauthorizedError: If token is missing or invalid
    """
    if credentials is None:
        raise UnauthorizedError("Not authenticated")

    try:
        payload = decode_access_token(credentials.credentials)
        email: str = payload.get("sub")
        if email is None:
            raise UnauthorizedError("Invalid token")
    except Exception:
        raise UnauthorizedError("Invalid token")

    user = await user_crud.get_by_email(db, email=email)
    if user is None:
        raise UnauthorizedError("User not found")

    if not user.is_active:
        raise UnauthorizedError("User is inactive")

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
    """
    Get current user if they are an admin.

    Raises:
        ForbiddenError: If user is not an admin
    """
    if current_user.role != "admin":
        raise ForbiddenError("Admin access required")
    return current_user


async def get_optional_user(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security),
    db: AsyncSession = Depends(get_db),
) -> Optional[User]:
    """
    Get the current user if authenticated, None otherwise.

    Does not raise an error if not authenticated.
    """
    if credentials is None:
        return None

    try:
        payload = decode_access_token(credentials.credentials)
        email: str = payload.get("sub")
        if email is None:
            return None

        user = await user_crud.get_by_email(db, email=email)
        if user and user.is_active:
            return user
    except Exception:
        pass

    return None

