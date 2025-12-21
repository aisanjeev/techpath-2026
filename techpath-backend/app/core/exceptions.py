"""Custom exception classes for the API."""
from typing import Any, Dict, Optional

from fastapi import status


class APIException(Exception):
    """Base exception for API errors."""

    def __init__(
        self,
        message: str,
        status_code: int = status.HTTP_400_BAD_REQUEST,
        error_code: Optional[str] = None,
        details: Optional[Dict[str, Any]] = None,
    ) -> None:
        self.message = message
        self.status_code = status_code
        self.error_code = error_code or "API_ERROR"
        self.details = details or {}
        super().__init__(self.message)

    def to_dict(self) -> Dict[str, Any]:
        """Convert exception to dictionary for JSON response."""
        return {
            "success": False,
            "error": {
                "code": self.error_code,
                "message": self.message,
                "details": self.details,
            },
        }


class ValidationError(APIException):
    """Validation error exception."""

    def __init__(
        self, message: str = "Validation error", details: Optional[Dict[str, Any]] = None
    ) -> None:
        super().__init__(
            message=message,
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            error_code="VALIDATION_ERROR",
            details=details,
        )


class NotFoundError(APIException):
    """Resource not found exception."""

    def __init__(self, resource: str = "Resource") -> None:
        super().__init__(
            message=f"{resource} not found",
            status_code=status.HTTP_404_NOT_FOUND,
            error_code="NOT_FOUND",
        )


class UnauthorizedError(APIException):
    """Unauthorized access exception."""

    def __init__(self, message: str = "Unauthorized") -> None:
        super().__init__(
            message=message,
            status_code=status.HTTP_401_UNAUTHORIZED,
            error_code="UNAUTHORIZED",
        )


class ForbiddenError(APIException):
    """Forbidden access exception."""

    def __init__(self, message: str = "Access forbidden") -> None:
        super().__init__(
            message=message,
            status_code=status.HTTP_403_FORBIDDEN,
            error_code="FORBIDDEN",
        )


class ConflictError(APIException):
    """Resource conflict exception."""

    def __init__(self, message: str = "Resource already exists") -> None:
        super().__init__(
            message=message,
            status_code=status.HTTP_409_CONFLICT,
            error_code="CONFLICT",
        )


class RateLimitError(APIException):
    """Rate limit exceeded exception."""

    def __init__(self, message: str = "Rate limit exceeded") -> None:
        super().__init__(
            message=message,
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            error_code="RATE_LIMIT_EXCEEDED",
        )


class ExternalServiceError(APIException):
    """External service error exception."""

    def __init__(
        self, service: str = "External service", message: Optional[str] = None
    ) -> None:
        super().__init__(
            message=message or f"{service} is unavailable",
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            error_code="EXTERNAL_SERVICE_ERROR",
            details={"service": service},
        )

