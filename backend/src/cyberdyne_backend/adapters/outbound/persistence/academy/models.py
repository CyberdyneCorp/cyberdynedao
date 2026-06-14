"""SQLAlchemy ORM models for the academy (cross-context) persistence.

The translation tables themselves live with the courses/quizzes models;
this module owns the durable translation-job queue that drives them.
"""

from __future__ import annotations

from datetime import datetime
from uuid import UUID

from sqlalchemy import DateTime, Index, Integer, String, Text, UniqueConstraint, Uuid
from sqlalchemy.orm import Mapped, mapped_column

from cyberdyne_backend.infrastructure.database.base import Base


class TranslationJobRow(Base):
    """One queued translate-a-course-into-a-language job.

    A restart-safe replacement for the old in-process background task: the
    worker claims rows here, so a redeploy that kills a running translation
    leaves a durable record that ``requeue_running`` resurrects on startup.
    ``status`` is plain text (not a DB enum) for SQLite-test compatibility
    and to match the rest of the schema.
    """

    __tablename__ = "translation_jobs"
    __table_args__ = (
        UniqueConstraint("course_slug", "language", name="uq_translation_jobs_slug_lang"),
        Index("ix_translation_jobs_status_created", "status", "created_at"),
    )

    id: Mapped[UUID] = mapped_column(Uuid(), primary_key=True)
    course_slug: Mapped[str] = mapped_column(String(128), nullable=False)
    language: Mapped[str] = mapped_column(String(8), nullable=False)
    status: Mapped[str] = mapped_column(String(16), nullable=False, default="pending")
    attempts: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    error: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
