"""Pilot signup API endpoints."""
from typing import List, Optional

from fastapi import APIRouter, Depends, Query, Request, status, BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import NotFoundError
from app.crud.pilot_signup import pilot_signup_crud
from app.db.session import get_db
from app.schemas.pilot_signup import (
    PilotSignupCreate,
    PilotSignupUpdate,
    PilotSignupResponse,
    PilotSignupSubmitResponse,
)
from app.schemas.common import MessageResponse
from app.api.v1.dependencies import get_current_admin_user
from app.services.email_service import email_service
from app.models.user import User

router = APIRouter()

# Hardcoded admin email for pilot signup notifications
PILOT_SIGNUP_ADMIN_EMAIL = "sanjeev@techpath.biz"


# ----- Public Endpoint -----

@router.post("/", response_model=PilotSignupSubmitResponse, status_code=status.HTTP_201_CREATED)
async def submit_pilot_signup(
    signup_in: PilotSignupCreate,
    request: Request,
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(get_db),
) -> PilotSignupSubmitResponse:
    """
    Submit a pilot signup application.

    This is a public endpoint - no authentication required.
    """
    # Get request metadata
    ip_address = request.client.host if request.client else None
    user_agent = request.headers.get("user-agent")

    # Create signup
    signup = await pilot_signup_crud.create_with_metadata(
        db,
        obj_in=signup_in,
        ip_address=ip_address,
        user_agent=user_agent,
    )

    # Send notification email in background to hardcoded admin email
    if email_service.is_configured:
        background_tasks.add_task(
            email_service.send_pilot_signup_notification,
            PILOT_SIGNUP_ADMIN_EMAIL,
            signup_in.name,
            signup_in.email,
            signup_in.phone,
            signup_in.business_name,
            signup_in.industry,
            signup_in.message,
        )

    return PilotSignupSubmitResponse(
        success=True,
        message="Application submitted successfully",
        data={
            "applicationId": str(signup.id),
            "submittedAt": signup.created_at.isoformat() + "Z",
        },
    )


# ----- Admin Endpoints -----

@router.get("/applications", response_model=List[PilotSignupResponse])
async def list_applications(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    status_filter: Optional[str] = Query(None, alias="status", description="Filter by status"),
    industry: Optional[str] = Query(None, description="Filter by industry"),
    db: AsyncSession = Depends(get_db),
    current_admin: User = Depends(get_current_admin_user),
) -> List[PilotSignupResponse]:
    """List pilot signup applications (admin only)."""
    if status_filter:
        signups = await pilot_signup_crud.get_by_status(
            db, status=status_filter, skip=skip, limit=limit
        )
    elif industry:
        signups = await pilot_signup_crud.get_by_industry(
            db, industry=industry, skip=skip, limit=limit
        )
    else:
        signups = await pilot_signup_crud.get_recent(db, skip=skip, limit=limit)

    return [PilotSignupResponse.model_validate(s) for s in signups]


@router.get("/applications/{application_id}", response_model=PilotSignupResponse)
async def get_application(
    application_id: int,
    db: AsyncSession = Depends(get_db),
    current_admin: User = Depends(get_current_admin_user),
) -> PilotSignupResponse:
    """Get a single pilot signup application (admin only)."""
    signup = await pilot_signup_crud.get(db, id=application_id)
    if not signup:
        raise NotFoundError("Pilot signup application")
    return PilotSignupResponse.model_validate(signup)


@router.put("/applications/{application_id}", response_model=PilotSignupResponse)
async def update_application(
    application_id: int,
    signup_in: PilotSignupUpdate,
    db: AsyncSession = Depends(get_db),
    current_admin: User = Depends(get_current_admin_user),
) -> PilotSignupResponse:
    """Update pilot signup application status/notes (admin only)."""
    signup = await pilot_signup_crud.get(db, id=application_id)
    if not signup:
        raise NotFoundError("Pilot signup application")

    signup = await pilot_signup_crud.update(db, db_obj=signup, obj_in=signup_in)
    return PilotSignupResponse.model_validate(signup)


@router.delete("/applications/{application_id}", response_model=MessageResponse)
async def delete_application(
    application_id: int,
    db: AsyncSession = Depends(get_db),
    current_admin: User = Depends(get_current_admin_user),
) -> MessageResponse:
    """Delete a pilot signup application (admin only)."""
    signup = await pilot_signup_crud.get(db, id=application_id)
    if not signup:
        raise NotFoundError("Pilot signup application")

    await pilot_signup_crud.delete(db, id=application_id)
    return MessageResponse(message="Pilot signup application deleted successfully")
