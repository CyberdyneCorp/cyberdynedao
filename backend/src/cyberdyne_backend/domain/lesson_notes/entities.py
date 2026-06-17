"""Entities for the lesson-notes context (issue #188).

A *lesson note* is a per-user annotation on a lesson: an optional
highlighted ``quote`` from the lesson plus the learner's ``body``. The
client (Cyberdyne Learn) keeps these on-device and syncs them here; it
supplies the ``id`` so re-syncing is idempotent (no duplicates).
"""

from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from datetime import UTC, datetime
from uuid import UUID

from cyberdyne_backend.domain.lesson_notes.errors import InvalidLessonNoteError

_MAX_COURSE_SLUG = 128
_MAX_LESSON_ID = 128
_MAX_QUOTE = 4000
_MAX_BODY = 10000


@dataclass(slots=True)
class LessonNote:
    id: UUID
    user_id: UUID
    course_slug: str
    lesson_id: str
    body: str
    quote: str | None = None
    created_at: datetime = field(default_factory=lambda: datetime.now(tz=UTC))
    updated_at: datetime | None = None

    def validate(self) -> None:
        if not self.course_slug or len(self.course_slug) > _MAX_COURSE_SLUG:
            raise InvalidLessonNoteError(f"courseSlug must be 1..{_MAX_COURSE_SLUG} chars")
        if not self.lesson_id or len(self.lesson_id) > _MAX_LESSON_ID:
            raise InvalidLessonNoteError(f"lessonId must be 1..{_MAX_LESSON_ID} chars")
        if not self.body.strip() or len(self.body) > _MAX_BODY:
            raise InvalidLessonNoteError(f"body must be 1..{_MAX_BODY} chars")
        if self.quote is not None and len(self.quote) > _MAX_QUOTE:
            raise InvalidLessonNoteError(f"quote must be at most {_MAX_QUOTE} chars")


def new_lesson_note(
    *,
    user_id: UUID,
    course_slug: str,
    lesson_id: str,
    body: str,
    quote: str | None = None,
    note_id: UUID | None = None,
    now: datetime | None = None,
) -> LessonNote:
    """Build a note. ``note_id`` is the client-supplied id when syncing; a
    fresh one is minted when absent."""
    moment = now or datetime.now(tz=UTC)
    note = LessonNote(
        id=note_id or uuid.uuid4(),
        user_id=user_id,
        course_slug=course_slug.strip(),
        lesson_id=lesson_id.strip(),
        body=body.strip(),
        quote=quote.strip() if quote else None,
        created_at=moment,
        updated_at=moment,
    )
    note.validate()
    return note


@dataclass(slots=True)
class LessonNotePage:
    items: list[LessonNote] = field(default_factory=list)
    next_cursor: str | None = None
