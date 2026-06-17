"""Unit tests for notebook LLM generation (issue #187)."""

from __future__ import annotations

import asyncio
import uuid

from cyberdyne_backend.application.notebook import (
    GenerateFlashcards,
    SummarizeNote,
)
from cyberdyne_backend.application.notebook.ai_use_cases import parse_flashcards
from cyberdyne_backend.domain.ai_chat import LLMResponse
from cyberdyne_backend.domain.notebook import Flashcard, Note, NoteType


class _FakeLLM:
    def __init__(self, reply: str) -> None:
        self.reply = reply
        self.calls = 0

    async def complete(self, *, messages, tools, system_prompt) -> LLMResponse:
        self.calls += 1
        self.last_system = system_prompt
        self.last_content = messages[0].content
        return LLMResponse(content=self.reply, model="fake")


class _FakeRepo:
    def __init__(self, note: Note) -> None:
        self._note = note
        self.flashcards: list[Flashcard] = []
        self.updated: Note | None = None

    async def get(self, *, user_id, note_id) -> Note:
        from cyberdyne_backend.domain.notebook import NoteNotFoundError

        if note_id != self._note.id or user_id != self._note.user_id:
            raise NoteNotFoundError(str(note_id))
        return self._note

    async def add_flashcard(self, flashcard: Flashcard) -> Flashcard:
        self.flashcards.append(flashcard)
        return flashcard

    async def update(self, note: Note) -> Note:
        self.updated = note
        return note


def _note() -> Note:
    return Note(
        id=uuid.uuid4(),
        user_id=uuid.uuid4(),
        title="Ohm's Law",
        type=NoteType.THEORY,
        body="V = I * R relates voltage, current, resistance.",
    )


# ── parse_flashcards ──────────────────────────────────────────────────


def test_parse_plain_json_array() -> None:
    out = parse_flashcards(
        '[{"question": "Q1?", "answer": "A1"}, {"question": "Q2?", "answer": "A2"}]'
    )
    assert out == [("Q1?", "A1"), ("Q2?", "A2")]


def test_parse_strips_code_fence() -> None:
    out = parse_flashcards('```json\n[{"question": "Q", "answer": "A"}]\n```')
    assert out == [("Q", "A")]


def test_parse_offline_plaintext_returns_empty() -> None:
    # The StaticChatClient's canned reply is not JSON → no cards.
    assert parse_flashcards("I'm running in offline mode — set OPENAI_API_KEY.") == []


def test_parse_drops_malformed_items() -> None:
    out = parse_flashcards('[{"question": "Q", "answer": "A"}, {"question": ""}, "x", 5]')
    assert out == [("Q", "A")]


# ── use cases ─────────────────────────────────────────────────────────


def test_generate_persists_parsed_cards() -> None:
    note = _note()
    repo = _FakeRepo(note)
    llm = _FakeLLM('[{"question": "What is V=IR?", "answer": "Ohm\'s law"}]')
    cards = asyncio.run(
        GenerateFlashcards(repo=repo, llm=llm).execute(user_id=note.user_id, note_id=note.id)
    )
    assert [c.question for c in cards] == ["What is V=IR?"]
    assert len(repo.flashcards) == 1
    assert llm.calls == 1


def test_generate_offline_yields_no_cards() -> None:
    note = _note()
    repo = _FakeRepo(note)
    llm = _FakeLLM("offline mode, no JSON here")
    cards = asyncio.run(
        GenerateFlashcards(repo=repo, llm=llm).execute(user_id=note.user_id, note_id=note.id)
    )
    assert cards == []
    assert repo.flashcards == []


def test_generate_caps_at_max() -> None:
    from cyberdyne_backend.application.notebook import MAX_GENERATED_FLASHCARDS

    note = _note()
    repo = _FakeRepo(note)
    many = [{"question": f"Q{i}", "answer": f"A{i}"} for i in range(MAX_GENERATED_FLASHCARDS + 5)]
    import json

    llm = _FakeLLM(json.dumps(many))
    cards = asyncio.run(
        GenerateFlashcards(repo=repo, llm=llm).execute(user_id=note.user_id, note_id=note.id)
    )
    assert len(cards) == MAX_GENERATED_FLASHCARDS


def test_summarize_persists_summary() -> None:
    note = _note()
    repo = _FakeRepo(note)
    llm = _FakeLLM("  Ohm's law links V, I and R.  ")
    updated = asyncio.run(
        SummarizeNote(repo=repo, llm=llm).execute(user_id=note.user_id, note_id=note.id)
    )
    assert updated.ai_summary == "Ohm's law links V, I and R."
    assert repo.updated is not None


def test_summary_prompt_includes_code_when_present() -> None:
    note = _note()
    note.code = "print(2+2)"
    note.language = "python"
    repo = _FakeRepo(note)
    llm = _FakeLLM("summary")
    asyncio.run(SummarizeNote(repo=repo, llm=llm).execute(user_id=note.user_id, note_id=note.id))
    assert "print(2+2)" in llm.last_content
