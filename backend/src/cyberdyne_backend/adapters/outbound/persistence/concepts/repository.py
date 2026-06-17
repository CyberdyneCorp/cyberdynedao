"""SQLAlchemy adapter for ``ConceptRepository``."""

from __future__ import annotations

import base64
import binascii
from datetime import UTC, datetime
from uuid import UUID

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from cyberdyne_backend.adapters.outbound.persistence.concepts.models import ConceptRow
from cyberdyne_backend.domain.concepts import (
    Concept,
    ConceptNotFoundError,
    ConceptPage,
    DuplicateConceptError,
)


def _as_utc(value: datetime | None) -> datetime | None:
    if value is not None and value.tzinfo is None:
        return value.replace(tzinfo=UTC)
    return value


def _encode_cursor(slug: str) -> str:
    return base64.urlsafe_b64encode(slug.encode()).decode("ascii")


def _decode_cursor(cursor: str) -> str | None:
    try:
        return base64.urlsafe_b64decode(cursor.encode("ascii")).decode()
    except (ValueError, binascii.Error, UnicodeDecodeError):
        return None


def _row_to_concept(row: ConceptRow) -> Concept:
    return Concept(
        id=row.id,
        slug=row.slug,
        title=row.title,
        domain=row.domain,
        summary=row.summary,
        formula=row.formula,
        related_lesson_ids=tuple(UUID(x) for x in row.related_lesson_ids),
        related_course_slugs=tuple(row.related_course_slugs),
        created_at=_as_utc(row.created_at) or row.created_at,
        updated_at=_as_utc(row.updated_at),
    )


class SqlAlchemyConceptRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def _row_for_slug(self, slug: str) -> ConceptRow | None:
        return (
            await self._session.execute(select(ConceptRow).where(ConceptRow.slug == slug))
        ).scalar_one_or_none()

    async def get_by_slug(self, slug: str) -> Concept:
        row = await self._row_for_slug(slug)
        if row is None:
            raise ConceptNotFoundError(f"concept {slug!r} not found")
        return _row_to_concept(row)

    async def list_concepts(
        self,
        *,
        query: str | None = None,
        domain: str | None = None,
        cursor: str | None = None,
        limit: int = 20,
    ) -> ConceptPage:
        stmt = select(ConceptRow).order_by(ConceptRow.slug).limit(limit + 1)
        if domain is not None:
            stmt = stmt.where(ConceptRow.domain == domain)
        if query:
            needle = f"%{query.lower()}%"
            stmt = stmt.where(
                func.lower(ConceptRow.title).like(needle)
                | func.lower(ConceptRow.summary).like(needle)
            )
        if cursor is not None:
            decoded = _decode_cursor(cursor)
            if decoded is not None:
                stmt = stmt.where(ConceptRow.slug > decoded)

        rows = (await self._session.execute(stmt)).scalars().all()
        has_more = len(rows) > limit
        page = rows[:limit]
        items = [_row_to_concept(r) for r in page]
        next_cursor = _encode_cursor(items[-1].slug) if has_more and items else None
        return ConceptPage(items=items, next_cursor=next_cursor)

    async def create(self, concept: Concept) -> Concept:
        if await self._row_for_slug(concept.slug) is not None:
            raise DuplicateConceptError(f"concept {concept.slug!r} already exists")
        self._session.add(_concept_to_row(concept))
        await self._session.flush()
        return concept

    async def update(self, concept: Concept) -> Concept:
        row = await self._row_for_slug(concept.slug)
        if row is None:
            raise ConceptNotFoundError(f"concept {concept.slug!r} not found")
        row.title = concept.title
        row.domain = concept.domain
        row.summary = concept.summary
        row.formula = concept.formula
        row.related_lesson_ids = [str(x) for x in concept.related_lesson_ids]
        row.related_course_slugs = list(concept.related_course_slugs)
        row.updated_at = concept.updated_at
        await self._session.flush()
        return concept

    async def delete(self, slug: str) -> None:
        row = await self._row_for_slug(slug)
        if row is None:
            raise ConceptNotFoundError(f"concept {slug!r} not found")
        await self._session.delete(row)
        await self._session.flush()


def _concept_to_row(concept: Concept) -> ConceptRow:
    return ConceptRow(
        id=concept.id,
        slug=concept.slug,
        title=concept.title,
        domain=concept.domain,
        summary=concept.summary,
        formula=concept.formula,
        related_lesson_ids=[str(x) for x in concept.related_lesson_ids],
        related_course_slugs=list(concept.related_course_slugs),
        created_at=concept.created_at,
        updated_at=concept.updated_at,
    )
