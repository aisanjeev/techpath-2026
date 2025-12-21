"""Media file models for centralized file management."""
from datetime import datetime
from typing import List, Optional

from sqlalchemy import String, Integer, DateTime, ForeignKey, Index, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base


class MediaFile(Base):
    """Model for storing media file metadata with deduplication support."""

    __tablename__ = "media_files"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    filename: Mapped[str] = mapped_column(String(255), nullable=False)
    stored_path: Mapped[str] = mapped_column(String(500), nullable=False, unique=True)
    file_hash: Mapped[str] = mapped_column(String(64), nullable=False, index=True)
    content_type: Mapped[str] = mapped_column(String(100), nullable=False)
    size: Mapped[int] = mapped_column(Integer, nullable=False)
    width: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    height: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    alt_text: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=func.now(), onupdate=func.now(), nullable=False
    )

    # Relationships
    usages: Mapped[List["MediaFileUsage"]] = relationship(
        "MediaFileUsage", back_populates="file", cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"<MediaFile(id={self.id}, filename={self.filename})>"


class MediaFileUsage(Base):
    """Model for tracking where media files are used."""

    __tablename__ = "media_file_usages"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    file_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("media_files.id", ondelete="CASCADE"), nullable=False
    )
    entity_type: Mapped[str] = mapped_column(String(50), nullable=False)
    entity_id: Mapped[int] = mapped_column(Integer, nullable=False)
    field_name: Mapped[str] = mapped_column(String(50), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=func.now(), nullable=False
    )

    # Relationships
    file: Mapped["MediaFile"] = relationship("MediaFile", back_populates="usages")

    # Composite index for efficient lookups
    __table_args__ = (
        Index("ix_media_file_usages_entity", "entity_type", "entity_id"),
        Index("ix_media_file_usages_file_entity", "file_id", "entity_type", "entity_id"),
    )

    def __repr__(self) -> str:
        return f"<MediaFileUsage(file_id={self.file_id}, entity={self.entity_type}:{self.entity_id})>"

