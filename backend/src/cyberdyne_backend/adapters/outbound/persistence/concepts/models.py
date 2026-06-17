"""SQLAlchemy ORM model for the concepts context."""

from __future__ import annotations

from datetime import datetime
from uuid import UUID

from sqlalchemy import JSON, DateTime, String, Text, Uuid
from sqlalchemy.orm import Mapped, mapped_column

from cyberdyne_backend.infrastructure.database.base import Base


class ConceptRow(Base):
    __tablename__ = "concepts"

    id: Mapped[UUID] = mapped_column(Uuid(), primary_key=True)
    slug: Mapped[str] = mapped_column(String(96), primary_key=False, unique=True, index=True)
    title: Mapped[str] = mapped_column(String(160), nullable=False)
    domain: Mapped[str] = mapped_column(String(64), nullable=False, index=True)
    summary: Mapped[str] = mapped_column(Text, nullable=False)
    formula: Mapped[str | None] = mapped_column(Text, nullable=True)
    # Back-links stored as JSON lists of references (lesson UUIDs as strings,
    # course slugs). Kept denormalized — the catalogue is small and the links
    # are author-curated, not queried relationally.
    related_lesson_ids: Mapped[list[str]] = mapped_column(JSON, nullable=False, default=list)
    related_course_slugs: Mapped[list[str]] = mapped_column(JSON, nullable=False, default=list)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    updated_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
