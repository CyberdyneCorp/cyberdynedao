"""End-to-end tests for the notebook AI endpoints (issue #187).

The use cases are overridden with fakes backed by a scripted LLM, so the
route wiring + persistence are exercised without a real OpenAI key.
"""

from __future__ import annotations

import uuid
from collections.abc import AsyncIterator
from datetime import UTC, datetime

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from cyberdyne_backend.adapters.inbound.api.notebook.router import (
    get_generate_flashcards_uc,
    get_summarize_note_uc,
)
from cyberdyne_backend.adapters.inbound.middleware.auth import require_principal
from cyberdyne_backend.adapters.outbound.persistence.notebook.repository import (
    SqlAlchemyNotebookRepository,
)
from cyberdyne_backend.application.notebook import GenerateFlashcards, SummarizeNote
from cyberdyne_backend.domain.ai_chat import LLMResponse
from cyberdyne_backend.domain.auth_identity import UserPrincipal
from cyberdyne_backend.infrastructure.database.engine import session_scope

pytestmark = pytest.mark.integration

_USER = uuid.UUID("c3c3c3c3-c3c3-c3c3-c3c3-c3c3c3c3c3c3")


def _principal() -> UserPrincipal:
    return UserPrincipal(
        user_id=_USER,
        username="learner",
        scopes=frozenset(),
        audience=None,
        expires_at=datetime(2999, 1, 1, tzinfo=UTC),
    )


class _ScriptedLLM:
    def __init__(self, reply: str) -> None:
        self._reply = reply

    async def complete(self, *, messages, tools, system_prompt) -> LLMResponse:
        return LLMResponse(content=self._reply, model="fake")


@pytest.fixture
def client(app: FastAPI, _prepared_schema: None) -> TestClient:
    app.dependency_overrides[require_principal] = lambda: _principal()
    return TestClient(app)


def _wire_llm(app: FastAPI, reply: str) -> None:
    async def _gen() -> AsyncIterator[GenerateFlashcards]:
        async with session_scope() as session:
            yield GenerateFlashcards(
                repo=SqlAlchemyNotebookRepository(session), llm=_ScriptedLLM(reply)
            )

    async def _sum() -> AsyncIterator[SummarizeNote]:
        async with session_scope() as session:
            yield SummarizeNote(repo=SqlAlchemyNotebookRepository(session), llm=_ScriptedLLM(reply))

    app.dependency_overrides[get_generate_flashcards_uc] = _gen
    app.dependency_overrides[get_summarize_note_uc] = _sum


def _new_note(client: TestClient) -> str:
    resp = client.post(
        "/api/v1/notebook/notes",
        json={"title": "Ohm's Law", "type": "theory", "body": "V = I*R"},
    )
    return resp.json()["id"]


def test_generate_flashcards_persists_and_lists(app: FastAPI, client: TestClient) -> None:
    _wire_llm(app, '[{"question": "What is V=IR?", "answer": "Ohm\'s law"}]')
    nid = _new_note(client)

    gen = client.post(f"/api/v1/notebook/notes/{nid}/flashcards/generate")
    assert gen.status_code == 201, gen.text
    assert [c["question"] for c in gen.json()] == ["What is V=IR?"]

    # Generated cards are persisted alongside any manual ones.
    listed = client.get(f"/api/v1/notebook/notes/{nid}/flashcards")
    assert [c["answer"] for c in listed.json()] == ["Ohm's law"]


def test_generate_offline_returns_empty(app: FastAPI, client: TestClient) -> None:
    _wire_llm(app, "offline mode — no JSON")
    nid = _new_note(client)
    gen = client.post(f"/api/v1/notebook/notes/{nid}/flashcards/generate")
    assert gen.status_code == 201
    assert gen.json() == []


def test_summarize_persists_ai_summary(app: FastAPI, client: TestClient) -> None:
    _wire_llm(app, "Ohm's law links V, I and R.")
    nid = _new_note(client)

    summ = client.post(f"/api/v1/notebook/notes/{nid}/summary")
    assert summ.status_code == 200, summ.text
    assert summ.json()["aiSummary"] == "Ohm's law links V, I and R."

    # Persisted: a later GET shows the summary.
    assert client.get(f"/api/v1/notebook/notes/{nid}").json()["aiSummary"] == (
        "Ohm's law links V, I and R."
    )


def test_generate_on_missing_note_404(app: FastAPI, client: TestClient) -> None:
    _wire_llm(app, "[]")
    resp = client.post(f"/api/v1/notebook/notes/{uuid.uuid4()}/flashcards/generate")
    assert resp.status_code == 404
