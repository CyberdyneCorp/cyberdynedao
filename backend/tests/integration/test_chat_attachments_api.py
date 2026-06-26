"""Chat message with attachments grounds the turn + echoes metadata (#220).

Drives POST /api/v1/chat/sessions/{id}/messages with an ``attachments``
upload-UUID, using a real RunChatTurn over the real chat repo plus a fake
LLM and a fake ingestor, then asserts GET history returns the attachment
metadata for rendering.
"""

from __future__ import annotations

import uuid
from collections.abc import AsyncIterator, Iterator

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from cyberdyne_backend.adapters.inbound.api.ai_chat import router as chat_router
from cyberdyne_backend.adapters.inbound.api.ai_chat.router import (
    get_history_uc,
    get_run_turn_uc,
)
from cyberdyne_backend.adapters.inbound.api.rate_limit import SlidingWindowRateLimiter
from cyberdyne_backend.adapters.outbound.persistence.ai_chat.repository import (
    SqlAlchemyChatRepository,
)
from cyberdyne_backend.application.ai_chat import GetChatHistory, RunChatTurn
from cyberdyne_backend.domain.ai_chat import (
    AttachmentRef,
    IngestedAttachment,
    LLMResponse,
    new_session,
)
from cyberdyne_backend.infrastructure.database.engine import get_session_factory

pytestmark = pytest.mark.integration


class _FakeLLM:
    async def complete(self, *, messages, tools, system_prompt) -> LLMResponse:
        self.last_system_prompt = system_prompt
        return LLMResponse(content="grounded answer", model="fake")

    async def stream(self, **_kwargs):  # pragma: no cover - not used here
        yield None


class _FakeIngestor:
    def __init__(self, ref: AttachmentRef) -> None:
        self._ref = ref

    async def ingest(self, upload_ids: tuple[uuid.UUID, ...]) -> tuple[IngestedAttachment, ...]:
        return (IngestedAttachment(ref=self._ref, text="the file contents"),)


class _NoopDispatcher:
    # The fake LLM returns a final answer with no tool calls, so dispatch is
    # never reached; this stands in for ToolDispatcher (duck-typed).
    def use_python_session(self, session_id: str) -> None:  # pragma: no cover
        return None

    async def dispatch(self, call, *, chat_session_id: str) -> str:  # pragma: no cover
        return ""


@pytest.fixture
def chat_client(app: FastAPI, monkeypatch) -> Iterator[tuple[TestClient, uuid.UUID, AttachmentRef]]:
    # The per-IP chat limiter is a module global; lift it so repeated POSTs
    # in one test don't trip it (mirrors test_chat_rate_limit.py).
    monkeypatch.setattr(
        chat_router,
        "_chat_rate_limiter",
        SlidingWindowRateLimiter(limit=1000, window_s=60.0, detail="x"),
    )
    session = new_session()
    ref = AttachmentRef(id=uuid.uuid4(), filename="lecture.pdf", content_type="application/pdf")

    async def _run_turn() -> AsyncIterator[RunChatTurn]:
        async with get_session_factory()() as db:
            repo = SqlAlchemyChatRepository(db)
            await repo.save_session(session)
            yield RunChatTurn(
                repo=repo,
                llm=_FakeLLM(),
                dispatcher=_NoopDispatcher(),  # type: ignore[arg-type]
                ingestor=_FakeIngestor(ref),
            )
            await db.commit()

    async def _history() -> AsyncIterator[GetChatHistory]:
        async with get_session_factory()() as db:
            yield GetChatHistory(repo=SqlAlchemyChatRepository(db))

    app.dependency_overrides[get_run_turn_uc] = _run_turn
    app.dependency_overrides[get_history_uc] = _history
    yield TestClient(app), session.id, ref


@pytest.mark.usefixtures("_prepared_schema")
def test_attachment_message_grounds_and_history_echoes(
    chat_client: tuple[TestClient, uuid.UUID, AttachmentRef],
) -> None:
    client, session_id, ref = chat_client

    sent = client.post(
        f"/api/v1/chat/sessions/{session_id}/messages",
        json={"content": "summarize the lecture", "attachments": [str(ref.id)]},
    )
    assert sent.status_code == 200, sent.text
    assert sent.json()["content"] == "grounded answer"

    history = client.get(f"/api/v1/chat/sessions/{session_id}")
    assert history.status_code == 200, history.text
    messages = history.json()["messages"]
    user_msg = next(m for m in messages if m["role"] == "user")
    assert user_msg["attachments"] == [
        {
            "id": str(ref.id),
            "filename": "lecture.pdf",
            "contentType": "application/pdf",
        }
    ]
