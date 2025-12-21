"""Application constants."""
from enum import Enum


class UserRole(str, Enum):
    """User role enumeration."""

    ADMIN = "admin"
    USER = "user"


class InquiryStatus(str, Enum):
    """Contact inquiry status enumeration."""

    NEW = "new"
    IN_PROGRESS = "in_progress"
    RESOLVED = "resolved"
    CLOSED = "closed"


class BlogPostStatus(str, Enum):
    """Blog post status enumeration."""

    DRAFT = "draft"
    PUBLISHED = "published"
    ARCHIVED = "archived"


# Pagination defaults
DEFAULT_PAGE_SIZE = 10
MAX_PAGE_SIZE = 100

# File upload limits
MAX_UPLOAD_SIZE_MB = 10
ALLOWED_IMAGE_TYPES = ["image/jpeg", "image/png", "image/webp", "image/gif"]
ALLOWED_DOCUMENT_TYPES = ["application/pdf", "application/msword"]

# Cache TTL (in seconds)
CACHE_TTL_SHORT = 60  # 1 minute
CACHE_TTL_MEDIUM = 300  # 5 minutes
CACHE_TTL_LONG = 3600  # 1 hour

# Rate limiting
RATE_LIMIT_REQUESTS = 100
RATE_LIMIT_WINDOW_SECONDS = 60

