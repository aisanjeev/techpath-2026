"""Contact and newsletter API endpoints."""

from typing import List, Optional

from fastapi import APIRouter, Depends, Query, Request, status, BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.exceptions import ForbiddenError, NotFoundError, ConflictError
from app.core.rate_limit import SlidingWindowRateLimiter, get_client_ip
from app.crud.contact import contact_crud, newsletter_crud
from app.db.session import get_db
from app.schemas.contact import (
    SPAM_PROTECTION_FIELDS,
    ContactInquiryCreate,
    ContactInquirySubmit,
    ContactInquiryUpdate,
    ContactInquiryResponse,
    NewsletterCreate,
    NewsletterSubscribe,
    NewsletterResponse,
)
from app.schemas.common import MessageResponse
from app.api.v1.dependencies import get_current_admin_user
from app.services.email_service import email_service, get_contact_form_recipients
from app.services.turnstile import verify_turnstile_token
from app.models.user import User

router = APIRouter()

# Public-form abuse damping. Per-IP, in-memory (see SlidingWindowRateLimiter for
# the multi-worker caveat). Emails are only sent after every check passes, so
# these limits also cap outbound notification/confirmation email volume.
_contact_limiter = SlidingWindowRateLimiter(max_hits=settings.CONTACT_RATE_LIMIT_PER_HOUR)
_newsletter_limiter = SlidingWindowRateLimiter(max_hits=settings.NEWSLETTER_RATE_LIMIT_PER_HOUR)

_CONTACT_SUCCESS_MESSAGE = "Thank you for your inquiry. We'll get back to you soon!"
_NEWSLETTER_SUCCESS_MESSAGE = "Successfully subscribed to the newsletter!"
_VERIFICATION_FAILED_MESSAGE = "Verification failed — please refresh the page and try again."


# ----- Contact Inquiries -----


@router.post("/", response_model=MessageResponse, status_code=status.HTTP_201_CREATED)
async def submit_contact_form(
    inquiry_in: ContactInquirySubmit,
    request: Request,
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(get_db),
) -> MessageResponse:
    """
    Submit a contact form inquiry.

    This is a public endpoint - no authentication required.
    """
    # Get request metadata
    ip_address = get_client_ip(request)
    user_agent = request.headers.get("user-agent")

    _contact_limiter.check(ip_address, "Too many submissions — please try again later")

    # Honeypot: hidden field real users never fill. Return the normal success
    # response without saving anything so bots can't tell they were caught.
    if inquiry_in.website:
        return MessageResponse(message=_CONTACT_SUCCESS_MESSAGE)

    if not await verify_turnstile_token(inquiry_in.turnstile_token, ip_address):
        raise ForbiddenError(_VERIFICATION_FAILED_MESSAGE)

    # Create inquiry
    inquiry = await contact_crud.create_with_metadata(
        db,
        obj_in=ContactInquiryCreate(**inquiry_in.model_dump(exclude=SPAM_PROTECTION_FIELDS)),
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

    return MessageResponse(message=_CONTACT_SUCCESS_MESSAGE)


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
        inquiries = await contact_crud.get_by_status(db, status=status, skip=skip, limit=limit)
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
    subscriber_in: NewsletterSubscribe,
    request: Request,
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(get_db),
) -> MessageResponse:
    """
    Subscribe to the newsletter.

    This is a public endpoint - no authentication required.
    If already subscribed, the subscription will be reactivated.
    """
    ip_address = get_client_ip(request)

    _newsletter_limiter.check(ip_address, "Too many submissions — please try again later")

    # Honeypot — see submit_contact_form.
    if subscriber_in.website:
        return MessageResponse(message=_NEWSLETTER_SUCCESS_MESSAGE)

    if not await verify_turnstile_token(subscriber_in.turnstile_token, ip_address):
        raise ForbiddenError(_VERIFICATION_FAILED_MESSAGE)

    subscriber = await newsletter_crud.subscribe(
        db,
        obj_in=NewsletterCreate(**subscriber_in.model_dump(exclude=SPAM_PROTECTION_FIELDS)),
        ip_address=ip_address,
    )

    # Send welcome email in background
    if email_service.is_configured:
        background_tasks.add_task(
            email_service.send_newsletter_welcome,
            subscriber_in.email,
            subscriber_in.name,
        )

    return MessageResponse(message=_NEWSLETTER_SUCCESS_MESSAGE)


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
