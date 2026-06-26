"""SQLAlchemy adapter for ``CourseRequestRepository``.

Clusters are aggregated in the adapter (newest-first scan, grouped by the
normalized ``topic_key``) rather than in SQL, so the representative label and
ranking are computed identically across SQLite and Postgres. Course-request
volume is modest (one row per learner request) and the read is admin-only.
"""

from __future__ import annotations

from datetime import UTC, datetime

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from cyberdyne_backend.adapters.outbound.persistence.course_demand.models import (
    CourseRequestRow,
)
from cyberdyne_backend.domain.course_demand import CourseRequest, DemandCluster


def _as_utc(value: datetime) -> datetime:
    """SQLite drops tzinfo on read; re-attach UTC. Postgres is already aware."""
    if value.tzinfo is None:
        return value.replace(tzinfo=UTC)
    return value


class SqlAlchemyCourseRequestRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def add(self, request: CourseRequest) -> CourseRequest:
        self._session.add(
            CourseRequestRow(
                id=request.id,
                user_id=request.user_id,
                topic=request.topic,
                topic_key=request.topic_key,
                subject=request.subject,
                source=request.source.value,
                source_question_text=request.source_question_text,
                course_id=request.course_id,
                lesson_id=request.lesson_id,
                created_at=request.created_at,
            )
        )
        await self._session.flush()
        return request

    async def list_clusters(self) -> list[DemandCluster]:
        rows = (
            (
                await self._session.execute(
                    select(CourseRequestRow).order_by(CourseRequestRow.created_at.desc())
                )
            )
            .scalars()
            .all()
        )
        clusters: dict[str, DemandCluster] = {}
        for row in rows:  # newest-first → first row per key is the representative
            existing = clusters.get(row.topic_key)
            if existing is None:
                clusters[row.topic_key] = DemandCluster(
                    topic_key=row.topic_key,
                    topic=row.topic,
                    subject=row.subject,
                    count=1,
                    last_requested_at=_as_utc(row.created_at),
                )
            else:
                existing.count += 1
        return sorted(
            clusters.values(),
            key=lambda c: (c.count, c.last_requested_at),
            reverse=True,
        )
