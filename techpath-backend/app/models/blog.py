"""Blog models for posts and tags."""
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
    featured_image: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    author_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True
    )
    status: Mapped[str] = mapped_column(String(50), default="draft", nullable=False)
    featured: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    reading_time: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)  # in minutes
    published_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    meta_title: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    meta_description: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)

    # Relationships
    tags: Mapped[List[BlogTag]] = relationship(
        "BlogTag",
        secondary=blog_post_tags,
        back_populates="posts",
    )

    def __repr__(self) -> str:
        return f"<BlogPost(id={self.id}, title='{self.title}', status='{self.status}')>"

