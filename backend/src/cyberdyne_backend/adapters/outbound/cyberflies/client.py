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

from cyberdyne_backend.domain.ai_chat import MeetingDetail, MeetingSummary

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

    async def get_meeting(self, *, meeting_id: str, bearer: str | None) -> MeetingDetail | None:
        url = f"{self._base_url}/api/v1/recordings/{meeting_id}"
        response = await self._http.get(url, headers=self._headers(bearer), timeout=self._timeout)
        if response.status_code == 404:
            return None
        if response.status_code >= 400:
            raise RuntimeError(
                f"cyberflies /api/v1/recordings/{meeting_id} "
                f"{response.status_code}: {response.text[:240]}"
            )
        return self._to_detail(cast(dict[str, Any], response.json()))

    @staticmethod
    def _to_detail(body: dict[str, Any]) -> MeetingDetail:
        summary = body.get("summary")
        summary = summary if isinstance(summary, dict) else {}
        transcription = body.get("transcription")
        transcription = transcription if isinstance(transcription, dict) else {}
        raw_bullets = summary.get("bullets")
        bullets = tuple(str(b) for b in raw_bullets) if isinstance(raw_bullets, list) else ()
        duration = transcription.get("duration_seconds")
        return MeetingDetail(
            id=str(body.get("id", "")),
            headline=str(summary.get("headline") or ""),
            abstract=str(summary.get("abstract") or ""),
            bullets=bullets,
            transcript=str(transcription.get("text") or ""),
            status=str(body.get("status", "")),
            created_at=str(body.get("captured_at") or body.get("created_at") or ""),
            word_count=int(transcription.get("word_count") or 0),
            duration_seconds=float(duration) if duration is not None else None,
        )

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
