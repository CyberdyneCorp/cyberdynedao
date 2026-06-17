"""Locks the documented SSE framing of the chat stream endpoint (#167).

Drives POST /api/v1/chat/sessions/{id}/messages/stream with a stubbed
StreamChatTurn that yields a scripted status -> delta -> done sequence,
then asserts the on-the-wire `text/event-stream` framing matches
docs/chat-streaming.md.
"""

from __future__ import annotations

import json
import uuid
from collections.abc import AsyncIterator
from datetime import UTC, datetime

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from cyberdyne_backend.adapters.inbound.api.ai_chat.router import get_stream_turn_uc
from cyberdyne_backend.application.ai_chat.use_cases import StreamEvent
from cyberdyne_backend.domain.ai_chat.entities import ChatMessage, ChatRole

pytestmark = pytest.mark.integration

_SESSION = uuid.uuid4()


def _final_message(content: str) -> ChatMessage:
    return ChatMessage(
        id=uuid.uuid4(),
        session_id=_SESSION,
        role=ChatRole.ASSISTANT,
        content=content,
        created_at=datetime(2026, 6, 17, 12, 0, tzinfo=UTC),
    )


class _StubStreamUC:
    """Stands in for StreamChatTurn; yields a scripted event sequence."""

    def __init__(self, events: list[StreamEvent]) -> None:
        self._events = events

    async def execute(self, **_kwargs) -> AsyncIterator[StreamEvent]:
        for ev in self._events:
            yield ev


def _client(app: FastAPI, events: list[StreamEvent]) -> TestClient:
    app.dependency_overrides[get_stream_turn_uc] = lambda: _StubStreamUC(events)
    return TestClient(app)


def _data_chunks(body: str) -> list[dict]:
    return [
        json.loads(line[len("data: ") :])
        for line in body.splitlines()
        if line.startswith("data: ")
    ]


def test_stream_emits_status_delta_then_done(app: FastAPI) -> None:
    events = [
        StreamEvent(kind="status", text="list_projects"),
        StreamEvent(kind="delta", text="We build "),
        StreamEvent(kind="delta", text="CyberSTAC."),
        StreamEvent(kind="done", message=_final_message("We build CyberSTAC.")),
    ]
    client = _client(app, events)

    resp = client.post(
        f"/api/v1/chat/sessions/{_SESSION}/messages/stream", json={"content": "what?"}
    )
    assert resp.status_code == 200
    assert resp.headers["content-type"].startswith("text/event-stream")

    # Framing: every event is a `data: <json>` line; blank-line separated.
    assert "data: " in resp.text
    chunks = _data_chunks(resp.text)
    assert [c["type"] for c in chunks] == ["status", "delta", "delta", "done"]

    # status carries the tool name; deltas concatenate to the reply.
    assert chunks[0]["tool"] == "list_projects"
    assert "".join(c["text"] for c in chunks if c["type"] == "delta") == "We build CyberSTAC."

    # Terminal `done` carries the full camelCase ChatMessageResponse.
    done = chunks[-1]
    assert done["message"]["content"] == "We build CyberSTAC."
    assert done["message"]["sessionId"] == str(_SESSION)
    assert done["message"]["role"] == "assistant"
    assert "toolCalls" in done["message"]

    # No [DONE] sentinel is ever sent.
    assert "[DONE]" not in resp.text


def test_stream_error_is_delivered_in_band_with_200(app: FastAPI) -> None:
    client = _client(app, [StreamEvent(kind="error", text="provider down")])
    resp = client.post(
        f"/api/v1/chat/sessions/{_SESSION}/messages/stream", json={"content": "hi"}
    )
    # Errors after the stream opens stay HTTP 200, framed as an error event.
    assert resp.status_code == 200
    chunks = _data_chunks(resp.text)
    assert chunks == [{"type": "error", "detail": "provider down"}]
