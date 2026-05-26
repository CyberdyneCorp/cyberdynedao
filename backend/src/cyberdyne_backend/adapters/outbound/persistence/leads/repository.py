"""SQLAlchemy adapter for ``AskRepository``."""

from __future__ import annotations

from uuid import UUID

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from cyberdyne_backend.adapters.outbound.persistence.leads.models import (
    AskEventRow,
    AskRow,
)
from cyberdyne_backend.domain.leads import (
    Ask,
    AskChannel,
    AskEvent,
    AskEventKind,
    AskNotFoundError,
    AskStatus,
)


def _row_to_event(row: AskEventRow) -> AskEvent:
    return AskEvent(
        id=row.id,
        ask_id=row.ask_id,
        kind=AskEventKind(row.kind),
        by_user_id=row.by_user_id,
        payload=dict(row.payload or {}),
        at=row.at,
    )


def _row_to_ask(row: AskRow, events: list[AskEvent]) -> Ask:
    return Ask(
        id=row.id,
        channel=AskChannel(row.channel),
        name=row.name,
        email=row.email,
        body=row.body,
        product_slug=row.product_slug,
        source_url=row.source_url,
        status=AskStatus(row.status),
        owner_user_id=row.owner_user_id,
        notes_md=row.notes_md,
        created_at=row.created_at,
        events=events,
    )


class SqlAlchemyAskRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def save(self, ask: Ask) -> None:
        # Upsert the Ask row, then flush so the FK from ask_events ->
        # asks.id resolves before any new events get inserted in the
        # same transaction.
        existing = await self._session.get(AskRow, ask.id)
        if existing is None:
            self._session.add(
                AskRow(
                    id=ask.id,
                    channel=ask.channel.value,
                    name=ask.name,
                    email=ask.email,
                    body=ask.body,
                    product_slug=ask.product_slug,
                    source_url=ask.source_url,
                    status=ask.status.value,
                    owner_user_id=ask.owner_user_id,
                    notes_md=ask.notes_md,
                    created_at=ask.created_at,
                )
            )
        else:
            existing.status = ask.status.value
            existing.owner_user_id = ask.owner_user_id
            existing.notes_md = ask.notes_md
        await self._session.flush()

        # Insert any new events. Skipping ones we've already persisted
        # by checking the id (events are immutable once written).
        already_persisted = (
            (
                await self._session.execute(
                    select(AskEventRow.id).where(AskEventRow.ask_id == ask.id)
                )
            )
            .scalars()
            .all()
        )
        existing_ids = set(already_persisted)
        for evt in ask.events:
            if evt.id in existing_ids:
                continue
            self._session.add(
                AskEventRow(
                    id=evt.id,
                    ask_id=evt.ask_id,
                    kind=evt.kind.value,
                    by_user_id=evt.by_user_id,
                    payload=evt.payload,
                    at=evt.at,
                )
            )
        await self._session.flush()

    async def get(self, ask_id: UUID) -> Ask:
        row = await self._session.get(AskRow, ask_id)
        if row is None:
            raise AskNotFoundError(f"no ask with id={ask_id}")
        evt_rows = (
            (
                await self._session.execute(
                    select(AskEventRow)
                    .where(AskEventRow.ask_id == ask_id)
                    .order_by(AskEventRow.at, AskEventRow.id)
                )
            )
            .scalars()
            .all()
        )
        return _row_to_ask(row, [_row_to_event(r) for r in evt_rows])

    async def list_admin(
        self,
        *,
        status: AskStatus | None = None,
        channel: str | None = None,
        query: str | None = None,
        page: int = 1,
        page_size: int = 50,
    ) -> tuple[list[Ask], int]:
        stmt = select(AskRow)
        count_stmt = select(func.count(AskRow.id))
        if status is not None:
            stmt = stmt.where(AskRow.status == status.value)
            count_stmt = count_stmt.where(AskRow.status == status.value)
        if channel:
            stmt = stmt.where(AskRow.channel == channel)
            count_stmt = count_stmt.where(AskRow.channel == channel)
        if query:
            ilike = f"%{query}%"
            stmt = stmt.where(
                (AskRow.name.ilike(ilike))
                | (AskRow.email.ilike(ilike))
                | (AskRow.body.ilike(ilike))
            )
            count_stmt = count_stmt.where(
                (AskRow.name.ilike(ilike))
                | (AskRow.email.ilike(ilike))
                | (AskRow.body.ilike(ilike))
            )

        total = (await self._session.execute(count_stmt)).scalar_one()
        stmt = (
            stmt.order_by(AskRow.created_at.desc())
            .offset(max(0, (page - 1) * page_size))
            .limit(page_size)
        )
        rows = (await self._session.execute(stmt)).scalars().all()
        # Skip loading events for list view — they're lazy-loaded on detail.
        return [_row_to_ask(r, []) for r in rows], total
