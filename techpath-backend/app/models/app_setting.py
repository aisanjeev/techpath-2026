"""App Settings model for configurable application settings stored in database."""
from typing import Optional

from sqlalchemy import String, Text, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin


class AppSetting(Base, TimestampMixin):
    """
    Application settings stored in the database.
    
    For non-sensitive configuration values that admins can change via the admin panel.
    Sensitive values (API keys, connection strings) should be in Key Vault instead.
    """

    __tablename__ = "app_settings"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    
    # Setting identification
    key: Mapped[str] = mapped_column(
        String(100), unique=True, index=True, nullable=False,
        comment="Setting key, e.g., 'admin_notification_email'"
    )
    value: Mapped[Optional[str]] = mapped_column(
        Text, nullable=True,
        comment="Setting value"
    )
    
    # Metadata for admin UI
    display_name: Mapped[str] = mapped_column(
        String(200), nullable=False,
        comment="Human-readable name for the UI"
    )
    description: Mapped[Optional[str]] = mapped_column(
        Text, nullable=True,
        comment="Description of what this setting does"
    )
    category: Mapped[str] = mapped_column(
        String(50), nullable=False, index=True,
        comment="Category: email, general, notifications, etc."
    )
    
    # Value type for validation
    value_type: Mapped[str] = mapped_column(
        String(20), default="string", nullable=False,
        comment="Type: string, email, number, boolean, json"
    )
    
    # Display order within category
    display_order: Mapped[int] = mapped_column(
        Integer, default=0, nullable=False,
        comment="Order for display in UI"
    )
    
    # Audit trail
    updated_by_id: Mapped[Optional[int]] = mapped_column(
        Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True
    )
    
    updated_by = relationship("User", foreign_keys=[updated_by_id])

    def __repr__(self) -> str:
        return f"<AppSetting(key='{self.key}', value='{self.value[:20] if self.value else None}...')>"

