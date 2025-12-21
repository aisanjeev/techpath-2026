"""Common Pydantic schemas for API responses."""
from datetime import datetime
from typing import Any, Generic, List, Optional, TypeVar

from pydantic import BaseModel, ConfigDict

T = TypeVar("T")


class APIResponse(BaseModel, Generic[T]):
    """Standard API response wrapper."""

    success: bool = True
    data: Optional[T] = None
    message: Optional[str] = None
    timestamp: datetime = datetime.utcnow()

    model_config = ConfigDict(from_attributes=True)


class PaginatedResponse(BaseModel, Generic[T]):
    """Paginated API response."""

    success: bool = True
    data: List[T]
    pagination: "PaginationMeta"
    timestamp: datetime = datetime.utcnow()

    model_config = ConfigDict(from_attributes=True)


class PaginationMeta(BaseModel):
    """Pagination metadata."""

    total: int
    page: int
    per_page: int
    pages: int


class MessageResponse(BaseModel):
    """Simple message response."""

    success: bool = True
    message: str


class HealthResponse(BaseModel):
    """Health check response."""

    status: str = "healthy"
    version: str
    database: str = "connected"
    timestamp: datetime = datetime.utcnow()


class ErrorDetail(BaseModel):
    """Error detail schema."""

    code: str
    message: str
    details: dict[str, Any] = {}


class ErrorResponse(BaseModel):
    """Error response schema."""

    success: bool = False
    error: ErrorDetail

