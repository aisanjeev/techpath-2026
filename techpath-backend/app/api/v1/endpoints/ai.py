"""AI-powered API endpoints."""
from typing import Optional

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.exceptions import ExternalServiceError
from app.crud.service import service_crud
from app.db.session import get_db
from app.schemas.ai import ChatRequest, ChatResponse, SuggestionRequest, SuggestionResponse
from app.services.ai_service import ai_service
from app.api.v1.dependencies import get_optional_user
from app.models.user import User

router = APIRouter()


@router.post("/chat", response_model=ChatResponse)
async def chat(
    request: ChatRequest,
    db: AsyncSession = Depends(get_db),
    current_user: Optional[User] = Depends(get_optional_user),
) -> ChatResponse:
    """
    Chat with AI assistant about TechPath services.

    The AI assistant can answer questions about:
    - Available services
    - Pricing and packages
    - Technical capabilities
    - Project timelines
    """
    if not settings.has_openai_config:
        raise ExternalServiceError(
            "Azure OpenAI",
            "AI chat is not available. Azure OpenAI is not configured.",
        )

    # Get services context
    services = await service_crud.get_active(db, limit=10)
    services_context = "\n".join(
        f"- {s.title}: {s.short_description or s.description[:200]}"
        for s in services
    )

    context = f"Our services:\n{services_context}"
    if request.context:
        context = f"{context}\n\nAdditional context: {request.context}"

    response = await ai_service.chat(
        message=request.message,
        conversation_history=request.conversation_history,
        context=context,
    )

    return ChatResponse(message=response)


@router.post("/suggest", response_model=SuggestionResponse)
async def suggest_services(
    request: SuggestionRequest,
    db: AsyncSession = Depends(get_db),
) -> SuggestionResponse:
    """
    Get AI-powered service suggestions based on user needs.

    Describe your requirements and get personalized recommendations
    for the most suitable services.
    """
    if not settings.has_openai_config:
        raise ExternalServiceError(
            "Azure OpenAI",
            "Service suggestions are not available. Azure OpenAI is not configured.",
        )

    # Get all active services
    services = await service_crud.get_active(db, limit=20)
    available_services = [
        {
            "name": s.title,
            "slug": s.slug,
            "description": s.short_description or s.description[:300],
        }
        for s in services
    ]

    suggestions, reasoning = await ai_service.suggest_services(
        query=request.query,
        available_services=available_services,
        industry=request.industry,
        budget=request.budget,
        timeline=request.timeline,
    )

    return SuggestionResponse(
        suggestions=suggestions,
        reasoning=reasoning,
    )


@router.get("/status")
async def ai_status() -> dict:
    """Check if AI services are available."""
    return {
        "configured": settings.has_openai_config,
        "endpoint": settings.AZURE_OPENAI_ENDPOINT[:30] + "..." if settings.AZURE_OPENAI_ENDPOINT else None,
        "model": settings.AZURE_OPENAI_DEPLOYMENT if settings.has_openai_config else None,
    }

