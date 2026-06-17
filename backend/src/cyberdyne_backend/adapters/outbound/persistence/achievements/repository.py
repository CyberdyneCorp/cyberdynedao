"""SQLAlchemy adapter for ``AchievementRepository``."""

from __future__ import annotations

import uuid
from datetime import UTC, datetime
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from cyberdyne_backend.adapters.outbound.persistence.achievements.models import (
    UserAchievementRow,
)


def _as_utc(value: datetime) -> datetime:
    if value.tzinfo is None:
        return value.replace(tzinfo=UTC)
    return value


class SqlAlchemyAchievementRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def list_earned(self, user_id: UUID) -> dict[str, datetime]:
        rows = (
            (
                await self._session.execute(
                    select(UserAchievementRow).where(UserAchievementRow.user_id == user_id)
                )
            )
            .scalars()
            .all()
        )
        return {r.key: _as_utc(r.earned_at) for r in rows}

    async def record_earned(self, *, user_id: UUID, key: str, earned_at: datetime) -> None:
        existing = (
            await self._session.execute(
                select(UserAchievementRow).where(
                    UserAchievementRow.user_id == user_id,
                    UserAchievementRow.key == key,
                )
            )
        ).scalar_one_or_none()
        if existing is not None:
            return
        self._session.add(
            UserAchievementRow(
                id=uuid.uuid4(),
                user_id=user_id,
                key=key,
                earned_at=earned_at,
            )
        )
        await self._session.flush()
