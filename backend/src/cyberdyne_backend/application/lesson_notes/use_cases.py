"""Use cases for per-user lesson notes (issue #188)."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, datetime
from uuid import UUID

from cyberdyne_backend.domain.lesson_notes import (
    LessonNote,
    LessonNoteNotFoundError,
    LessonNotePage,
    LessonNoteRepository,
    new_lesson_note,
)

DEFAULT_NOTES_LIMIT = 50
MAX_NOTES_LIMIT = 200


@dataclass(slots=True)
class SyncResult:
    """A note plus whether this call created it (vs. updated an existing
    client-supplied id) — lets the router return 201 vs 200."""

    note: LessonNote
    created: bool


@dataclass(slots=True)
class SyncLessonNote:
    """Idempotent create: a client-supplied ``note_id`` that already exists
    for the user updates it in place rather than duplicating."""

    repo: LessonNoteRepository

    async def execute(
        self,
        *,
        user_id: UUID,
        lesson_id: str,
        course_slug: str,
        body: str,
        quote: str | None = None,
        note_id: UUID | None = None,
    ) -> SyncResult:
        note = new_lesson_note(
            user_id=user_id,
            course_slug=course_slug,
            lesson_id=lesson_id,
            body=body,
            quote=quote,
            note_id=note_id,
        )
        created = await self.repo.upsert(note)
        return SyncResult(note=note, created=created)


@dataclass(slots=True)
class ListLessonNotes:
    repo: LessonNoteRepository

    async def execute(self, *, user_id: UUID, lesson_id: str) -> list[LessonNote]:
        return await self.repo.list_for_lesson(user_id=user_id, lesson_id=lesson_id)


@dataclass(slots=True)
class ListUserNotes:
    repo: LessonNoteRepository

    async def execute(
        self,
        *,
        user_id: UUID,
        course_slug: str | None = None,
        cursor: str | None = None,
        limit: int = DEFAULT_NOTES_LIMIT,
    ) -> LessonNotePage:
        clamped = max(1, min(limit, MAX_NOTES_LIMIT))
        return await self.repo.list_for_user(
            user_id=user_id, course_slug=course_slug, cursor=cursor, limit=clamped
        )


@dataclass(slots=True)
class UpdateLessonNote:
    repo: LessonNoteRepository

    async def execute(
        self,
        *,
        user_id: UUID,
        note_id: UUID,
        body: str | None = None,
        quote: str | None = None,
        quote_set: bool = False,
    ) -> LessonNote:
        existing = await self.repo.get(user_id=user_id, note_id=note_id)
        if body is not None:
            existing.body = body.strip()
        # ``quote_set`` distinguishes "clear the quote" (null) from "leave
        # it untouched" (field absent from the PATCH payload).
        if quote_set:
            existing.quote = quote.strip() if quote else None
        existing.updated_at = datetime.now(tz=UTC)
        existing.validate()
        return await self.repo.update(existing)


@dataclass(slots=True)
class DeleteLessonNote:
    repo: LessonNoteRepository

    async def execute(self, *, user_id: UUID, note_id: UUID) -> None:
        removed = await self.repo.delete(user_id=user_id, note_id=note_id)
        if not removed:
            raise LessonNoteNotFoundError(f"note {note_id} not found")
