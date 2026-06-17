"""SQLAlchemy adapter for ``ActivityRepository``."""

from __future__ import annotations

from datetime import UTC, datetime
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from cyberdyne_backend.adapters.outbound.persistence.activity.models import (
    ActivityEventRow,
)
from cyberdyne_backend.domain.activity import ActivityEvent, ActivityKind


def _as_utc(value: datetime) -> datetime:
    """SQLite drops tzinfo on read; re-attach UTC. No-op on Postgres."""
    if value.tzinfo is None:
        return value.replace(tzinfo=UTC)
    return value


def _row_to_event(row: ActivityEventRow) -> ActivityEvent:
    return ActivityEvent(
        id=row.id,
        user_id=row.user_id,
        kind=ActivityKind(row.kind),
        ref=row.ref,
        occurred_at=_as_utc(row.occurred_at),
    )


class SqlAlchemyActivityRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def record(self, event: ActivityEvent) -> ActivityEvent:
        self._session.add(
            ActivityEventRow(
                id=event.id,
                user_id=event.user_id,
                kind=event.kind.value,
                ref=event.ref,
                occurred_at=event.occurred_at,
            )
        )
        await self._session.flush()
        return event

    async def list_for_user(self, user_id: UUID) -> list[ActivityEvent]:
        rows = (
            (
                await self._session.execute(
                    select(ActivityEventRow)
                    .where(ActivityEventRow.user_id == user_id)
                    .order_by(ActivityEventRow.occurred_at)
                )
            )
            .scalars()
            .all()
        )
        return [_row_to_event(r) for r in rows]
