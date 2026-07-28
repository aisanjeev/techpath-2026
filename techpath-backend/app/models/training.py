"""Training content models: programmes, modules and reusable lecture assets.

Shape of the thing: a programme owns an ordered list of modules; a module references
lecture assets through ``training_module_assets``. Assets are *not* owned by a module —
they live in a shared library and one asset can appear in many modules. That indirection
is the whole point: content is authored once and reused, rather than re-uploaded per
module.

JSON is stored as text (matching ``Course.curriculum`` and friends) because the database
is SQLite in development and MySQL in production; neither gives us JSONB.
"""
from datetime import datetime, timezone
from typing import List, Optional

from sqlalchemy import (
    Boolean,
    DateTime,
    ForeignKey,
    Index,
    Integer,
    String,
    Text,
    UniqueConstraint,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.constants import AssetStatus, TrainingDeliveryMode
from app.models.base import Base, TimestampMixin


class TrainingProgram(Base, TimestampMixin):
    """A body of training material, optionally tied to a public Course."""

    __tablename__ = "training_programs"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    slug: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
    summary: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    # Nullable on purpose: plenty of training is delivered offline and has no public
    # course page. SET NULL so deleting a course never destroys its training content.
    course_id: Mapped[Optional[int]] = mapped_column(
        Integer, ForeignKey("courses.id", ondelete="SET NULL"), nullable=True, index=True
    )

    delivery_mode: Mapped[str] = mapped_column(
        String(20), default=TrainingDeliveryMode.OFFLINE.value, nullable=False
    )
    level: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)
    duration: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    cover_image: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    tags_json: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    status: Mapped[str] = mapped_column(
        String(50), default=AssetStatus.DRAFT.value, nullable=False, index=True
    )
    display_order: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    modules: Mapped[List["TrainingModule"]] = relationship(
        "TrainingModule",
        back_populates="program",
        cascade="all, delete-orphan",
        order_by="TrainingModule.display_order",
    )

    batches: Mapped[List["TrainingBatch"]] = relationship(  # noqa: F821
        "TrainingBatch",
        secondary="training_batch_programs",
        back_populates="programs"
    )

    def __repr__(self) -> str:
        return f"<TrainingProgram(id={self.id}, slug='{self.slug}')>"


class TrainingModule(Base, TimestampMixin):
    """An ordered unit within a programme — roughly "one lecture"."""

    __tablename__ = "training_modules"
    __table_args__ = (
        UniqueConstraint("program_id", "slug", name="uq_training_modules_program_slug"),
        Index("ix_training_modules_program_order", "program_id", "display_order"),
    )

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    program_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("training_programs.id", ondelete="CASCADE"), nullable=False
    )
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    slug: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    display_order: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    estimated_minutes: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    status: Mapped[str] = mapped_column(
        String(50), default=AssetStatus.DRAFT.value, nullable=False
    )

    program: Mapped["TrainingProgram"] = relationship(
        "TrainingProgram", back_populates="modules"
    )
    asset_links: Mapped[List["TrainingModuleAsset"]] = relationship(
        "TrainingModuleAsset",
        back_populates="module",
        cascade="all, delete-orphan",
        order_by="TrainingModuleAsset.display_order",
    )

    def __repr__(self) -> str:
        return f"<TrainingModule(id={self.id}, title='{self.title}')>"


class LectureAsset(Base, TimestampMixin):
    """One reusable block of teaching material.

    A single table with an ``asset_type`` discriminator rather than a table per type:
    the types share almost all of their columns and differ only in a small payload, and
    ``CRUDBase`` is single-table by construction. The payload column that matters is
    determined by the type's storage kind (see ``ASSET_TYPE_RULES``), and the shape of
    ``config_json`` is validated at the API edge by a discriminated union — so this
    stays flexible in the database without becoming untyped in practice.
    """

    __tablename__ = "lecture_assets"
    __table_args__ = (Index("ix_lecture_assets_type_status", "asset_type", "status"),)

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    # Unguessable public handle. Used for sandboxed bundle URLs so that an asset's
    # location can never be derived from its sequential primary key.
    public_id: Mapped[str] = mapped_column(String(36), unique=True, index=True, nullable=False)

    title: Mapped[str] = mapped_column(String(255), nullable=False)
    asset_type: Mapped[str] = mapped_column(String(50), nullable=False, index=True)
    description: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)

    # Exactly one of the following carries the payload, per the type's storage kind.
    body: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    media_file_id: Mapped[Optional[int]] = mapped_column(
        Integer, ForeignKey("media_files.id", ondelete="SET NULL"), nullable=True
    )
    external_url: Mapped[Optional[str]] = mapped_column(String(1000), nullable=True)
    config_json: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    bundle_path: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    bundle_entry: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)

    tags_json: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    status: Mapped[str] = mapped_column(
        String(50), default=AssetStatus.DRAFT.value, nullable=False
    )
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    created_by_id: Mapped[Optional[int]] = mapped_column(
        Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True
    )

    module_links: Mapped[List["TrainingModuleAsset"]] = relationship(
        "TrainingModuleAsset", back_populates="asset"
    )

    def __repr__(self) -> str:
        return f"<LectureAsset(id={self.id}, type='{self.asset_type}', title='{self.title}')>"


class TrainingModuleAsset(Base):
    """Placement of an asset within a module.

    A mapped class rather than a bare association ``Table`` because a placement carries
    its own data (ordering, whether it is required, and a per-placement trainer note —
    the same asset can warrant different notes in different modules), and because
    ``CRUDBase`` needs an ``id`` primary key.
    """

    __tablename__ = "training_module_assets"
    __table_args__ = (
        UniqueConstraint("module_id", "asset_id", name="uq_module_asset"),
        Index("ix_module_assets_module_order", "module_id", "display_order"),
    )

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    module_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("training_modules.id", ondelete="CASCADE"), nullable=False
    )
    # RESTRICT: deleting an asset that is still being taught from would silently gut
    # every module using it. The API turns this into an explicit conflict listing the
    # usages, and archiving is offered instead.
    asset_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("lecture_assets.id", ondelete="RESTRICT"), nullable=False
    )
    display_order: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    is_required: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc)
    )

    module: Mapped["TrainingModule"] = relationship(
        "TrainingModule", back_populates="asset_links"
    )
    asset: Mapped["LectureAsset"] = relationship("LectureAsset", back_populates="module_links")

    def __repr__(self) -> str:
        return f"<TrainingModuleAsset(module={self.module_id}, asset={self.asset_id})>"
