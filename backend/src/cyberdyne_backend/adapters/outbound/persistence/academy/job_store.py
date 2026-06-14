"""SQLAlchemy adapter for :class:`TranslationJobStore`.

Backs the durable translation-job queue (``translation_jobs`` table). The
worker calls ``claim_next`` to pick the oldest pending job and flip it to
``running`` in a single committed transaction, so two worker instances (or a
worker racing a restart) can't both run the same job — the ``running`` flip
is the claim. ``requeue_running`` resurrects jobs stranded ``running`` by a
crash/redeploy.
"""

from __future__ import annotations

import uuid
from datetime import UTC, datetime
from uuid import UUID

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from cyberdyne_backend.adapters.outbound.persistence.academy.models import TranslationJobRow
from cyberdyne_backend.application.academy import MAX_ATTEMPTS, TranslationJob


def _now() -> datetime:
    return datetime.now(UTC)


class SqlAlchemyTranslationJobStore:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def enqueue(self, course_slug: str, language: str) -> None:
        existing = (
            await self._session.execute(
                select(TranslationJobRow).where(
                    TranslationJobRow.course_slug == course_slug,
                    TranslationJobRow.language == language,
                )
            )
        ).scalar_one_or_none()
        now = _now()
        if existing is None:
            self._session.add(
                TranslationJobRow(
                    id=uuid.uuid4(),
                    course_slug=course_slug,
                    language=language,
                    status="pending",
                    attempts=0,
                    error=None,
                    created_at=now,
                    updated_at=now,
                )
            )
        else:
            # Re-enqueue: reset to pending and clear prior failure state.
            # Idempotent translation means a re-run only fills gaps.
            existing.status = "pending"
            existing.attempts = 0
            existing.error = None
            existing.updated_at = now
        await self._session.flush()

    async def claim_next(self) -> TranslationJob | None:
        row = (
            await self._session.execute(
                select(TranslationJobRow)
                .where(TranslationJobRow.status == "pending")
                .order_by(TranslationJobRow.created_at)
                .limit(1)
                .with_for_update(skip_locked=True)
            )
        ).scalar_one_or_none()
        if row is None:
            return None
        row.status = "running"
        row.updated_at = _now()
        await self._session.flush()
        return TranslationJob(
            id=row.id,
            course_slug=row.course_slug,
            language=row.language,
            attempts=row.attempts,
        )

    async def mark_done(self, job_id: UUID) -> None:
        await self._session.execute(
            update(TranslationJobRow)
            .where(TranslationJobRow.id == job_id)
            .values(status="done", error=None, updated_at=_now())
        )
        await self._session.flush()

    async def mark_failed(self, job_id: UUID, error: str) -> None:
        row = (
            await self._session.execute(
                select(TranslationJobRow).where(TranslationJobRow.id == job_id)
            )
        ).scalar_one_or_none()
        if row is None:
            return
        row.attempts += 1
        row.error = error
        # Retry until the cap, then give up so a broken course can't loop.
        row.status = "failed" if row.attempts >= MAX_ATTEMPTS else "pending"
        row.updated_at = _now()
        await self._session.flush()

    async def requeue_running(self) -> int:
        result = await self._session.execute(
            update(TranslationJobRow)
            .where(TranslationJobRow.status == "running")
            .values(status="pending", updated_at=_now())
        )
        await self._session.flush()
        # ``rowcount`` exists on the CursorResult of an UPDATE.
        return int(getattr(result, "rowcount", 0) or 0)
