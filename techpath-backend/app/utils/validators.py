"""Custom validation utilities."""
import re
from typing import Optional


def validate_email(email: str) -> bool:
    """
    Validate email format.

    Args:
        email: Email address to validate

    Returns:
        True if valid, False otherwise
    """
    pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    return bool(re.match(pattern, email))


def validate_phone(phone: str) -> bool:
    """
    Validate phone number format.

    Accepts various formats including:
    - +1234567890
    - (123) 456-7890
    - 123-456-7890
    - 123.456.7890

    Args:
        phone: Phone number to validate

    Returns:
        True if valid, False otherwise
    """
    # Remove all non-digit characters except +
    cleaned = re.sub(r"[^\d+]", "", phone)

    # Check length (7-15 digits, optionally starting with +)
    if cleaned.startswith("+"):
        return 8 <= len(cleaned) <= 16
    return 7 <= len(cleaned) <= 15


def validate_slug(slug: str) -> bool:
    """
    Validate URL slug format.

    Args:
        slug: Slug to validate

    Returns:
        True if valid, False otherwise
    """
    pattern = r"^[a-z0-9]+(?:-[a-z0-9]+)*$"
    return bool(re.match(pattern, slug))


def validate_password_strength(password: str) -> tuple[bool, Optional[str]]:
    """
    Validate password strength.

    Requirements:
    - At least 8 characters
    - At least one uppercase letter
    - At least one lowercase letter
    - At least one digit

    Args:
        password: Password to validate

    Returns:
        Tuple of (is_valid, error_message)
    """
    if len(password) < 8:
        return False, "Password must be at least 8 characters long"

    if not re.search(r"[A-Z]", password):
        return False, "Password must contain at least one uppercase letter"

    if not re.search(r"[a-z]", password):
        return False, "Password must contain at least one lowercase letter"

    if not re.search(r"\d", password):
        return False, "Password must contain at least one digit"

    return True, None


def sanitize_html(html: str) -> str:
    """
    Remove potentially dangerous HTML tags.

    Args:
        html: HTML string to sanitize

    Returns:
        Sanitized HTML string
    """
    # Remove script tags and their content
    html = re.sub(r"<script[^>]*>.*?</script>", "", html, flags=re.DOTALL | re.IGNORECASE)

    # Remove on* attributes (onclick, onload, etc.)
    html = re.sub(r'\s+on\w+="[^"]*"', "", html, flags=re.IGNORECASE)
    html = re.sub(r"\s+on\w+='[^']*'", "", html, flags=re.IGNORECASE)

    # Remove javascript: URLs
    html = re.sub(r'href="javascript:[^"]*"', 'href="#"', html, flags=re.IGNORECASE)

    return html

