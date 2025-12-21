"""Authentication endpoints."""
from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.security import create_access_token
from app.core.exceptions import UnauthorizedError, ConflictError
from app.crud.user import user_crud
from app.db.session import get_db
from app.schemas.user import UserCreate, UserLogin, UserResponse, Token
from app.schemas.common import MessageResponse
from app.api.v1.dependencies import get_current_user, get_current_admin_user
from app.models.user import User

router = APIRouter()


@router.post("/login", response_model=Token)
async def login(
    credentials: UserLogin,
    db: AsyncSession = Depends(get_db),
) -> Token:
    """
    Authenticate user and return JWT token.

    - **email**: User's email address
    - **password**: User's password
    """
    user = await user_crud.authenticate(
        db, email=credentials.email, password=credentials.password
    )

    if not user:
        raise UnauthorizedError("Invalid email or password")

    if not user.is_active:
        raise UnauthorizedError("User account is inactive")

    # Create access token
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email, "role": user.role},
        expires_delta=access_token_expires,
    )

    return Token(
        access_token=access_token,
        token_type="bearer",
        expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
    )


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register(
    user_in: UserCreate,
    db: AsyncSession = Depends(get_db),
    current_admin: User = Depends(get_current_admin_user),
) -> UserResponse:
    """
    Register a new user (admin only).

    - **email**: Unique email address
    - **name**: User's full name
    - **password**: Password (min 8 characters)
    - **role**: User role (admin or user)
    """
    # Check if user already exists
    existing_user = await user_crud.get_by_email(db, email=user_in.email)
    if existing_user:
        raise ConflictError("User with this email already exists")

    # Create user
    user = await user_crud.create(db, obj_in=user_in)
    return UserResponse.model_validate(user)


@router.get("/me", response_model=UserResponse)
async def get_current_user_info(
    current_user: User = Depends(get_current_user),
) -> UserResponse:
    """Get current authenticated user's information."""
    return UserResponse.model_validate(current_user)


@router.post("/logout", response_model=MessageResponse)
async def logout(
    current_user: User = Depends(get_current_user),
) -> MessageResponse:
    """
    Logout current user.
    
    Since JWT tokens are stateless, the actual token invalidation
    happens client-side by removing the token from storage.
    This endpoint is provided for API consistency and logging purposes.
    """
    # In a production system, you might want to:
    # - Add the token to a blacklist (if using Redis)
    # - Log the logout event
    # - Update user's last_logout timestamp
    return MessageResponse(message="Successfully logged out")


@router.post("/setup", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def setup_admin(
    user_in: UserCreate,
    db: AsyncSession = Depends(get_db),
) -> UserResponse:
    """
    Create initial admin user (only works if no users exist).

    This endpoint is for initial setup only and will fail if any users
    already exist in the database.
    """
    # Check if any users exist
    user_count = await user_crud.count(db)
    if user_count > 0:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Setup already completed. Use /register with admin credentials.",
        )

    # Force admin role for initial user
    user_data = user_in.model_copy(update={"role": "admin"})
    user = await user_crud.create(db, obj_in=user_data)

    return UserResponse.model_validate(user)

