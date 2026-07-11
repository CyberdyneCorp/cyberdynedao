"""SERPAPI web-search adapter (Google engine) — ``httpx``-only.

Maps SERPAPI's ``/search.json`` response to the domain ``SearchResponse``:
organic results plus a direct answer when an answer box is present.
Transport failures and engine errors (bad key, quota) map to
``SearchProviderError`` so the caller can distinguish "retry / fix ops"
from "empty results".
"""

from __future__ import annotations

import logging
from typing import Any, cast

import httpx

from cyberdyne_backend.domain.websearch import (
    SearchProviderError,
    SearchResponse,
    SearchResult,
)

logger = logging.getLogger("cyberdyne_backend.serpapi")

_DEFAULT_BASE_URL = "https://serpapi.com"


class SerpApiClient:
    """``WebSearchPort`` implementation over SERPAPI's Google engine."""

    def __init__(
        self,
        *,
        api_key: str,
        http_client: httpx.AsyncClient,
        base_url: str = _DEFAULT_BASE_URL,
        timeout_s: float = 15.0,
    ) -> None:
        if not api_key:
            raise ValueError("SERPAPI api_key is required")
        self._api_key = api_key
        self._http = http_client
        self._base_url = base_url.rstrip("/")
        self._timeout_s = timeout_s

    async def search(self, query: str, *, num_results: int) -> SearchResponse:
        params = {
            "engine": "google",
            "q": query,
            "num": str(num_results),
            "api_key": self._api_key,
            "hl": "en",
        }
        try:
            response = await self._http.get(
                f"{self._base_url}/search.json", params=params, timeout=self._timeout_s
            )
        except httpx.HTTPError as exc:
            raise SearchProviderError(f"could not reach SERPAPI: {exc}") from exc
        if response.status_code >= 400:
            # SERPAPI reports bad key / quota as a JSON ``error`` body.
            detail = _error_detail(response)
            raise SearchProviderError(f"SERPAPI error {response.status_code}: {detail}")
        payload = cast(dict[str, Any], response.json())
        if payload.get("error"):
            raise SearchProviderError(f"SERPAPI error: {payload['error']}")
        return _to_response(query, payload)


def _error_detail(response: httpx.Response) -> str:
    try:
        body = response.json()
    except ValueError:
        return response.text[:200]
    if isinstance(body, dict) and body.get("error"):
        return str(body["error"])
    return response.text[:200]


def _to_response(query: str, payload: dict[str, Any]) -> SearchResponse:
    results = []
    for index, entry in enumerate(payload.get("organic_results") or [], start=1):
        if not isinstance(entry, dict):
            continue
        link = entry.get("link")
        if not link:
            continue
        results.append(
            SearchResult(
                position=int(entry.get("position") or index),
                title=str(entry.get("title") or ""),
                url=str(link),
                snippet=str(entry.get("snippet") or ""),
                source=str(entry.get("source") or entry.get("displayed_link") or ""),
            )
        )
    return SearchResponse(
        query=query,
        results=tuple(results),
        answer=_answer_from(payload),
    )


def _answer_from(payload: dict[str, Any]) -> str | None:
    """Best-effort direct answer from the answer box, if present. Answer
    boxes vary in shape; prefer an explicit ``answer``, then a snippet."""
    box = payload.get("answer_box")
    if not isinstance(box, dict):
        return None
    for key in ("answer", "snippet", "result"):
        value = box.get(key)
        if isinstance(value, str) and value.strip():
            return value.strip()
    return None
