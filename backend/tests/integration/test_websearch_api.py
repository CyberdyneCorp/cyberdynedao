"""API tests for the /search endpoint: auth gating, response shape, and
error mapping. The web-search port is faked — no network."""

from __future__ import annotations

import uuid
from datetime import UTC, datetime

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from cyberdyne_backend.adapters.inbound.api.websearch.router import get_search_web_uc
from cyberdyne_backend.adapters.inbound.middleware.auth import require_principal
from cyberdyne_backend.application.websearch import SearchWeb
from cyberdyne_backend.domain.auth_identity import UserPrincipal
from cyberdyne_backend.domain.websearch import (
    SearchProviderError,
    SearchResponse,
    SearchResult,
)

pytestmark = pytest.mark.integration


def _learner() -> UserPrincipal:
    return UserPrincipal(
        user_id=uuid.uuid4(),
        username="l",
        scopes=frozenset(),
        audience=None,
        expires_at=datetime(2026, 7, 1, tzinfo=UTC),
    )


class _Port:
    def __init__(self, error: Exception | None = None) -> None:
        self._error = error
        self.calls: list[tuple[str, int]] = []

    async def search(self, query: str, *, num_results: int) -> SearchResponse:
        self.calls.append((query, num_results))
        if self._error is not None:
            raise self._error
        return SearchResponse(
            query=query,
            answer="a direct answer",
            results=(
                SearchResult(
                    position=1,
                    title="Result One",
                    url="https://one.example",
                    snippet="snippet one",
                    source="one.example",
                ),
            ),
        )


def _client(app: FastAPI, provider: object) -> TestClient:
    app.dependency_overrides[require_principal] = _learner
    app.dependency_overrides[get_search_web_uc] = lambda: SearchWeb(provider=provider)  # type: ignore[arg-type]
    return TestClient(app)


class TestSearchEndpoint:
    def test_requires_authentication(self, app: FastAPI) -> None:
        client = TestClient(app)
        assert client.get("/api/v1/search", params={"q": "hi"}).status_code == 401

    def test_returns_results(self, app: FastAPI) -> None:
        port = _Port()
        client = _client(app, port)
        response = client.get("/api/v1/search", params={"q": "cyberdyne", "num": 5})
        assert response.status_code == 200
        assert response.json() == {
            "query": "cyberdyne",
            "answer": "a direct answer",
            "results": [
                {
                    "position": 1,
                    "title": "Result One",
                    "url": "https://one.example",
                    "snippet": "snippet one",
                    "source": "one.example",
                }
            ],
        }
        assert port.calls == [("cyberdyne", 5)]

    def test_missing_query_is_422(self, app: FastAPI) -> None:
        client = _client(app, _Port())
        assert client.get("/api/v1/search").status_code == 422

    def test_out_of_range_num_is_422(self, app: FastAPI) -> None:
        client = _client(app, _Port())
        assert client.get("/api/v1/search", params={"q": "x", "num": 99}).status_code == 422

    def test_unconfigured_provider_is_503(self, app: FastAPI) -> None:
        # provider=None models an unset SERPAPI key.
        client = _client(app, None)
        assert client.get("/api/v1/search", params={"q": "x"}).status_code == 503

    def test_provider_error_is_503(self, app: FastAPI) -> None:
        client = _client(app, _Port(error=SearchProviderError("quota exhausted")))
        assert client.get("/api/v1/search", params={"q": "x"}).status_code == 503
