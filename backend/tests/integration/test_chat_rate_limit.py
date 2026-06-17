"""Chat message endpoints are per-IP rate limited (issue #7)."""

from __future__ import annotations

import uuid
from datetime import UTC, datetime

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from cyberdyne_backend.adapters.inbound.api.ai_chat import router as chat_router
from cyberdyne_backend.adapters.inbound.api.ai_chat.router import get_run_turn_uc
from cyberdyne_backend.adapters.inbound.api.rate_limit import SlidingWindowRateLimiter
from cyberdyne_backend.domain.ai_chat.entities import ChatMessage, ChatRole

pytestmark = pytest.mark.integration

_SESSION = uuid.uuid4()


class _FakeRunTurn:
    async def execute(self, *, session_id, user_content, **_kwargs) -> ChatMessage:
        return ChatMessage(
            id=uuid.uuid4(),
            session_id=session_id,
            role=ChatRole.ASSISTANT,
            content="ok",
            created_at=datetime(2026, 6, 17, 12, 0, tzinfo=UTC),
        )


def test_chat_messages_are_rate_limited(app: FastAPI, monkeypatch) -> None:
    # Shrink the per-IP cap to 1/min so the second call trips the guard.
    monkeypatch.setattr(
        chat_router,
        "_chat_rate_limiter",
        SlidingWindowRateLimiter(limit=1, window_s=60.0, detail="too many chat messages"),
    )
    app.dependency_overrides[get_run_turn_uc] = lambda: _FakeRunTurn()
    client = TestClient(app)

    first = client.post(f"/api/v1/chat/sessions/{_SESSION}/messages", json={"content": "hi"})
    assert first.status_code == 200, first.text

    second = client.post(f"/api/v1/chat/sessions/{_SESSION}/messages", json={"content": "again"})
    assert second.status_code == 429
    assert second.json()["detail"] == "too many chat messages"
