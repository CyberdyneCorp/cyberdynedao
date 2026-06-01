"""SQLAlchemy ORM models for the quizzes context."""

from __future__ import annotations

from datetime import datetime
from uuid import UUID

from sqlalchemy import (
    JSON,
    Boolean,
    DateTime,
    ForeignKey,
    Index,
    Integer,
    Text,
    Uuid,
)
from sqlalchemy.orm import Mapped, mapped_column

from cyberdyne_backend.infrastructure.database.base import Base


class QuizRow(Base):
    __tablename__ = "quizzes"

    id: Mapped[UUID] = mapped_column(Uuid(), primary_key=True)
    lesson_id: Mapped[UUID] = mapped_column(
        Uuid(),
        ForeignKey("lessons.id", ondelete="CASCADE"),
        nullable=False,
        unique=True,
        index=True,
    )
    passing_score: Mapped[int] = mapped_column(Integer, nullable=False, default=70)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    updated_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)


class QuizQuestionRow(Base):
    __tablename__ = "quiz_questions"

    id: Mapped[UUID] = mapped_column(Uuid(), primary_key=True)
    quiz_id: Mapped[UUID] = mapped_column(
        Uuid(),
        ForeignKey("quizzes.id", ondelete="CASCADE"),
        nullable=False,
    )
    prompt: Mapped[str] = mapped_column(Text, nullable=False)
    explanation: Mapped[str] = mapped_column(Text, nullable=False, default="")
    sort_order: Mapped[int] = mapped_column(Integer, nullable=False, default=0)

    __table_args__ = (Index("ix_quiz_questions_quiz_id", "quiz_id"),)


class QuizOptionRow(Base):
    __tablename__ = "quiz_options"

    id: Mapped[UUID] = mapped_column(Uuid(), primary_key=True)
    question_id: Mapped[UUID] = mapped_column(
        Uuid(),
        ForeignKey("quiz_questions.id", ondelete="CASCADE"),
        nullable=False,
    )
    text: Mapped[str] = mapped_column(Text, nullable=False)
    is_correct: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    sort_order: Mapped[int] = mapped_column(Integer, nullable=False, default=0)

    __table_args__ = (Index("ix_quiz_options_question_id", "question_id"),)


class QuizAttemptRow(Base):
    __tablename__ = "quiz_attempts"

    id: Mapped[UUID] = mapped_column(Uuid(), primary_key=True)
    user_id: Mapped[UUID] = mapped_column(Uuid(), nullable=False)
    quiz_id: Mapped[UUID] = mapped_column(
        Uuid(),
        ForeignKey("quizzes.id", ondelete="CASCADE"),
        nullable=False,
    )
    lesson_id: Mapped[UUID] = mapped_column(Uuid(), nullable=False)
    score: Mapped[int] = mapped_column(Integer, nullable=False)
    passed: Mapped[bool] = mapped_column(Boolean, nullable=False)
    attempt_number: Mapped[int] = mapped_column(Integer, nullable=False)
    answers: Mapped[dict[str, str]] = mapped_column(JSON, nullable=False, default=dict)
    submitted_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)

    __table_args__ = (Index("ix_quiz_attempts_user_quiz", "user_id", "quiz_id"),)
