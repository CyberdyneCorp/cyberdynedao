"""Web search use case — open-web search for the chat agents."""

from __future__ import annotations

from dataclasses import dataclass

from cyberdyne_backend.domain.websearch import (
    DEFAULT_RESULTS,
    InvalidQueryError,
    SearchResponse,
    SearchUnavailableError,
    WebSearchPort,
    clamp_num_results,
)


@dataclass(slots=True)
class SearchWeb:
    """Runs a web search, returning organic results and an optional direct
    answer.

    The provider is optional: when web search is not configured (no
    SERPAPI key) it is ``None`` and every call raises
    ``SearchUnavailableError`` so the endpoint degrades to 503 rather than
    silently returning nothing.
    """

    provider: WebSearchPort | None

    async def execute(self, query: str, *, num_results: int = DEFAULT_RESULTS) -> SearchResponse:
        cleaned = query.strip()
        if not cleaned:
            raise InvalidQueryError("query cannot be empty")
        if self.provider is None:
            raise SearchUnavailableError("web search is not configured (SERPAPI_KEY not set)")
        return await self.provider.search(cleaned, num_results=clamp_num_results(num_results))
