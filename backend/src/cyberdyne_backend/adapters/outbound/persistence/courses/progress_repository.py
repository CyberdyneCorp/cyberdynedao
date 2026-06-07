"""SQLAlchemy adapter for ``CourseProgressRepository``."""

from __future__ import annotations

from datetime import UTC, datetime
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from cyberdyne_backend.adapters.outbound.persistence.courses.models import (
    LessonProgressRow,
    LessonRow,
)
from cyberdyne_backend.domain.courses.progress import LessonProgress


def _as_utc(value: datetime | None) -> datetime | None:
    """SQLite drops tzinfo on read; re-attach UTC so domain comparisons
    against an aware ``now`` don't blow up. Postgres rows are already
    aware, so this is a no-op there."""
    if value is not None and value.tzinfo is None:
        return value.replace(tzinfo=UTC)
    return value


def _row_to_progress(row: LessonProgressRow) -> LessonProgress:
    started = _as_utc(row.started_at)
    assert started is not None  # NOT NULL column
    return LessonProgress(
        id=row.id,
        user_id=row.user_id,
        course_id=row.course_id,
        lesson_id=row.lesson_id,
        percent=row.percent,
        started_at=started,
        completed_at=_as_utc(row.completed_at),
        updated_at=_as_utc(row.updated_at),
    )


class SqlAlchemyCourseProgressRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_lesson_progress(self, *, user_id: UUID, lesson_id: UUID) -> LessonProgress | None:
        result = await self._session.execute(
            select(LessonProgressRow).where(
                LessonProgressRow.user_id == user_id,
                LessonProgressRow.lesson_id == lesson_id,
            )
        )
        row = result.scalar_one_or_none()
        return _row_to_progress(row) if row is not None else None

    async def upsert_lesson_progress(self, progress: LessonProgress) -> None:
        existing = await self._session.get(LessonProgressRow, progress.id)
        if existing is None:
            self._session.add(
                LessonProgressRow(
                    id=progress.id,
                    user_id=progress.user_id,
                    course_id=progress.course_id,
                    lesson_id=progress.lesson_id,
                    percent=progress.percent,
                    started_at=progress.started_at,
                    completed_at=progress.completed_at,
                    updated_at=progress.updated_at,
                )
            )
        else:
            existing.percent = progress.percent
            existing.completed_at = progress.completed_at
            existing.updated_at = progress.updated_at
        await self._session.flush()

    async def list_course_progress(self, *, user_id: UUID, course_id: UUID) -> list[LessonProgress]:
        result = await self._session.execute(
            select(LessonProgressRow).where(
                LessonProgressRow.user_id == user_id,
                LessonProgressRow.course_id == course_id,
            )
        )
        return [_row_to_progress(row) for row in result.scalars().all()]

    async def list_all_progress_for_user(self, *, user_id: UUID) -> list[LessonProgress]:
        result = await self._session.execute(
            select(LessonProgressRow).where(LessonProgressRow.user_id == user_id)
        )
        return [_row_to_progress(row) for row in result.scalars().all()]

    async def get_lesson_course_id(self, lesson_id: UUID) -> UUID | None:
        result = await self._session.execute(
            select(LessonRow.course_id).where(LessonRow.id == lesson_id)
        )
        return result.scalar_one_or_none()
