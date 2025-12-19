"""Blog models for posts, tags, and categories."""
from datetime import datetime
from typing import List, Optional

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String, Table, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin


# Association table for many-to-many relationship between posts and tags
blog_post_tags = Table(
    "blog_post_tags",
    Base.metadata,
    Column("post_id", Integer, ForeignKey("blog_posts.id", ondelete="CASCADE"), primary_key=True),
    Column("tag_id", Integer, ForeignKey("blog_tags.id", ondelete="CASCADE"), primary_key=True),
)


class BlogCategory(Base, TimestampMixin):
    """Blog category model with hierarchical support."""

    __tablename__ = "blog_categories"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    slug: Mapped[str] = mapped_column(String(100), unique=True, index=True, nullable=False)
    description: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    parent_id: Mapped[Optional[int]] = mapped_column(
        Integer, ForeignKey("blog_categories.id", ondelete="SET NULL"), nullable=True
    )
    display_order: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    # Self-referential relationships for hierarchy
    parent: Mapped[Optional["BlogCategory"]] = relationship(
        "BlogCategory",
        remote_side="BlogCategory.id",
        back_populates="children",
    )
    children: Mapped[List["BlogCategory"]] = relationship(
        "BlogCategory",
        back_populates="parent",
        cascade="all, delete-orphan",
    )

    # Relationship to posts
    posts: Mapped[List["BlogPost"]] = relationship(
        "BlogPost",
        back_populates="category",
    )

    def __repr__(self) -> str:
        return f"<BlogCategory(id={self.id}, name='{self.name}')>"

    @property
    def full_path(self) -> str:
        """Get full category path (e.g., 'Technology > AI > Machine Learning')."""
        if self.parent:
            return f"{self.parent.full_path} > {self.name}"
        return self.name

    @property
    def level(self) -> int:
        """Get the depth level of this category (0 = root, 1 = child, etc.)."""
        if self.parent:
            return self.parent.level + 1
        return 0


class BlogTag(Base):
    """Blog tag model."""

    __tablename__ = "blog_tags"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    slug: Mapped[str] = mapped_column(String(100), unique=True, index=True, nullable=False)

    # Relationship to posts
    posts: Mapped[List["BlogPost"]] = relationship(
        "BlogPost",
        secondary=blog_post_tags,
        back_populates="tags",
    )

    def __repr__(self) -> str:
        return f"<BlogTag(id={self.id}, name='{self.name}')>"


class BlogPost(Base, TimestampMixin):
    """Blog post model."""

    __tablename__ = "blog_posts"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    slug: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
    excerpt: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    content_type: Mapped[str] = mapped_column(String(20), default="html", nullable=False)
    featured_image: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    author_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True
    )
    category_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("blog_categories.id", ondelete="RESTRICT"), nullable=False
    )
    status: Mapped[str] = mapped_column(String(50), default="draft", nullable=False)
    featured: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    reading_time: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)  # in minutes
    published_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    meta_title: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    meta_description: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)

    # Relationships
    category: Mapped["BlogCategory"] = relationship(
        "BlogCategory",
        back_populates="posts",
    )
    tags: Mapped[List[BlogTag]] = relationship(
        "BlogTag",
        secondary=blog_post_tags,
        back_populates="posts",
    )

    def __repr__(self) -> str:
        return f"<BlogPost(id={self.id}, title='{self.title}', status='{self.status}')>"
