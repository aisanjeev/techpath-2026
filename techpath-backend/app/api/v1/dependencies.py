"""Shared API dependencies."""
import logging
from collections.abc import Awaitable, Callable
from typing import Optional

from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.constants import UserRole
from app.core.firebase_admin import verify_firebase_token
from app.core.exceptions import UnauthorizedError, ForbiddenError
from app.crud.training_roster import training_student_crud
from app.crud.user import user_crud
from app.db.session import get_db
from app.models.training_roster import TrainingStudent
from app.models.user import User

logger = logging.getLogger(__name__)

security = HTTPBearer(auto_error=False)


async def get_current_user(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security),
    db: AsyncSession = Depends(get_db),
) -> User:
    """Verify Firebase ID token and return the corresponding DB user.

    An unrecognised Firebase account is provisioned inactive and rejected here; an
    admin must activate it before it can authenticate.
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
    except Exception as exc:
        # The client only ever gets "invalid or expired", but a misconfigured Admin SDK
        # fails here identically to a genuinely expired token — so log the real cause.
        logger.warning(
            "Firebase token verification failed: %s: %s", type(exc).__name__, exc
        )
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


def require_roles(*roles: UserRole) -> Callable[[User], Awaitable[User]]:
    """Build a dependency asserting the current user holds one of ``roles``."""
    allowed = {role.value for role in roles}

    async def dependency(current_user: User = Depends(get_current_user)) -> User:
        if current_user.role not in allowed:
            raise ForbiddenError(f"Requires one of: {', '.join(sorted(allowed))}")
        return current_user

    return dependency


get_current_admin_user = require_roles(UserRole.ADMIN)

# Admins are deliberately allowed through trainer routes so they can support trainers.
get_current_trainer_user = require_roles(UserRole.TRAINER, UserRole.ADMIN)


async def get_current_student(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security),
    db: AsyncSession = Depends(get_db),
) -> TrainingStudent:
    """Verify Firebase ID token and resolve it to a roster student.

    Deliberately independent of ``get_current_user``/``User`` end to end — a student
    signing in with Gmail must never be resolvable as (or confusable with) an admin or
    trainer account, even though both flows verify tokens from the same Firebase
    project. See ``CRUDTrainingStudent.get_or_link_from_firebase`` for why an
    unrecognised account is rejected rather than provisioned.
    """
    if credentials is None:
        raise UnauthorizedError("Not authenticated")

    try:
        decoded = verify_firebase_token(credentials.credentials)
        firebase_uid: str = decoded.get("uid", "")
        email: str = decoded.get("email", "")

        if not firebase_uid or not email:
            raise UnauthorizedError("Invalid token claims")
    except (UnauthorizedError, ForbiddenError):
        raise
    except Exception as exc:
        logger.warning(
            "Firebase token verification failed (student portal): %s: %s",
            type(exc).__name__,
            exc,
        )
        raise UnauthorizedError("Invalid or expired token")

    student = await training_student_crud.get_or_link_from_firebase(db, firebase_uid, email)
    if student is None:
        raise UnauthorizedError("This Google account isn't linked to any TechPath training roster")

    return student


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
