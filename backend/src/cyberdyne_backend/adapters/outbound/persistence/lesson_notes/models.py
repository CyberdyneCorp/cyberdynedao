"""SQLAlchemy ORM model for the lesson-notes context."""

from __future__ import annotations

from datetime import datetime
from uuid import UUID

from sqlalchemy import DateTime, Index, String, Text, Uuid
from sqlalchemy.orm import Mapped, mapped_column

from cyberdyne_backend.infrastructure.database.base import Base


class LessonNoteRow(Base):
    __tablename__ = "lesson_notes"

    id: Mapped[UUID] = mapped_column(Uuid(), primary_key=True)
    user_id: Mapped[UUID] = mapped_column(Uuid(), nullable=False, index=True)
    course_slug: Mapped[str] = mapped_column(String(128), nullable=False)
    lesson_id: Mapped[str] = mapped_column(String(128), nullable=False)
    quote: Mapped[str | None] = mapped_column(Text, nullable=True)
    body: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    updated_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

    __table_args__ = (
        # The two list paths: by lesson, and by user/course newest-first.
        Index("ix_lesson_notes_user_lesson", "user_id", "lesson_id"),
        Index("ix_lesson_notes_user_course_created", "user_id", "course_slug", "created_at"),
    )
