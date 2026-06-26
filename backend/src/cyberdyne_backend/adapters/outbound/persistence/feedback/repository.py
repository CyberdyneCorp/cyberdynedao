"""SQLAlchemy adapter for ``FeedbackRepository``."""

from __future__ import annotations

from datetime import UTC, datetime

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from cyberdyne_backend.adapters.outbound.persistence.feedback.models import FeedbackRow
from cyberdyne_backend.domain.feedback import (
    Feedback,
    FeedbackKind,
    FeedbackStatus,
)


def _as_utc(value: datetime) -> datetime:
    """SQLite drops tzinfo on read; re-attach UTC. Postgres is already
    aware, so this is a no-op there."""
    if value.tzinfo is None:
        return value.replace(tzinfo=UTC)
    return value


def _row_to_feedback(row: FeedbackRow) -> Feedback:
    return Feedback(
        id=row.id,
        user_id=row.user_id,
        kind=FeedbackKind(row.kind),
        status=FeedbackStatus(row.status),
        message=row.message,
        course_id=row.course_id,
        lesson_id=row.lesson_id,
        app_version=row.app_version,
        platform=row.platform,
        created_at=_as_utc(row.created_at),
        updated_at=_as_utc(row.updated_at),
    )


class SqlAlchemyFeedbackRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def add(self, feedback: Feedback) -> Feedback:
        self._session.add(
            FeedbackRow(
                id=feedback.id,
                user_id=feedback.user_id,
                kind=feedback.kind.value,
                status=feedback.status.value,
                message=feedback.message,
                course_id=feedback.course_id,
                lesson_id=feedback.lesson_id,
                app_version=feedback.app_version,
                platform=feedback.platform,
                created_at=feedback.created_at,
                updated_at=feedback.updated_at,
            )
        )
        await self._session.flush()
        return feedback

    async def list_all(
        self,
        *,
        kind: FeedbackKind | None = None,
        status: FeedbackStatus | None = None,
    ) -> list[Feedback]:
        stmt = select(FeedbackRow).order_by(FeedbackRow.created_at.desc())
        if kind is not None:
            stmt = stmt.where(FeedbackRow.kind == kind.value)
        if status is not None:
            stmt = stmt.where(FeedbackRow.status == status.value)
        rows = (await self._session.execute(stmt)).scalars().all()
        return [_row_to_feedback(r) for r in rows]
