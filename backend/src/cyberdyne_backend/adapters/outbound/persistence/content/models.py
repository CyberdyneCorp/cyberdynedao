"""SQLAlchemy ORM models for the content context."""

from __future__ import annotations

from datetime import datetime
from typing import Any

from sqlalchemy import JSON, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from cyberdyne_backend.infrastructure.database.base import Base


class TeamMemberRow(Base):
    """One row per teammate; ordered by ``sort_order`` then ``id``."""

    __tablename__ = "team_members"

    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    name: Mapped[str] = mapped_column(String(128), nullable=False)
    title: Mapped[str] = mapped_column(String(128), nullable=False)
    image_url: Mapped[str] = mapped_column(String(256), nullable=False)
    bio: Mapped[str] = mapped_column(Text, nullable=False)
    palette: Mapped[str] = mapped_column(String(32), nullable=False)
    tags: Mapped[list[str]] = mapped_column(JSON, nullable=False, default=list)
    sort_order: Mapped[int] = mapped_column(nullable=False, default=0)


class ContentPageRow(Base):
    """Free-form content document keyed by slug.

    Phase 1 stores the cyberdyne page payload as one big JSON blob.
    When admin authoring lands in Phase 3, individual sections can be
    promoted to dedicated tables; the slug-keyed shape stays useful
    for one-off marketing pages.
    """

    __tablename__ = "content_pages"

    slug: Mapped[str] = mapped_column(String(64), primary_key=True)
    payload: Mapped[dict[str, Any]] = mapped_column(JSON, nullable=False)
    updated_at: Mapped[datetime | None] = mapped_column(nullable=True)
