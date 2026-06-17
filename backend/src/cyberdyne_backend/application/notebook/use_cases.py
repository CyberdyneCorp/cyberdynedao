"""Use cases for the notebook notes CRUD (issue #161, part 1)."""

from __future__ import annotations

from dataclasses import dataclass
from uuid import UUID

from cyberdyne_backend.domain.notebook import (
    Flashcard,
    FlashcardNotFoundError,
    Note,
    NotebookRepository,
    NoteFields,
    NoteNotFoundError,
    NotePage,
    NoteType,
    ReviewRating,
    apply_fields,
    new_flashcard,
    new_note,
    record_review,
)

DEFAULT_NOTE_LIMIT = 20
MAX_NOTE_LIMIT = 100


@dataclass(slots=True)
class CreateNote:
    repo: NotebookRepository

    async def execute(self, *, user_id: UUID, fields: NoteFields) -> Note:
        return await self.repo.add(new_note(user_id=user_id, fields=fields))


@dataclass(slots=True)
class GetNote:
    repo: NotebookRepository

    async def execute(self, *, user_id: UUID, note_id: UUID) -> Note:
        return await self.repo.get(user_id=user_id, note_id=note_id)


@dataclass(slots=True)
class ListNotes:
    repo: NotebookRepository

    async def execute(
        self,
        *,
        user_id: UUID,
        type: NoteType | None = None,
        query: str | None = None,
        due: bool = False,
        cursor: str | None = None,
        limit: int = DEFAULT_NOTE_LIMIT,
    ) -> NotePage:
        clamped = max(1, min(limit, MAX_NOTE_LIMIT))
        return await self.repo.list_for_user(
            user_id=user_id,
            type=type,
            query=query,
            due=due,
            cursor=cursor,
            limit=clamped,
        )


@dataclass(slots=True)
class UpdateNote:
    repo: NotebookRepository

    async def execute(self, *, user_id: UUID, note_id: UUID, fields: NoteFields) -> Note:
        existing = await self.repo.get(user_id=user_id, note_id=note_id)
        return await self.repo.update(apply_fields(existing, fields))


@dataclass(slots=True)
class DeleteNote:
    repo: NotebookRepository

    async def execute(self, *, user_id: UUID, note_id: UUID) -> None:
        removed = await self.repo.delete(user_id=user_id, note_id=note_id)
        if not removed:
            raise NoteNotFoundError(f"note {note_id} not found")


# ── Flashcards (issue #161, part 2) ───────────────────────────────────
#
# Every flashcard operation first loads the note scoped to the user, so a
# learner can only touch flashcards on notes they own (raises
# NoteNotFoundError otherwise).


@dataclass(slots=True)
class AddFlashcard:
    repo: NotebookRepository

    async def execute(
        self, *, user_id: UUID, note_id: UUID, question: str, answer: str
    ) -> Flashcard:
        await self.repo.get(user_id=user_id, note_id=note_id)
        card = new_flashcard(note_id=note_id, question=question, answer=answer)
        return await self.repo.add_flashcard(card)


@dataclass(slots=True)
class ListFlashcards:
    repo: NotebookRepository

    async def execute(self, *, user_id: UUID, note_id: UUID) -> list[Flashcard]:
        await self.repo.get(user_id=user_id, note_id=note_id)
        return await self.repo.list_flashcards(note_id)


@dataclass(slots=True)
class DeleteFlashcard:
    repo: NotebookRepository

    async def execute(self, *, user_id: UUID, note_id: UUID, flashcard_id: UUID) -> None:
        await self.repo.get(user_id=user_id, note_id=note_id)
        removed = await self.repo.delete_flashcard(note_id=note_id, flashcard_id=flashcard_id)
        if not removed:
            raise FlashcardNotFoundError(f"flashcard {flashcard_id} not found")


@dataclass(slots=True)
class ReviewNote:
    """Record a spaced-review of a note: advance the interval and reschedule
    the next review. The note is loaded scoped to the user."""

    repo: NotebookRepository

    async def execute(self, *, user_id: UUID, note_id: UUID, rating: ReviewRating) -> Note:
        note = await self.repo.get(user_id=user_id, note_id=note_id)
        record_review(note, rating)
        return await self.repo.update(note)
