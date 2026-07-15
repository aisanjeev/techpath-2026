"""Authentication endpoints."""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import ConflictError
from app.crud.user import user_crud
from app.db.session import get_db
from app.schemas.user import UserCreate, UserResponse
from app.schemas.common import MessageResponse
from app.api.v1.dependencies import get_current_user, get_current_admin_user
from app.models.user import User

router = APIRouter()


@router.get("/me", response_model=UserResponse)
async def get_current_user_info(
    current_user: User = Depends(get_current_user),
) -> UserResponse:
    """Return the authenticated user's profile (verifies Firebase token)."""
    return UserResponse.model_validate(current_user)


@router.post("/logout", response_model=MessageResponse)
async def logout(
    current_user: User = Depends(get_current_user),
) -> MessageResponse:
    """Acknowledge logout. Token invalidation is handled client-side via Firebase."""
    return MessageResponse(message="Successfully logged out")


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register(
    user_in: UserCreate,
    db: AsyncSession = Depends(get_db),
    current_admin: User = Depends(get_current_admin_user),
) -> UserResponse:
    """Create a new user in the local DB (admin only).

    Note: The user must also be created in Firebase console to be able to sign in.
    """
    existing = await user_crud.get_by_email(db, email=user_in.email)
    if existing:
        raise ConflictError("User with this email already exists")

    user = await user_crud.create(db, obj_in=user_in)
    return UserResponse.model_validate(user)


@router.post("/setup", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def setup_admin(
    user_in: UserCreate,
    db: AsyncSession = Depends(get_db),
) -> UserResponse:
    """Create the initial admin user (only works when the users table is empty)."""
    user_count = await user_crud.count(db)
    if user_count > 0:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Setup already completed. Use /register with admin credentials.",
        )

    user_data = user_in.model_copy(update={"role": "admin"})
    user = await user_crud.create(db, obj_in=user_data)
    return UserResponse.model_validate(user)
