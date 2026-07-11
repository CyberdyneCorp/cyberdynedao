"""Unit tests for the websearch context: use case, and the SERPAPI
client's response mapping + error handling (httpx mocked)."""

from __future__ import annotations

import httpx
import pytest

from cyberdyne_backend.adapters.outbound.websearch import SerpApiClient
from cyberdyne_backend.application.websearch import SearchWeb
from cyberdyne_backend.domain.websearch import (
    InvalidQueryError,
    SearchProviderError,
    SearchResponse,
    SearchResult,
    SearchUnavailableError,
    clamp_num_results,
)


class TestClamp:
    @pytest.mark.parametrize(("given", "expected"), [(0, 1), (1, 1), (10, 10), (20, 20), (99, 20)])
    def test_clamp(self, given: int, expected: int) -> None:
        assert clamp_num_results(given) == expected


class _FakePort:
    def __init__(self) -> None:
        self.calls: list[tuple[str, int]] = []

    async def search(self, query: str, *, num_results: int) -> SearchResponse:
        self.calls.append((query, num_results))
        return SearchResponse(
            query=query,
            results=(SearchResult(position=1, title="T", url="https://x", snippet="s"),),
            answer="42",
        )


class TestSearchWebUseCase:
    async def test_trims_query_and_clamps_num(self) -> None:
        port = _FakePort()
        result = await SearchWeb(provider=port).execute("  hello  ", num_results=99)
        assert result.query == "hello"
        assert port.calls == [("hello", 20)]

    async def test_empty_query_rejected(self) -> None:
        with pytest.raises(InvalidQueryError):
            await SearchWeb(provider=_FakePort()).execute("   ")

    async def test_no_provider_is_unavailable(self) -> None:
        with pytest.raises(SearchUnavailableError):
            await SearchWeb(provider=None).execute("anything")


def _client_returning(handler: object) -> SerpApiClient:
    http = httpx.AsyncClient(transport=httpx.MockTransport(handler))  # type: ignore[arg-type]
    return SerpApiClient(api_key="serp-test", http_client=http)


class TestSerpApiClient:
    async def test_maps_organic_results_and_answer(self) -> None:
        captured: dict[str, str] = {}

        def handler(request: httpx.Request) -> httpx.Response:
            captured.update(dict(request.url.params))
            return httpx.Response(
                200,
                json={
                    "answer_box": {"answer": "Paris"},
                    "organic_results": [
                        {
                            "position": 1,
                            "title": "France",
                            "link": "https://a.example",
                            "snippet": "About France",
                            "source": "a.example",
                        },
                        {"title": "no link dropped"},  # no link -> skipped
                        {
                            "title": "Second",
                            "link": "https://b.example",
                            "displayed_link": "b.example",
                        },
                    ],
                },
            )

        result = await _client_returning(handler).search("capital of france", num_results=5)
        assert captured["engine"] == "google"
        assert captured["q"] == "capital of france"
        assert captured["num"] == "5"
        assert result.answer == "Paris"
        assert [r.url for r in result.results] == ["https://a.example", "https://b.example"]
        assert result.results[0].source == "a.example"
        # position falls back to the raw-list rank (3rd entry) when absent.
        assert result.results[1].position == 3
        assert result.results[1].source == "b.example"

    async def test_no_answer_box_yields_none_answer(self) -> None:
        def handler(_request: httpx.Request) -> httpx.Response:
            return httpx.Response(200, json={"organic_results": []})

        result = await _client_returning(handler).search("q", num_results=10)
        assert result.answer is None
        assert result.results == ()

    async def test_error_body_raises_provider_error(self) -> None:
        def handler(_request: httpx.Request) -> httpx.Response:
            return httpx.Response(401, json={"error": "Invalid API key."})

        with pytest.raises(SearchProviderError, match="401"):
            await _client_returning(handler).search("q", num_results=10)

    async def test_error_field_on_200_raises(self) -> None:
        def handler(_request: httpx.Request) -> httpx.Response:
            return httpx.Response(200, json={"error": "Your account has run out of searches."})

        with pytest.raises(SearchProviderError, match="run out"):
            await _client_returning(handler).search("q", num_results=10)

    async def test_transport_error_raises_provider_error(self) -> None:
        def handler(_request: httpx.Request) -> httpx.Response:
            raise httpx.ConnectError("boom")

        with pytest.raises(SearchProviderError, match="could not reach"):
            await _client_returning(handler).search("q", num_results=10)
