"""SQLAlchemy ORM models for the blog context."""

from __future__ import annotations

from datetime import datetime
from uuid import UUID

from sqlalchemy import JSON, DateTime, ForeignKey, Index, String, Text, Uuid
from sqlalchemy.orm import Mapped, mapped_column

from cyberdyne_backend.infrastructure.database.base import Base


class BlogCategoryRow(Base):
    __tablename__ = "blog_categories"

    slug: Mapped[str] = mapped_column(String(64), primary_key=True)
    name: Mapped[str] = mapped_column(String(128), nullable=False)
    palette: Mapped[str] = mapped_column(String(32), nullable=False, default="blue")


class BlogPostRow(Base):
    __tablename__ = "blog_posts"

    id: Mapped[UUID] = mapped_column(Uuid(), primary_key=True)
    slug: Mapped[str] = mapped_column(String(128), nullable=False, unique=True, index=True)
    title: Mapped[str] = mapped_column(String(256), nullable=False)
    body_md: Mapped[str] = mapped_column(Text, nullable=False)
    excerpt: Mapped[str] = mapped_column(Text, nullable=False, default="")
    category_slug: Mapped[str | None] = mapped_column(
        String(64),
        ForeignKey("blog_categories.slug", ondelete="SET NULL"),
        nullable=True,
    )
    author_user_id: Mapped[UUID | None] = mapped_column(Uuid(), nullable=True)
    status: Mapped[str] = mapped_column(String(16), nullable=False, default="draft")
    tags: Mapped[list[str]] = mapped_column(JSON, nullable=False, default=list)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    published_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    updated_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

    __table_args__ = (
        Index("ix_blog_posts_status", "status"),
        Index("ix_blog_posts_published_at", "published_at"),
        Index("ix_blog_posts_category_slug", "category_slug"),
    )
