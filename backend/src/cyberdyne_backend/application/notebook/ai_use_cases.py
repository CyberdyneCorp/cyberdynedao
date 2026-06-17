"""LLM-backed notebook use cases (issue #187).

Auto-generate flashcards from a note and condense a note into an AI
summary. Both reuse the chat ``ChatLLMPort`` (so they run on the same
OpenAI client, or the offline ``StaticChatClient`` when no key is set —
in which case flashcard generation simply yields no cards rather than
failing). Each use case loads the note scoped to the user first.
"""

from __future__ import annotations

import json
import uuid
from dataclasses import dataclass
from uuid import UUID

from cyberdyne_backend.domain.ai_chat import ChatLLMPort, ChatMessage, ChatRole
from cyberdyne_backend.domain.notebook import (
    Flashcard,
    InvalidFlashcardError,
    Note,
    NotebookRepository,
    new_flashcard,
)

# Cap how many cards one generate call persists, and how much note context
# is sent to the model (keeps prompts bounded + costs predictable).
MAX_GENERATED_FLASHCARDS = 10
_MAX_CONTEXT_CHARS = 6000

_FLASHCARD_SYSTEM_PROMPT = (
    "You are a study-aid generator for Cyberdyne Academy. From the learner's "
    "note, write concise self-test flashcards. Respond with ONLY a JSON array "
    'of objects, each {"question": "...", "answer": "..."} — no prose, no code '
    "fences. Keep each question and answer to one or two sentences."
)

_SUMMARY_SYSTEM_PROMPT = (
    "You are a study assistant for Cyberdyne Academy. Summarize the learner's "
    "note in 2-3 plain sentences capturing the key idea. Output only the "
    "summary text."
)


def _note_context(note: Note) -> str:
    """Compact textual context for the model — title + body, plus the code
    and a short run-result repr when the note saved a Lab run."""
    parts = [f"Title: {note.title}", f"Type: {note.type.value}", "", note.body]
    if note.code:
        lang = note.language or ""
        parts += ["", f"Code ({lang}):", note.code]
    if note.run_result:
        parts += ["", f"Run result: {json.dumps(note.run_result)[:500]}"]
    return "\n".join(parts)[:_MAX_CONTEXT_CHARS]


def _strip_fence(text: str) -> str:
    """Drop a leading/trailing ```json … ``` fence if the model added one."""
    t = text.strip()
    if t.startswith("```"):
        t = t.split("\n", 1)[-1] if "\n" in t else t[3:]
        if t.rstrip().endswith("```"):
            t = t.rstrip()[:-3]
    return t.strip()


def parse_flashcards(content: str) -> list[tuple[str, str]]:
    """Best-effort parse of the model's reply into (question, answer) pairs.
    Returns an empty list for anything that isn't a JSON array of cards
    (e.g. the offline StaticChatClient's plain-text reply)."""
    try:
        data = json.loads(_strip_fence(content))
    except (ValueError, TypeError):
        return []
    if not isinstance(data, list):
        return []
    pairs: list[tuple[str, str]] = []
    for item in data:
        if not isinstance(item, dict):
            continue
        q, a = item.get("question"), item.get("answer")
        if isinstance(q, str) and isinstance(a, str) and q.strip() and a.strip():
            pairs.append((q, a))
    return pairs


def _user_message(content: str) -> ChatMessage:
    return ChatMessage(
        id=uuid.uuid4(),
        session_id=uuid.uuid4(),
        role=ChatRole.USER,
        content=content,
    )


@dataclass(slots=True)
class GenerateFlashcards:
    repo: NotebookRepository
    llm: ChatLLMPort

    async def execute(self, *, user_id: UUID, note_id: UUID) -> list[Flashcard]:
        note = await self.repo.get(user_id=user_id, note_id=note_id)
        response = await self.llm.complete(
            messages=[_user_message(_note_context(note))],
            tools=[],
            system_prompt=_FLASHCARD_SYSTEM_PROMPT,
        )
        created: list[Flashcard] = []
        for question, answer in parse_flashcards(response.content)[:MAX_GENERATED_FLASHCARDS]:
            try:
                card = new_flashcard(note_id=note_id, question=question, answer=answer)
            except InvalidFlashcardError:
                continue  # skip a malformed card rather than failing the batch
            created.append(await self.repo.add_flashcard(card))
        return created


@dataclass(slots=True)
class SummarizeNote:
    repo: NotebookRepository
    llm: ChatLLMPort

    async def execute(self, *, user_id: UUID, note_id: UUID) -> Note:
        note = await self.repo.get(user_id=user_id, note_id=note_id)
        response = await self.llm.complete(
            messages=[_user_message(_note_context(note))],
            tools=[],
            system_prompt=_SUMMARY_SYSTEM_PROMPT,
        )
        note.ai_summary = response.content.strip()
        return await self.repo.update(note)
