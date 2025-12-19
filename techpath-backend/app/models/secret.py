"""Secret metadata model for tracking secrets stored in Key Vault."""
from typing import Optional

from sqlalchemy import Boolean, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin


class SecretMetadata(Base, TimestampMixin):
    """
    Metadata for secrets stored in Azure Key Vault.
    
    The actual secret values are stored in Key Vault, not in this table.
    This table only tracks metadata for the admin UI.
    """

    __tablename__ = "secret_metadata"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    
    # Secret identification
    key_name: Mapped[str] = mapped_column(
        String(100), unique=True, index=True, nullable=False,
        comment="Environment variable name, e.g., AZURE_OPENAI_KEY"
    )
    display_name: Mapped[str] = mapped_column(
        String(200), nullable=False,
        comment="Human-readable name for the UI"
    )
    description: Mapped[Optional[str]] = mapped_column(
        Text, nullable=True,
        comment="Description of what this secret is used for"
    )
    
    # Categorization
    category: Mapped[str] = mapped_column(
        String(50), nullable=False, index=True,
        comment="Category: azure_openai, storage, email, etc."
    )
    
    # Status flags
    is_required: Mapped[bool] = mapped_column(
        Boolean, default=False, nullable=False,
        comment="Whether this secret is required for the app to function"
    )
    is_set: Mapped[bool] = mapped_column(
        Boolean, default=False, nullable=False,
        comment="Whether the secret has been set in Key Vault"
    )
    
    # Display order within category
    display_order: Mapped[int] = mapped_column(
        Integer, default=0, nullable=False,
        comment="Order for display in UI"
    )
    
    # Audit trail
    updated_by_id: Mapped[Optional[int]] = mapped_column(
        Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True,
        comment="Last user who updated this secret"
    )
    
    # Relationship to user
    updated_by = relationship("User", foreign_keys=[updated_by_id])

    def __repr__(self) -> str:
        return f"<SecretMetadata(key='{self.key_name}', category='{self.category}', is_set={self.is_set})>"

