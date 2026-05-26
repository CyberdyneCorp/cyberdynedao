"""SQLAlchemy adapter for ``ContentRepository``."""

from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from cyberdyne_backend.adapters.outbound.persistence.content.models import (
    ContentPageRow,
    TeamMemberRow,
)
from cyberdyne_backend.domain.content import CyberdynePage, TeamMember
from cyberdyne_backend.domain.content.ports import ContentNotFoundError


class SqlAlchemyContentRepository:
    """Reads content from Postgres via an async SQLAlchemy session."""

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def list_team(self) -> list[TeamMember]:
        result = await self._session.execute(
            select(TeamMemberRow).order_by(TeamMemberRow.sort_order, TeamMemberRow.id)
        )
        rows = result.scalars().all()
        return [
            TeamMember(
                id=row.id,
                name=row.name,
                title=row.title,
                image_url=row.image_url,
                bio=row.bio,
                tags=tuple(row.tags),
                palette=row.palette,
            )
            for row in rows
        ]

    async def get_page(self, slug: str) -> CyberdynePage:
        result = await self._session.execute(
            select(ContentPageRow).where(ContentPageRow.slug == slug)
        )
        row = result.scalar_one_or_none()
        if row is None:
            raise ContentNotFoundError(f"no content page with slug={slug!r}")
        return CyberdynePage(slug=row.slug, payload=row.payload)
