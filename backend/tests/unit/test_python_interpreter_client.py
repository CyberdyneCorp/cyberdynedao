"""Unit tests for the Python interpreter outbound client.

Covers the wire-format mapping (especially FileMeta artifacts → names),
bearer forwarding, and error surfacing — the bits the agent dispatch
tests don't exercise because they use a fake port.
"""

from __future__ import annotations

import httpx
import pytest

from cyberdyne_backend.adapters.outbound.python_interpreter.client import (
    PythonInterpreterClient,
)


def _client_with(handler):
    transport = httpx.MockTransport(handler)
    http = httpx.AsyncClient(transport=transport)
    return PythonInterpreterClient(base_url="https://interp.example/", http_client=http)


class TestPythonInterpreterClient:
    async def test_execute_maps_response_and_forwards_bearer(self) -> None:
        seen: dict[str, object] = {}

        def handler(request: httpx.Request) -> httpx.Response:
            seen["path"] = request.url.path
            seen["auth"] = request.headers.get("authorization")
            import json

            seen["body"] = json.loads(request.content)
            return httpx.Response(
                200,
                json={
                    "success": True,
                    "result": "45",
                    "stdout": "45\n",
                    "stderr": "",
                    "error": None,
                    "artifacts": [
                        {"name": "plot.png", "size_bytes": 10, "modified_at": 1.0},
                        {"name": "data.csv", "size_bytes": 5, "modified_at": 2.0},
                    ],
                },
            )

        client = _client_with(handler)
        res = await client.execute(code="print(sum(range(10)))", session_id="srv-1", bearer="tok-1")
        assert res.ok is True
        assert res.stdout == "45\n"
        assert res.result == "45"
        assert res.artifacts == ("plot.png", "data.csv")
        assert res.session_id == "srv-1"
        assert seen["path"] == "/execute"
        assert seen["auth"] == "Bearer tok-1"
        # restricted defaults to True — the backend forbids unrestricted.
        assert seen["body"] == {
            "code": "print(sum(range(10)))",
            "session_id": "srv-1",
            "restricted": True,
        }

    async def test_create_session_returns_server_id(self) -> None:
        seen: dict[str, object] = {}

        def handler(request: httpx.Request) -> httpx.Response:
            seen["path"] = request.url.path
            seen["auth"] = request.headers.get("authorization")
            return httpx.Response(200, json={"session_id": "srv-xyz"})

        client = _client_with(handler)
        sid = await client.create_session(bearer="tok-2")
        assert sid == "srv-xyz"
        assert seen["path"] == "/sessions"
        assert seen["auth"] == "Bearer tok-2"

    async def test_execute_tolerates_string_or_missing_artifacts(self) -> None:
        def handler(request: httpx.Request) -> httpx.Response:
            return httpx.Response(
                200,
                json={
                    "success": False,
                    "stdout": "",
                    "stderr": "boom",
                    "error": "NameError",
                    "artifacts": ["legacy.txt", {"no_name": 1}, 42],
                },
            )

        client = _client_with(handler)
        res = await client.execute(code="x", session_id="s", bearer=None)
        assert res.ok is False
        assert res.error == "NameError"
        # String entries kept; malformed entries dropped.
        assert res.artifacts == ("legacy.txt",)

    async def test_execute_raises_on_http_error(self) -> None:
        client = _client_with(lambda r: httpx.Response(500, json={"detail": "kaboom"}))
        with pytest.raises(RuntimeError, match="python_interpreter /execute 500"):
            await client.execute(code="x", session_id="s", bearer=None)
