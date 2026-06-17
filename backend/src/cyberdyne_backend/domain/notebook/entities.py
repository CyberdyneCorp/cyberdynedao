"""Entities for the notebook context — the learner's "living memory" (#161).

A *note* is a per-user saved fragment of learning: a concept, an executed
code snippet + its run result/plots, an AI summary, a theory write-up, a
worked problem. This module covers the core note model + CRUD invariants;
flashcards and spaced-review scheduling are layered on in follow-ups.
"""

from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from datetime import UTC, datetime, timedelta
from enum import StrEnum
from uuid import UUID

from cyberdyne_backend.domain.notebook.errors import (
    InvalidFlashcardError,
    InvalidNoteError,
    InvalidReviewError,
)

_MAX_TITLE = 200
_MAX_FLASHCARD = 2000


class NoteType(StrEnum):
    LESSON = "lesson"
    LAB = "lab"
    CODE = "code"
    SIMULATION = "simulation"
    THEORY = "theory"
    PROBLEM = "problem"


def parse_note_type(raw: str) -> NoteType:
    try:
        return NoteType(raw)
    except ValueError as exc:
        allowed = ", ".join(t.value for t in NoteType)
        raise InvalidNoteError(f"unknown note type {raw!r}; expected one of: {allowed}") from exc


@dataclass(slots=True)
class Note:
    id: UUID
    user_id: UUID
    title: str
    type: NoteType
    body: str  # markdown
    course_slug: str | None = None
    lesson_id: UUID | None = None
    # Saved-from-the-Lab payload: a code snippet, its language, the run
    # result (arbitrary JSON), and references to generated plot artifacts.
    code: str | None = None
    language: str | None = None
    run_result: dict[str, object] | None = None
    plot_refs: tuple[str, ...] = ()
    tags: tuple[str, ...] = ()
    # Spaced-review schedule (issue #161, part 3). `review_interval_days` is
    # the current spacing in days (0 = never reviewed); the timestamps are
    # the last review and when the note is next due.
    reviewed_at: datetime | None = None
    next_review_at: datetime | None = None
    review_interval_days: int = 0
    # LLM-generated condensed summary, populated on demand (issue #187).
    ai_summary: str | None = None
    created_at: datetime = field(default_factory=lambda: datetime.now(tz=UTC))
    updated_at: datetime | None = None

    def validate(self) -> None:
        if not self.title.strip() or len(self.title) > _MAX_TITLE:
            raise InvalidNoteError(f"title must be 1..{_MAX_TITLE} chars")


@dataclass(slots=True)
class NoteFields:
    """Mutable fields of a note — the create/update payload."""

    title: str
    type: NoteType
    body: str
    course_slug: str | None = None
    lesson_id: UUID | None = None
    code: str | None = None
    language: str | None = None
    run_result: dict[str, object] | None = None
    plot_refs: tuple[str, ...] = ()
    tags: tuple[str, ...] = ()


def new_note(*, user_id: UUID, fields: NoteFields, now: datetime | None = None) -> Note:
    moment = now or datetime.now(tz=UTC)
    note = Note(
        id=uuid.uuid4(),
        user_id=user_id,
        title=fields.title.strip(),
        type=fields.type,
        body=fields.body,
        course_slug=fields.course_slug,
        lesson_id=fields.lesson_id,
        code=fields.code,
        language=fields.language,
        run_result=fields.run_result,
        plot_refs=fields.plot_refs,
        tags=fields.tags,
        created_at=moment,
        updated_at=moment,
    )
    note.validate()
    return note


def apply_fields(note: Note, fields: NoteFields, *, now: datetime | None = None) -> Note:
    """Return ``note`` mutated to ``fields`` (identity + created_at kept)."""
    note.title = fields.title.strip()
    note.type = fields.type
    note.body = fields.body
    note.course_slug = fields.course_slug
    note.lesson_id = fields.lesson_id
    note.code = fields.code
    note.language = fields.language
    note.run_result = fields.run_result
    note.plot_refs = fields.plot_refs
    note.tags = fields.tags
    note.updated_at = now or datetime.now(tz=UTC)
    note.validate()
    return note


@dataclass(slots=True)
class NotePage:
    items: list[Note] = field(default_factory=list)
    next_cursor: str | None = None


@dataclass(slots=True)
class Flashcard:
    """A question/answer card generated from (or attached to) a note, for
    self-testing + spaced review."""

    id: UUID
    note_id: UUID
    question: str
    answer: str
    created_at: datetime = field(default_factory=lambda: datetime.now(tz=UTC))


def new_flashcard(
    *,
    note_id: UUID,
    question: str,
    answer: str,
    now: datetime | None = None,
) -> Flashcard:
    q, a = question.strip(), answer.strip()
    if not q or len(q) > _MAX_FLASHCARD:
        raise InvalidFlashcardError(f"question must be 1..{_MAX_FLASHCARD} chars")
    if not a or len(a) > _MAX_FLASHCARD:
        raise InvalidFlashcardError(f"answer must be 1..{_MAX_FLASHCARD} chars")
    return Flashcard(
        id=uuid.uuid4(),
        note_id=note_id,
        question=q,
        answer=a,
        created_at=now or datetime.now(tz=UTC),
    )


# ── Spaced review (issue #161, part 3) ────────────────────────────────


class ReviewRating(StrEnum):
    """How well the learner recalled the note at review time."""

    AGAIN = "again"  # forgot — reset spacing
    HARD = "hard"
    GOOD = "good"
    EASY = "easy"


# Cap the spacing so an interval can't run away.
_MAX_INTERVAL_DAYS = 365


def parse_review_rating(raw: str) -> ReviewRating:
    try:
        return ReviewRating(raw)
    except ValueError as exc:
        allowed = ", ".join(r.value for r in ReviewRating)
        raise InvalidReviewError(
            f"unknown review rating {raw!r}; expected one of: {allowed}"
        ) from exc


def next_interval_days(previous: int, rating: ReviewRating) -> int:
    """Deterministic spaced-repetition schedule (Leitner/SM-2-lite).

    A forgotten note resets to 1 day; otherwise the interval grows by a
    rating-dependent factor. ``previous`` is the current interval in days
    (0 = never reviewed). Result is clamped to 1..365.
    """
    if rating is ReviewRating.AGAIN:
        return 1
    if previous <= 0:
        first = {ReviewRating.HARD: 1, ReviewRating.GOOD: 2, ReviewRating.EASY: 4}
        return first[rating]
    factor = {ReviewRating.HARD: 1.2, ReviewRating.GOOD: 2.0, ReviewRating.EASY: 2.5}
    grown = max(previous + 1, round(previous * factor[rating]))
    return min(grown, _MAX_INTERVAL_DAYS)


def record_review(note: Note, rating: ReviewRating, *, now: datetime | None = None) -> Note:
    """Apply a review to ``note`` in place: advance the interval, stamp
    ``reviewed_at`` and the next due time."""
    moment = now or datetime.now(tz=UTC)
    interval = next_interval_days(note.review_interval_days, rating)
    note.review_interval_days = interval
    note.reviewed_at = moment
    note.next_review_at = moment + timedelta(days=interval)
    note.updated_at = moment
    return note
