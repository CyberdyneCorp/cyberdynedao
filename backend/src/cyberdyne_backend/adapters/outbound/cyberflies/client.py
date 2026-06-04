"""Cyberflies (meetings) backend client for the chat agent.

Lets the agent answer questions about the signed-in user's recorded
meetings. ``ask_meetings`` delegates to Cyberflies' own meeting-aware
chat agent (which has semantic search over transcripts), and
``list_meetings`` enumerates the user's recordings.

The agent calls **as the signed-in user** — ``bearer`` is forwarded from
the chat request — so it only ever sees that user's meetings.
"""

from __future__ import annotations

import logging
from typing import Any, cast

import httpx

from cyberdyne_backend.domain.ai_chat import MeetingSummary

logger = logging.getLogger("cyberdyne_backend.cyberflies")


class CyberfliesClient:
    def __init__(
        self, base_url: str, http_client: httpx.AsyncClient, timeout_s: float = 60.0
    ) -> None:
        self._base_url = base_url.rstrip("/")
        self._http = http_client
        self._timeout = timeout_s

    def _headers(self, bearer: str | None) -> dict[str, str]:
        headers = {"content-type": "application/json", "accept": "application/json"}
        if bearer:
            headers["authorization"] = f"Bearer {bearer}"
        return headers

    async def ask_meetings(self, *, question: str, bearer: str | None) -> str:
        body = await self._request(
            "POST",
            "/api/v1/chat",
            bearer,
            json={"messages": [{"role": "user", "content": question}]},
        )
        return str(body.get("reply") or "")

    async def list_meetings(self, *, bearer: str | None) -> tuple[MeetingSummary, ...]:
        body = await self._request("GET", "/api/v1/recordings?limit=50", bearer)
        items = body.get("items")
        if not isinstance(items, list):
            return ()
        out: list[MeetingSummary] = []
        for it in items:
            if not isinstance(it, dict):
                continue
            summary = it.get("summary")
            headline = (
                summary.get("headline")
                if isinstance(summary, dict) and summary.get("headline")
                else f"Recording {str(it.get('id', ''))[:8]}"
            )
            out.append(
                MeetingSummary(
                    id=str(it.get("id", "")),
                    headline=str(headline),
                    status=str(it.get("status", "")),
                    created_at=str(it.get("captured_at") or it.get("created_at") or ""),
                )
            )
        return tuple(out)

    async def _request(
        self,
        method: str,
        path: str,
        bearer: str | None,
        *,
        json: dict[str, object] | None = None,
    ) -> dict[str, Any]:
        url = f"{self._base_url}{path}"
        response = await self._http.request(
            method, url, json=json, headers=self._headers(bearer), timeout=self._timeout
        )
        if response.status_code >= 400:
            raise RuntimeError(f"cyberflies {path} {response.status_code}: {response.text[:240]}")
        return cast(dict[str, Any], response.json())
