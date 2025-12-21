"""AI-related Pydantic schemas."""
from typing import List, Optional

from pydantic import BaseModel, Field


class ChatMessage(BaseModel):
    """Chat message schema."""

    role: str = Field(..., pattern="^(user|assistant|system)$")
    content: str = Field(..., min_length=1)


class ChatRequest(BaseModel):
    """Schema for AI chat request."""

    message: str = Field(..., min_length=1, max_length=4000)
    conversation_history: Optional[List[ChatMessage]] = None
    context: Optional[str] = Field(None, max_length=2000)  # Additional context about services


class ChatResponse(BaseModel):
    """Schema for AI chat response."""

    message: str
    conversation_id: Optional[str] = None


class SuggestionRequest(BaseModel):
    """Schema for AI service suggestion request."""

    query: str = Field(..., min_length=5, max_length=1000)
    industry: Optional[str] = None
    budget: Optional[str] = None
    timeline: Optional[str] = None


class SuggestionResponse(BaseModel):
    """Schema for AI service suggestion response."""

    suggestions: List["ServiceSuggestion"]
    reasoning: str


class ServiceSuggestion(BaseModel):
    """Individual service suggestion."""

    service_name: str
    service_slug: str
    relevance_score: float = Field(..., ge=0, le=1)
    explanation: str


# Update forward references
SuggestionResponse.model_rebuild()

