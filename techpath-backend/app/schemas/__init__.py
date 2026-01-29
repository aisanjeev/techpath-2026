"""Pydantic schemas module."""
from app.schemas.common import (
    APIResponse,
    PaginatedResponse,
    MessageResponse,
    HealthResponse,
)
from app.schemas.user import UserCreate, UserUpdate, UserResponse, UserLogin, Token
from app.schemas.service import ServiceCreate, ServiceUpdate, ServiceResponse
from app.schemas.blog import BlogPostCreate, BlogPostUpdate, BlogPostResponse
from app.schemas.contact import (
    ContactInquiryCreate,
    ContactInquiryResponse,
    NewsletterCreate,
    NewsletterResponse,
)
from app.schemas.ai import ChatRequest, ChatResponse, SuggestionRequest, SuggestionResponse
from app.schemas.pilot_signup import (
    PilotSignupCreate,
    PilotSignupUpdate,
    PilotSignupResponse,
    PilotSignupSubmitResponse,
)

__all__ = [
    # Common
    "APIResponse",
    "PaginatedResponse",
    "MessageResponse",
    "HealthResponse",
    # User
    "UserCreate",
    "UserUpdate",
    "UserResponse",
    "UserLogin",
    "Token",
    # Service
    "ServiceCreate",
    "ServiceUpdate",
    "ServiceResponse",
    # Blog
    "BlogPostCreate",
    "BlogPostUpdate",
    "BlogPostResponse",
    # Contact
    "ContactInquiryCreate",
    "ContactInquiryResponse",
    "NewsletterCreate",
    "NewsletterResponse",
    # AI
    "ChatRequest",
    "ChatResponse",
    "SuggestionRequest",
    "SuggestionResponse",
    # Pilot Signup
    "PilotSignupCreate",
    "PilotSignupUpdate",
    "PilotSignupResponse",
    "PilotSignupSubmitResponse",
]

