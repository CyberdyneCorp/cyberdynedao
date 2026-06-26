"""Unit tests for the durable translation worker (jobs + worker loop).

Uses an in-memory fake job store that mimics the SQLAlchemy adapter's
semantics (oldest-pending claim, running transition, attempt/retry cap,
requeue-on-startup) and a fake TranslateCourse scope, so these exercise the
application logic without a database.
"""

from __future__ import annotations

import asyncio
from contextlib import asynccontextmanager
from dataclasses import dataclass, field
from uuid import UUID, uuid4

import pytest

from cyberdyne_backend.application.academy import (
    MAX_ATTEMPTS,
    TranslationFailure,
    TranslationJob,
    TranslationStats,
    TranslationWorker,
    summarize_failures,
)

pytestmark = pytest.mark.unit


@dataclass
class _Row:
    id: UUID
    course_slug: str
    language: str
    status: str = "pending"
    attempts: int = 0
    error: str | None = None
    seq: int = 0  # insertion order — stands in for created_at


class FakeJobStore:
    """In-memory ``TranslationJobStore`` mirroring the adapter's semantics."""

    def __init__(self) -> None:
        self.rows: list[_Row] = []
        self._seq = 0

    async def enqueue(self, course_slug: str, language: str) -> None:
        for row in self.rows:
            if row.course_slug == course_slug and row.language == language:
                row.status = "pending"
                row.attempts = 0
                row.error = None
                return
        self._seq += 1
        self.rows.append(
            _Row(id=uuid4(), course_slug=course_slug, language=language, seq=self._seq)
        )

    async def claim_next(self) -> TranslationJob | None:
        pending = sorted((r for r in self.rows if r.status == "pending"), key=lambda r: r.seq)
        if not pending:
            return None
        row = pending[0]
        row.status = "running"
        return TranslationJob(
            id=row.id, course_slug=row.course_slug, language=row.language, attempts=row.attempts
        )

    async def mark_done(self, job_id: UUID) -> None:
        self._get(job_id).status = "done"

    async def mark_failed(self, job_id: UUID, error: str) -> None:
        row = self._get(job_id)
        row.attempts += 1
        row.error = error
        row.status = "failed" if row.attempts >= MAX_ATTEMPTS else "pending"

    async def requeue_running(self) -> int:
        count = 0
        for row in self.rows:
            if row.status == "running":
                row.status = "pending"
                count += 1
        return count

    def _get(self, job_id: UUID) -> _Row:
        return next(r for r in self.rows if r.id == job_id)


@dataclass
class FakeTranslateCourse:
    calls: list[tuple[str, str]] = field(default_factory=list)
    raise_on: tuple[str, str] | None = None
    stats: TranslationStats | None = None

    async def execute(self, slug: str, language: str) -> TranslationStats:
        self.calls.append((slug, language))
        if self.raise_on == (slug, language):
            raise RuntimeError("boom")
        if self.stats is not None:
            return self.stats
        return TranslationStats(translated=3, skipped=1, failed=0)


def _factory(translate: FakeTranslateCourse):
    @asynccontextmanager
    async def scope():
        yield translate

    return scope


# ── store semantics ────────────────────────────────────────────────────


async def test_enqueue_adds_pending_job() -> None:
    store = FakeJobStore()
    await store.enqueue("alg", "pt-BR")
    assert len(store.rows) == 1
    assert store.rows[0].status == "pending"


async def test_enqueue_is_idempotent_per_slug_language() -> None:
    store = FakeJobStore()
    await store.enqueue("alg", "pt-BR")
    await store.enqueue("alg", "pt-BR")
    assert len(store.rows) == 1


async def test_enqueue_resets_failed_job_to_pending() -> None:
    store = FakeJobStore()
    await store.enqueue("alg", "pt-BR")
    store.rows[0].status = "failed"
    store.rows[0].attempts = 9
    await store.enqueue("alg", "pt-BR")
    assert store.rows[0].status == "pending"
    assert store.rows[0].attempts == 0


async def test_claim_next_picks_oldest_and_marks_running() -> None:
    store = FakeJobStore()
    await store.enqueue("first", "es")
    await store.enqueue("second", "es")
    job = await store.claim_next()
    assert job is not None
    assert job.course_slug == "first"
    assert store.rows[0].status == "running"
    # Second claim skips the now-running first and takes the next pending.
    job2 = await store.claim_next()
    assert job2 is not None
    assert job2.course_slug == "second"


async def test_claim_next_returns_none_when_empty() -> None:
    assert await FakeJobStore().claim_next() is None


async def test_requeue_running_resets_running_to_pending() -> None:
    store = FakeJobStore()
    await store.enqueue("alg", "pt-BR")
    await store.claim_next()  # -> running
    assert store.rows[0].status == "running"
    requeued = await store.requeue_running()
    assert requeued == 1
    assert store.rows[0].status == "pending"


# ── worker ─────────────────────────────────────────────────────────────


async def test_worker_processes_one_job_success() -> None:
    store = FakeJobStore()
    await store.enqueue("alg", "pt-BR")
    translate = FakeTranslateCourse()
    worker = TranslationWorker(store=store, translate_course_factory=_factory(translate))

    processed = await worker.run_once()

    assert processed is True
    assert translate.calls == [("alg", "pt-BR")]
    assert store.rows[0].status == "done"


async def test_worker_returns_false_on_empty_queue() -> None:
    worker = TranslationWorker(
        store=FakeJobStore(), translate_course_factory=_factory(FakeTranslateCourse())
    )
    assert await worker.run_once() is False


async def test_worker_marks_failed_and_retries_on_exception() -> None:
    store = FakeJobStore()
    await store.enqueue("alg", "pt-BR")
    translate = FakeTranslateCourse(raise_on=("alg", "pt-BR"))
    worker = TranslationWorker(store=store, translate_course_factory=_factory(translate))

    processed = await worker.run_once()

    assert processed is True
    # First failure: one attempt recorded, requeued for retry (under the cap).
    assert store.rows[0].attempts == 1
    assert store.rows[0].status == "pending"
    assert store.rows[0].error == "boom"


async def test_worker_run_forever_requeues_drains_then_cancels() -> None:
    store = FakeJobStore()
    await store.enqueue("alg", "pt-BR")
    # A job stranded 'running' by a prior restart must be requeued on startup.
    store.rows[0].status = "running"
    translate = FakeTranslateCourse()
    worker = TranslationWorker(
        store=store,
        translate_course_factory=_factory(translate),
        idle_sleep_s=0.01,
    )

    task = asyncio.create_task(worker.run_forever())
    # Let the loop requeue + drain the job, then cancel cleanly on shutdown.
    for _ in range(100):
        await asyncio.sleep(0.01)
        if store.rows[0].status == "done":
            break
    task.cancel()
    with pytest.raises(asyncio.CancelledError):
        await task

    assert translate.calls == [("alg", "pt-BR")]
    assert store.rows[0].status == "done"


async def test_worker_gives_up_after_max_attempts() -> None:
    store = FakeJobStore()
    await store.enqueue("alg", "pt-BR")
    translate = FakeTranslateCourse(raise_on=("alg", "pt-BR"))
    worker = TranslationWorker(store=store, translate_course_factory=_factory(translate))

    for _ in range(MAX_ATTEMPTS):
        await worker.run_once()

    assert store.rows[0].attempts == MAX_ATTEMPTS
    assert store.rows[0].status == "failed"


# ── Field-level failure recording (issue #235) ──────────────────────────


def _lesson_failure() -> TranslationFailure:
    return TranslationFailure(
        kind="lesson",
        ref_id=uuid4(),
        language="pt-BR",
        label="Machine learning on omics with tidymodels",
        error="translation dropped 1 protected span(s) for pt-BR",
    )


async def test_worker_records_field_failures_and_retries() -> None:
    # A job that completes but leaves a field untranslated must NOT be marked
    # done (the language would never reach 'available'); it retries with a
    # diagnosable error naming the broken field.
    store = FakeJobStore()
    await store.enqueue("r-data-analysis-advanced", "pt-BR")
    failure = _lesson_failure()
    translate = FakeTranslateCourse(
        stats=TranslationStats(translated=10, skipped=0, failed=1, failures=[failure])
    )
    worker = TranslationWorker(store=store, translate_course_factory=_factory(translate))

    processed = await worker.run_once()

    assert processed is True
    assert store.rows[0].status == "pending"  # under the cap → retry
    assert store.rows[0].attempts == 1
    assert store.rows[0].error is not None
    assert failure.label in store.rows[0].error
    assert str(failure.ref_id) in store.rows[0].error


def test_summarize_failures_caps_and_counts() -> None:
    failures = [_lesson_failure() for _ in range(8)]
    stats = TranslationStats(translated=0, failed=8, failures=failures)
    summary = summarize_failures(stats)
    assert summary.startswith("8 field(s) failed to translate:")
    # Only the first few are named; the rest are summarized as a count.
    assert "… and 3 more" in summary
