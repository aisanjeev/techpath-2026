"""Authentication and user administration endpoints."""
import logging
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.constants import UserRole
from app.core.exceptions import ConflictError, NotFoundError, ValidationError
from app.core.firebase_admin import create_firebase_user, delete_firebase_user, update_firebase_user_by_email
from app.crud.user import user_crud
from app.db.session import get_db
from app.schemas.user import (
    UserAdminResponse,
    UserAdminUpdate,
    UserCreate,
    UserProvision,
    UserResponse,
)
from app.schemas.common import MessageResponse
from app.api.v1.dependencies import get_current_user, get_current_admin_user
from app.models.user import User

logger = logging.getLogger(__name__)

router = APIRouter()


def _admin_out(user: User) -> UserAdminResponse:
    return UserAdminResponse(
        id=user.id,
        email=user.email,
        name=user.name,
        role=user.role,
        is_active=user.is_active,
        avatar_url=user.avatar_url,
        has_signed_in=user.firebase_uid is not None,
        created_at=user.created_at,
        updated_at=user.updated_at,
    )


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


@router.get("/users")
async def list_users(
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    role: Optional[str] = Query(None),
    db: AsyncSession = Depends(get_db),
    current_admin: User = Depends(get_current_admin_user),
) -> JSONResponse:
    """List users so an admin can assign roles and activate accounts."""
    filters = {"role": role} if role else None
    users = await user_crud.get_multi(
        db, skip=skip, limit=limit, filters=filters, order_by="id"
    )
    total = await user_crud.count(db, filters=filters)
    data = [_admin_out(u).model_dump(mode="json") for u in users]
    return JSONResponse(content=data, headers={"X-Total-Count": str(total)})


@router.post("/users", response_model=UserAdminResponse, status_code=status.HTTP_201_CREATED)
async def provision_user(
    payload: UserProvision,
    db: AsyncSession = Depends(get_db),
    current_admin: User = Depends(get_current_admin_user),
) -> UserAdminResponse:
    """Create a user, optionally with a Firebase account in one step.

    If ``password`` is provided, the Firebase account is created automatically and
    linked immediately — no manual Firebase console step needed. Without a password,
    only the local record is created (the admin creates the Firebase account manually).
    """
    user = await user_crud.get_by_email(db, email=payload.email)

    firebase_uid = None
    if payload.password:
        try:
            firebase_uid = create_firebase_user(
                email=payload.email,
                password=payload.password,
                display_name=payload.name,
            )
        except Exception as exc:
            error_msg = str(exc)
            if "EMAIL_EXISTS" in error_msg:
                try:
                    firebase_uid = update_firebase_user_by_email(
                        email=payload.email,
                        password=payload.password,
                        display_name=payload.name,
                    )
                except Exception as update_exc:
                    logger.error("Firebase user update failed: %s", update_exc)
                    raise ValidationError(f"Could not update existing Firebase account: {update_exc}")
            else:
                logger.error("Firebase user creation failed: %s", exc)
                raise ValidationError(f"Could not create Firebase account: {error_msg}")

    if user:
        user.name = payload.name
        user.role = payload.role
        user.is_active = payload.is_active
        if firebase_uid:
            user.firebase_uid = firebase_uid
        db.add(user)
    else:
        user = User(
            email=payload.email,
            name=payload.name,
            password_hash=None,
            firebase_uid=firebase_uid,
            role=payload.role,
            is_active=payload.is_active,
        )
        db.add(user)
        
    await db.flush()
    await db.refresh(user)
    return _admin_out(user)


@router.patch("/users/{user_id}", response_model=UserAdminResponse)
async def update_user(
    user_id: int,
    payload: UserAdminUpdate,
    db: AsyncSession = Depends(get_db),
    current_admin: User = Depends(get_current_admin_user),
) -> UserAdminResponse:
    """Change a user's role or activation."""
    user = await user_crud.get(db, user_id)
    if not user:
        raise NotFoundError("User")

    # Guard against an admin locking themselves out; recovering needs DB access.
    if user.id == current_admin.id:
        if payload.is_active is False:
            raise ValidationError("You cannot deactivate your own account")
        if payload.role and payload.role != UserRole.ADMIN.value:
            raise ValidationError("You cannot remove your own admin role")

    data = payload.model_dump(exclude_unset=True)

    # Removing the last admin would leave nobody able to grant the role back.
    if data.get("role") and user.role == UserRole.ADMIN.value:
        if data["role"] != UserRole.ADMIN.value:
            admin_count = await user_crud.count(db, filters={"role": UserRole.ADMIN.value})
            if admin_count <= 1:
                raise ValidationError("Cannot demote the only remaining admin")

    for field, value in data.items():
        setattr(user, field, value)
    db.add(user)
    await db.flush()
    await db.refresh(user)
    return _admin_out(user)


@router.delete("/users/{user_id}", response_model=MessageResponse)
async def delete_user(
    user_id: int,
    db: AsyncSession = Depends(get_db),
    current_admin: User = Depends(get_current_admin_user),
) -> MessageResponse:
    """Delete a user from TechPath and Firebase."""
    user = await user_crud.get(db, user_id)
    if not user:
        raise NotFoundError("User")

    if user.id == current_admin.id:
        raise ValidationError("You cannot delete your own account")

    if user.role == UserRole.ADMIN.value:
        admin_count = await user_crud.count(db, filters={"role": UserRole.ADMIN.value})
        if admin_count <= 1:
            raise ValidationError("Cannot delete the only remaining admin")

    # Delete from Firebase if linked
    if user.firebase_uid:
        try:
            delete_firebase_user(user.firebase_uid)
        except Exception as exc:
            logger.warning(
                "Firebase deletion failed for uid=%s (continuing with local delete): %s",
                user.firebase_uid,
                exc,
            )

    await db.delete(user)
    await db.flush()
    return MessageResponse(message=f"User {user.email} has been deleted")


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
