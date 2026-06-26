"""SQLAlchemy ORM model for the course-demand context."""

from __future__ import annotations

from datetime import datetime
from uuid import UUID

from sqlalchemy import DateTime, String, Text, Uuid
from sqlalchemy.orm import Mapped, mapped_column

from cyberdyne_backend.infrastructure.database.base import Base


class CourseRequestRow(Base):
    __tablename__ = "course_requests"

    id: Mapped[UUID] = mapped_column(Uuid(), primary_key=True)
    user_id: Mapped[UUID] = mapped_column(Uuid(), nullable=False, index=True)
    topic: Mapped[str] = mapped_column(String(256), nullable=False)
    # Normalized clustering key — the registry ranks demand by this.
    topic_key: Mapped[str] = mapped_column(String(256), nullable=False, index=True)
    subject: Mapped[str | None] = mapped_column(String(128), nullable=True)
    source: Mapped[str] = mapped_column(String(16), nullable=False)
    source_question_text: Mapped[str | None] = mapped_column(Text, nullable=True)
    course_id: Mapped[str | None] = mapped_column(String(128), nullable=True)
    lesson_id: Mapped[str | None] = mapped_column(String(128), nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, index=True
    )
