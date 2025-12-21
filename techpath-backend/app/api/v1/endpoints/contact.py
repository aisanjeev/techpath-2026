"""Contact and newsletter API endpoints."""
from typing import List, Optional

from fastapi import APIRouter, Depends, Query, Request, status, BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import NotFoundError, ConflictError
from app.crud.contact import contact_crud, newsletter_crud
from app.db.session import get_db
from app.schemas.contact import (
    ContactInquiryCreate,
    ContactInquiryUpdate,
    ContactInquiryResponse,
    NewsletterCreate,
    NewsletterResponse,
)
from app.schemas.common import MessageResponse
from app.api.v1.dependencies import get_current_admin_user
from app.services.email_service import email_service, get_contact_form_recipients
from app.models.user import User

router = APIRouter()


# ----- Contact Inquiries -----

@router.post("/", response_model=MessageResponse, status_code=status.HTTP_201_CREATED)
async def submit_contact_form(
    inquiry_in: ContactInquiryCreate,
    request: Request,
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(get_db),
) -> MessageResponse:
    """
    Submit a contact form inquiry.

    This is a public endpoint - no authentication required.
    """
    # Get request metadata
    ip_address = request.client.host if request.client else None
    user_agent = request.headers.get("user-agent")

    # Create inquiry
    inquiry = await contact_crud.create_with_metadata(
        db,
        obj_in=inquiry_in,
        ip_address=ip_address,
        user_agent=user_agent,
    )

    # Send notification emails in background
    if email_service.is_configured:
        # Get admin recipients from app settings
        admin_recipients = await get_contact_form_recipients(db)
        
        # Send notification to admin(s)
        for admin_email in admin_recipients:
            background_tasks.add_task(
                email_service.send_contact_notification,
                admin_email,
                inquiry_in.name,
                inquiry_in.email,
                inquiry_in.subject,
                inquiry_in.message,
            )
        
        # Send confirmation to user
        background_tasks.add_task(
            email_service.send_contact_confirmation,
            inquiry_in.email,
            inquiry_in.name,
        )

    return MessageResponse(
        message="Thank you for your inquiry. We'll get back to you soon!"
    )


@router.get("/inquiries", response_model=List[ContactInquiryResponse])
async def list_inquiries(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    status: Optional[str] = Query(None, description="Filter by status"),
    db: AsyncSession = Depends(get_db),
    current_admin: User = Depends(get_current_admin_user),
) -> List[ContactInquiryResponse]:
    """List contact inquiries (admin only)."""
    if status:
        inquiries = await contact_crud.get_by_status(
            db, status=status, skip=skip, limit=limit
        )
    else:
        inquiries = await contact_crud.get_recent(db, skip=skip, limit=limit)

    return [ContactInquiryResponse.model_validate(i) for i in inquiries]


@router.get("/inquiries/{inquiry_id}", response_model=ContactInquiryResponse)
async def get_inquiry(
    inquiry_id: int,
    db: AsyncSession = Depends(get_db),
    current_admin: User = Depends(get_current_admin_user),
) -> ContactInquiryResponse:
    """Get a single inquiry (admin only)."""
    inquiry = await contact_crud.get(db, id=inquiry_id)
    if not inquiry:
        raise NotFoundError("Inquiry")
    return ContactInquiryResponse.model_validate(inquiry)


@router.put("/inquiries/{inquiry_id}", response_model=ContactInquiryResponse)
async def update_inquiry(
    inquiry_id: int,
    inquiry_in: ContactInquiryUpdate,
    db: AsyncSession = Depends(get_db),
    current_admin: User = Depends(get_current_admin_user),
) -> ContactInquiryResponse:
    """Update inquiry status/notes (admin only)."""
    inquiry = await contact_crud.get(db, id=inquiry_id)
    if not inquiry:
        raise NotFoundError("Inquiry")

    inquiry = await contact_crud.update(db, db_obj=inquiry, obj_in=inquiry_in)
    return ContactInquiryResponse.model_validate(inquiry)


@router.delete("/inquiries/{inquiry_id}", response_model=MessageResponse)
async def delete_inquiry(
    inquiry_id: int,
    db: AsyncSession = Depends(get_db),
    current_admin: User = Depends(get_current_admin_user),
) -> MessageResponse:
    """Delete an inquiry (admin only)."""
    inquiry = await contact_crud.get(db, id=inquiry_id)
    if not inquiry:
        raise NotFoundError("Inquiry")

    await contact_crud.delete(db, id=inquiry_id)
    return MessageResponse(message="Inquiry deleted successfully")


# ----- Newsletter -----

@router.post("/newsletter", response_model=MessageResponse, status_code=status.HTTP_201_CREATED)
async def subscribe_newsletter(
    subscriber_in: NewsletterCreate,
    request: Request,
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(get_db),
) -> MessageResponse:
    """
    Subscribe to the newsletter.

    This is a public endpoint - no authentication required.
    If already subscribed, the subscription will be reactivated.
    """
    ip_address = request.client.host if request.client else None

    subscriber = await newsletter_crud.subscribe(
        db, obj_in=subscriber_in, ip_address=ip_address
    )

    # Send welcome email in background
    if email_service.is_configured:
        background_tasks.add_task(
            email_service.send_newsletter_welcome,
            subscriber_in.email,
            subscriber_in.name,
        )

    return MessageResponse(message="Successfully subscribed to the newsletter!")


@router.delete("/newsletter", response_model=MessageResponse)
async def unsubscribe_newsletter(
    email: str = Query(..., description="Email to unsubscribe"),
    db: AsyncSession = Depends(get_db),
) -> MessageResponse:
    """
    Unsubscribe from the newsletter.

    This is a public endpoint - no authentication required.
    """
    subscriber = await newsletter_crud.unsubscribe(db, email=email)
    if not subscriber:
        raise NotFoundError("Subscriber")

    return MessageResponse(message="Successfully unsubscribed from the newsletter")


@router.get("/newsletter/subscribers", response_model=List[NewsletterResponse])
async def list_subscribers(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    active_only: bool = Query(True),
    db: AsyncSession = Depends(get_db),
    current_admin: User = Depends(get_current_admin_user),
) -> List[NewsletterResponse]:
    """List newsletter subscribers (admin only)."""
    if active_only:
        subscribers = await newsletter_crud.get_active(db, skip=skip, limit=limit)
    else:
        subscribers = await newsletter_crud.get_multi(db, skip=skip, limit=limit)

    return [NewsletterResponse.model_validate(s) for s in subscribers]

