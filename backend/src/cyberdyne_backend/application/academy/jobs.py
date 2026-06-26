"""Durable, restart-safe translation jobs.

The per-course translate endpoint used to run the (many-LLM-call)
translation inside a FastAPI ``BackgroundTask`` — an in-process coroutine
that is killed whenever the container restarts or redeploys, truncating a
course's lesson translations. This module replaces that with a database-
backed job queue drained by a long-lived worker:

* :class:`TranslationJobStore` — outbound port over the ``translation_jobs``
  table. ``enqueue`` upserts a ``(slug, language)`` job to ``pending``;
  ``claim_next`` atomically picks the oldest pending job and marks it
  ``running``; ``mark_done`` / ``mark_failed`` close it out;
  ``requeue_running`` resets stranded ``running`` jobs back to ``pending``
  on startup so a job interrupted by a restart resumes.
* :class:`TranslationWorker` — application-layer loop that claims a job,
  runs the existing :class:`TranslateCourse` use case, and records the
  outcome. Idempotent by design: :class:`TranslateCourse` skips unchanged
  content by ``source_hash``, so a requeued (partially-done) job simply
  fills the gaps.

The worker owns its OWN DB session + LLM (a fresh use case per job), never a
request-scoped one — it outlives any request.
"""

from __future__ import annotations

import asyncio
import logging
from collections.abc import Callable
from contextlib import AbstractAsyncContextManager
from dataclasses import dataclass
from datetime import datetime
from typing import Protocol, runtime_checkable
from uuid import UUID

from cyberdyne_backend.application.academy.translation import TranslationStats
from cyberdyne_backend.application.academy.use_cases import TranslateCourse

logger = logging.getLogger("cyberdyne_backend.academy.jobs")

# A job that has failed this many times is left ``failed`` and not retried,
# so a permanently-broken course can't spin the worker forever.
MAX_ATTEMPTS = 5

# Cap how many failing fields are named in a job's error so a course with many
# broken lessons can't blow up the ``error`` column.
_MAX_FAILURES_IN_ERROR = 5


@dataclass(slots=True)
class TranslationJob:
    """A claimed unit of work: translate one course into one language."""

    id: UUID
    course_slug: str
    language: str
    attempts: int


@dataclass(slots=True)
class TranslationJobView:
    """Read-only view of a recorded translation job, for surfacing progress
    and per-field failures through the admin API (issue #235)."""

    language: str
    status: str  # pending | running | done | failed
    attempts: int
    error: str | None
    updated_at: datetime


def summarize_failures(stats: TranslationStats) -> str:
    """A compact, human-readable summary of the fields that failed to
    translate — recorded as the job's ``error`` so an admin can see *which*
    lesson/question broke and why without DB or log access."""
    shown = stats.failures[:_MAX_FAILURES_IN_ERROR]
    parts = [f'{f.kind} "{f.label}" ({f.ref_id}): {f.error}' for f in shown]
    extra = len(stats.failures) - len(shown)
    if extra > 0:
        parts.append(f"… and {extra} more")
    return f"{stats.failed} field(s) failed to translate: " + "; ".join(parts)


@runtime_checkable
class TranslationJobStore(Protocol):
    """Outbound port over the durable translation-job queue."""

    async def enqueue(self, course_slug: str, language: str) -> None:
        """Upsert a ``(course_slug, language)`` job to ``pending``.

        Re-enqueueing is safe: translation is idempotent (skips unchanged
        content by source hash), so re-running only fills gaps. A job that
        was ``done``/``failed`` is reset to ``pending`` with attempts
        cleared so it runs again."""
        ...

    async def claim_next(self) -> TranslationJob | None:
        """Atomically claim the oldest ``pending`` job, marking it
        ``running``. Returns ``None`` when the queue is empty."""
        ...

    async def mark_done(self, job_id: UUID) -> None:
        """Mark a claimed job ``done``."""
        ...

    async def mark_failed(self, job_id: UUID, error: str) -> None:
        """Record a failed attempt. Increments ``attempts`` and leaves the
        job ``pending`` for retry until ``MAX_ATTEMPTS``, after which it is
        marked ``failed``."""
        ...

    async def requeue_running(self) -> int:
        """Reset every ``running`` job back to ``pending`` (called on
        startup so jobs interrupted by a restart resume). Returns the
        number of jobs requeued."""
        ...

    async def list_jobs(self, course_slug: str) -> list[TranslationJobView]:
        """Every translation job recorded for a course (one per language),
        with status/attempts/error — lets the admin API surface translation
        progress and per-field failures without DB access."""
        ...


# An async context manager yielding a fresh, fully-wired TranslateCourse
# bound to its own session for one job. The context manager owns the session
# lifecycle (commit on success, rollback on error).
TranslateCourseScope = AbstractAsyncContextManager[TranslateCourse]

# A factory producing such a scope — supplied by main.py so the worker stays
# free of any adapter imports.
TranslateCourseFactory = Callable[[], TranslateCourseScope]


@dataclass(slots=True)
class TranslationWorker:
    """Drains the translation-job queue. Run as a long-lived task.

    Each iteration claims one job, runs translation against a fresh
    session/LLM, then records the outcome. With an empty queue it sleeps
    ``idle_sleep_s`` before polling again. ``run_forever`` exits cleanly on
    :class:`asyncio.CancelledError` (shutdown)."""

    store: TranslationJobStore
    translate_course_factory: TranslateCourseFactory
    idle_sleep_s: float = 2.0

    async def run_once(self) -> bool:
        """Claim and process a single job. Returns ``True`` if a job was
        processed, ``False`` if the queue was empty."""
        job = await self.store.claim_next()
        if job is None:
            return False
        try:
            async with self.translate_course_factory() as translate_course:
                stats = await translate_course.execute(job.course_slug, job.language)
        except Exception as exc:  # record any failure and move on
            logger.warning(
                "translation job failed — %s [%s] (attempt %d): %s",
                job.course_slug,
                job.language,
                job.attempts + 1,
                exc,
            )
            await self.store.mark_failed(job.id, str(exc))
            return True
        # A field-level failure (e.g. a code-heavy lesson the model keeps
        # dropping a sentinel on) leaves that field untranslated, so the
        # course never reaches 100% and the language stays unavailable.
        # Record which fields broke and retry; after MAX_ATTEMPTS the job
        # settles as ``failed`` with a diagnosable error rather than silently
        # "done" forever (issue #235).
        if stats.failed > 0:
            error = summarize_failures(stats)
            logger.warning(
                "translation job incomplete — %s [%s] (attempt %d): %s",
                job.course_slug,
                job.language,
                job.attempts + 1,
                error,
            )
            await self.store.mark_failed(job.id, error)
            return True
        await self.store.mark_done(job.id)
        logger.info(
            "translation job done — %s [%s]: +%d translated, %d skipped, %d failed",
            job.course_slug,
            job.language,
            stats.translated,
            stats.skipped,
            stats.failed,
        )
        return True

    async def run_forever(self) -> None:
        """Loop forever, sleeping when the queue is empty. Cancellation
        (shutdown) propagates out cleanly."""
        requeued = await self.store.requeue_running()
        if requeued:
            logger.info("requeued %d interrupted translation job(s) on startup", requeued)
        while True:
            try:
                processed = await self.run_once()
            except asyncio.CancelledError:
                raise
            except Exception:  # never let the loop die on a transient error
                logger.exception("translation worker iteration errored; continuing")
                processed = False
            if not processed:
                await asyncio.sleep(self.idle_sleep_s)


__all__ = [
    "MAX_ATTEMPTS",
    "TranslateCourseFactory",
    "TranslateCourseScope",
    "TranslationJob",
    "TranslationJobStore",
    "TranslationJobView",
    "TranslationWorker",
    "summarize_failures",
]
