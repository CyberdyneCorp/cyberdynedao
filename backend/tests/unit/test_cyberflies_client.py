"""Unit tests for the Cyberflies outbound client.

Covers the wire-format mapping for ``get_meeting`` (summary + transcription
→ MeetingDetail), the 404 → None path, and bearer forwarding — the bits the
agent dispatch tests don't exercise because they use a fake port.
"""

from __future__ import annotations

import httpx

from cyberdyne_backend.adapters.outbound.cyberflies.client import CyberfliesClient


def _client_with(handler):
    transport = httpx.MockTransport(handler)
    http = httpx.AsyncClient(transport=transport)
    return CyberfliesClient(base_url="https://flies.example/", http_client=http)


class TestCyberfliesClient:
    async def test_get_meeting_maps_summary_and_transcript(self) -> None:
        seen: dict[str, object] = {}

        def handler(request: httpx.Request) -> httpx.Response:
            seen["path"] = request.url.path
            seen["auth"] = request.headers.get("authorization")
            return httpx.Response(
                200,
                json={
                    "id": "rec-7",
                    "status": "completed",
                    "captured_at": "2026-06-02T10:00:00Z",
                    "summary": {
                        "headline": "Sprint planning",
                        "abstract": "Planned the sprint.",
                        "bullets": ["Pick stories", "Estimate"],
                    },
                    "transcription": {
                        "text": "We planned the sprint.",
                        "word_count": 4,
                        "duration_seconds": 600.5,
                    },
                },
            )

        client = _client_with(handler)
        detail = await client.get_meeting(meeting_id="rec-7", bearer="tok-9")
        assert detail is not None
        assert detail.id == "rec-7"
        assert detail.headline == "Sprint planning"
        assert detail.abstract == "Planned the sprint."
        assert detail.bullets == ("Pick stories", "Estimate")
        assert detail.transcript == "We planned the sprint."
        assert detail.word_count == 4
        assert detail.duration_seconds == 600.5
        assert detail.created_at == "2026-06-02T10:00:00Z"
        assert seen["path"] == "/api/v1/recordings/rec-7"
        assert seen["auth"] == "Bearer tok-9"

    async def test_get_meeting_returns_none_on_404(self) -> None:
        def handler(request: httpx.Request) -> httpx.Response:
            return httpx.Response(404, json={"detail": "not found"})

        client = _client_with(handler)
        assert await client.get_meeting(meeting_id="missing", bearer="t") is None

    async def test_get_meeting_tolerates_missing_summary_and_transcription(self) -> None:
        def handler(request: httpx.Request) -> httpx.Response:
            return httpx.Response(
                200, json={"id": "rec-8", "status": "processing", "created_at": "2026-06-03"}
            )

        client = _client_with(handler)
        detail = await client.get_meeting(meeting_id="rec-8", bearer="t")
        assert detail is not None
        assert detail.id == "rec-8"
        assert detail.headline == ""
        assert detail.bullets == ()
        assert detail.transcript == ""
        assert detail.word_count == 0
        assert detail.duration_seconds is None
        assert detail.created_at == "2026-06-03"
