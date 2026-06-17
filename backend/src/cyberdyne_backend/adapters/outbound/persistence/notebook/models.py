"""SQLAlchemy ORM model for the notebook context."""

from __future__ import annotations

from datetime import datetime
from uuid import UUID

from sqlalchemy import JSON, DateTime, ForeignKey, Index, Integer, String, Text, Uuid
from sqlalchemy.orm import Mapped, mapped_column

from cyberdyne_backend.infrastructure.database.base import Base


class NoteRow(Base):
    __tablename__ = "notebook_notes"

    id: Mapped[UUID] = mapped_column(Uuid(), primary_key=True)
    user_id: Mapped[UUID] = mapped_column(Uuid(), nullable=False, index=True)
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    type: Mapped[str] = mapped_column(String(16), nullable=False)
    body: Mapped[str] = mapped_column(Text, nullable=False, default="")
    course_slug: Mapped[str | None] = mapped_column(String(128), nullable=True)
    lesson_id: Mapped[UUID | None] = mapped_column(Uuid(), nullable=True)
    code: Mapped[str | None] = mapped_column(Text, nullable=True)
    language: Mapped[str | None] = mapped_column(String(32), nullable=True)
    run_result: Mapped[dict[str, object] | None] = mapped_column(JSON, nullable=True)
    plot_refs: Mapped[list[str]] = mapped_column(JSON, nullable=False, default=list)
    tags: Mapped[list[str]] = mapped_column(JSON, nullable=False, default=list)
    reviewed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    next_review_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    review_interval_days: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    ai_summary: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    updated_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

    __table_args__ = (
        # Newest-first listing per user is the hot path.
        Index("ix_notebook_notes_user_created", "user_id", "created_at"),
        # Due-for-review lookups (`?due=true`).
        Index("ix_notebook_notes_user_next_review", "user_id", "next_review_at"),
    )


class FlashcardRow(Base):
    __tablename__ = "notebook_flashcards"

    id: Mapped[UUID] = mapped_column(Uuid(), primary_key=True)
    note_id: Mapped[UUID] = mapped_column(
        Uuid(),
        ForeignKey("notebook_notes.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    question: Mapped[str] = mapped_column(Text, nullable=False)
    answer: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
