"""Ports for the websearch context."""

from __future__ import annotations

from typing import Protocol, runtime_checkable

from cyberdyne_backend.domain.websearch.entities import SearchResponse


@runtime_checkable
class WebSearchPort(Protocol):
    """Runs a web search and returns organic results (+ an optional direct
    answer).

    Implementations talk to a search engine over HTTP and may be rate
    limited or quota-capped; callers should expect ``SearchProviderError``.
    """

    async def search(self, query: str, *, num_results: int) -> SearchResponse: ...
