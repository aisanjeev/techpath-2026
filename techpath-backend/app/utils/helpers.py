"""Utility helper functions."""
import re
import unicodedata
from datetime import datetime, timezone


def generate_slug(text: str) -> str:
    """
    Generate a URL-friendly slug from text.

    Args:
        text: Input text to convert to slug

    Returns:
        URL-friendly slug string
    """
    # Normalize unicode characters
    text = unicodedata.normalize("NFKD", text)
    text = text.encode("ascii", "ignore").decode("ascii")

    # Convert to lowercase
    text = text.lower()

    # Replace spaces and underscores with hyphens
    text = re.sub(r"[\s_]+", "-", text)

    # Remove non-alphanumeric characters except hyphens
    text = re.sub(r"[^a-z0-9-]", "", text)

    # Remove multiple consecutive hyphens
    text = re.sub(r"-+", "-", text)

    # Remove leading/trailing hyphens
    text = text.strip("-")

    return text


def get_utc_now() -> datetime:
    """Get current UTC datetime with timezone info."""
    return datetime.now(timezone.utc)


def calculate_reading_time(content: str, words_per_minute: int = 200) -> int:
    """
    Calculate estimated reading time for content.

    Args:
        content: Text content
        words_per_minute: Reading speed (default: 200 wpm)

    Returns:
        Estimated reading time in minutes
    """
    # Remove HTML tags if present
    clean_content = re.sub(r"<[^>]+>", "", content)

    # Count words
    words = len(clean_content.split())

    # Calculate reading time (minimum 1 minute)
    reading_time = max(1, round(words / words_per_minute))

    return reading_time


def truncate_text(text: str, max_length: int = 200, suffix: str = "...") -> str:
    """
    Truncate text to a maximum length.

    Args:
        text: Text to truncate
        max_length: Maximum length
        suffix: Suffix to add if truncated

    Returns:
        Truncated text
    """
    if len(text) <= max_length:
        return text

    # Find last space before max_length
    truncated = text[: max_length - len(suffix)]
    last_space = truncated.rfind(" ")

    if last_space > 0:
        truncated = truncated[:last_space]

    return truncated + suffix


def sanitize_filename(filename: str) -> str:
    """
    Sanitize a filename for safe storage.

    Args:
        filename: Original filename

    Returns:
        Sanitized filename
    """
    # Get file extension
    parts = filename.rsplit(".", 1)
    name = parts[0]
    ext = parts[1] if len(parts) > 1 else ""

    # Generate slug from name
    safe_name = generate_slug(name)

    # Limit length
    safe_name = safe_name[:50]

    # Add extension back
    if ext:
        return f"{safe_name}.{ext.lower()}"
    return safe_name

