"""SQLAlchemy adapter for ``UsageCounterRepository``."""

from __future__ import annotations

import uuid
from uuid import UUID

from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from cyberdyne_backend.adapters.outbound.persistence.quota.models import UsageCounterRow
from cyberdyne_backend.domain.quota import QuotaMeter


class SqlAlchemyUsageCounterRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def current(self, *, user_id: UUID, meter: QuotaMeter, period_key: str) -> int:
        row = await self._row(user_id=user_id, meter=meter, period_key=period_key)
        return row.count if row is not None else 0

    async def increment(self, *, user_id: UUID, meter: QuotaMeter, period_key: str) -> int:
        row = await self._row(user_id=user_id, meter=meter, period_key=period_key)
        if row is None:
            row = UsageCounterRow(
                id=uuid.uuid4(),
                user_id=user_id,
                meter=meter.value,
                period_key=period_key,
                count=1,
            )
            self._session.add(row)
        else:
            row.count += 1
        await self._session.flush()
        return row.count

    async def reset(self, *, user_id: UUID, meter: QuotaMeter, period_key: str) -> int:
        result = await self._session.execute(
            delete(UsageCounterRow).where(
                UsageCounterRow.user_id == user_id,
                UsageCounterRow.meter == meter.value,
                UsageCounterRow.period_key == period_key,
            )
        )
        await self._session.flush()
        # rowcount exists on the CursorResult of a DELETE.
        return int(getattr(result, "rowcount", 0) or 0)

    async def _row(
        self, *, user_id: UUID, meter: QuotaMeter, period_key: str
    ) -> UsageCounterRow | None:
        return (
            await self._session.execute(
                select(UsageCounterRow).where(
                    UsageCounterRow.user_id == user_id,
                    UsageCounterRow.meter == meter.value,
                    UsageCounterRow.period_key == period_key,
                )
            )
        ).scalar_one_or_none()
