"""SQLAlchemy ORM models for the courses context."""

from __future__ import annotations

from datetime import datetime
from uuid import UUID

from sqlalchemy import (
    Boolean,
    DateTime,
    ForeignKey,
    Index,
    Integer,
    String,
    Text,
    UniqueConstraint,
    Uuid,
)
from sqlalchemy.orm import Mapped, mapped_column

from cyberdyne_backend.infrastructure.database.base import Base


class CourseRow(Base):
    __tablename__ = "courses"

    id: Mapped[UUID] = mapped_column(Uuid(), primary_key=True)
    slug: Mapped[str] = mapped_column(String(128), nullable=False, unique=True, index=True)
    title: Mapped[str] = mapped_column(String(256), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False, default="")
    level: Mapped[str] = mapped_column(String(32), nullable=False)
    status: Mapped[str] = mapped_column(String(16), nullable=False, default="draft")
    mandatory: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    sort_order: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    published_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    updated_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    due_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

    __table_args__ = (
        Index("ix_courses_level", "level"),
        Index("ix_courses_status", "status"),
    )


class LessonRow(Base):
    __tablename__ = "lessons"

    id: Mapped[UUID] = mapped_column(Uuid(), primary_key=True)
    course_id: Mapped[UUID] = mapped_column(
        Uuid(),
        ForeignKey("courses.id", ondelete="CASCADE"),
        nullable=False,
    )
    title: Mapped[str] = mapped_column(String(256), nullable=False)
    lesson_type: Mapped[str] = mapped_column(String(16), nullable=False)
    content_url: Mapped[str | None] = mapped_column(Text, nullable=True)
    text_body: Mapped[str | None] = mapped_column(Text, nullable=True)
    duration: Mapped[str | None] = mapped_column(String(32), nullable=True)
    sort_order: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    updated_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

    __table_args__ = (Index("ix_lessons_course_id", "course_id"),)


class LessonProgressRow(Base):
    """A learner's progress through one lesson (courses context)."""

    __tablename__ = "lesson_progress"

    id: Mapped[UUID] = mapped_column(Uuid(), primary_key=True)
    user_id: Mapped[UUID] = mapped_column(Uuid(), nullable=False)
    course_id: Mapped[UUID] = mapped_column(
        Uuid(),
        ForeignKey("courses.id", ondelete="CASCADE"),
        nullable=False,
    )
    lesson_id: Mapped[UUID] = mapped_column(
        Uuid(),
        ForeignKey("lessons.id", ondelete="CASCADE"),
        nullable=False,
    )
    percent: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    started_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    completed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    updated_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

    __table_args__ = (
        UniqueConstraint("user_id", "lesson_id", name="uq_lesson_progress_user_lesson"),
        Index("ix_lesson_progress_user_course", "user_id", "course_id"),
    )


class CourseCertificateRow(Base):
    """A learner's completion certificate for a course (one per pair)."""

    __tablename__ = "course_certificates"
    __table_args__ = (
        UniqueConstraint("user_id", "course_slug", name="uq_course_cert_user_course"),
    )

    id: Mapped[UUID] = mapped_column(Uuid(), primary_key=True)
    user_id: Mapped[UUID] = mapped_column(Uuid(), nullable=False, index=True)
    course_slug: Mapped[str] = mapped_column(String(128), nullable=False)
    issued_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    verification_hash: Mapped[str] = mapped_column(String(128), nullable=False)
    signed_payload: Mapped[str] = mapped_column(Text, nullable=False)
