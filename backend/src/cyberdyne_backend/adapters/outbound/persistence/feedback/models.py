"""SQLAlchemy ORM model for the learner-feedback context."""

from __future__ import annotations

from datetime import datetime
from uuid import UUID

from sqlalchemy import DateTime, Index, String, Text, Uuid
from sqlalchemy.orm import Mapped, mapped_column

from cyberdyne_backend.infrastructure.database.base import Base


class FeedbackRow(Base):
    __tablename__ = "feedback"
    __table_args__ = (Index("ix_feedback_kind_status", "kind", "status"),)

    id: Mapped[UUID] = mapped_column(Uuid(), primary_key=True)
    user_id: Mapped[UUID] = mapped_column(Uuid(), nullable=False, index=True)
    kind: Mapped[str] = mapped_column(String(16), nullable=False)
    status: Mapped[str] = mapped_column(String(16), nullable=False)
    message: Mapped[str] = mapped_column(Text, nullable=False)
    course_id: Mapped[str | None] = mapped_column(String(128), nullable=True)
    lesson_id: Mapped[str | None] = mapped_column(String(128), nullable=True)
    app_version: Mapped[str | None] = mapped_column(String(64), nullable=True)
    platform: Mapped[str | None] = mapped_column(String(32), nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, index=True
    )
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
