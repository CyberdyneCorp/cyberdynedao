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


class TestManimRender:
    async def test_render_posts_then_polls_until_succeeded(self, monkeypatch) -> None:
        # Don't actually sleep between polls.
        import cyberdyne_backend.adapters.outbound.python_interpreter.client as mod

        async def _no_sleep(_seconds: float) -> None:
            return None

        monkeypatch.setattr(mod.asyncio, "sleep", _no_sleep)

        seen: dict[str, object] = {}
        polls = {"n": 0}

        def handler(request: httpx.Request) -> httpx.Response:
            if request.method == "POST" and request.url.path == "/manim/render":
                import json

                seen["body"] = json.loads(request.content)
                seen["auth"] = request.headers.get("authorization")
                return httpx.Response(
                    200, json={"job_id": "job-1", "status": "queued", "session_id": "srv-7"}
                )
            if request.url.path == "/manim/jobs/job-1":
                polls["n"] += 1
                if polls["n"] < 2:
                    return httpx.Response(200, json={"status": "running"})
                return httpx.Response(
                    200,
                    json={
                        "status": "succeeded",
                        "artifacts": [{"name": "Demo.gif", "size_bytes": 9}],
                        "error": None,
                        "stdout": "ok",
                        "stderr": "",
                    },
                )
            raise AssertionError(f"unexpected {request.method} {request.url.path}")

        client = _client_with(handler)
        res = await client.render_manim(
            code="from manim import *",
            scene="Demo",
            session_id="srv-7",
            bearer="tok",
            quality="low",
        )
        assert res.ok is True
        assert res.status == "succeeded"
        assert res.artifacts == ("Demo.gif",)
        assert res.session_id == "srv-7"
        assert seen["auth"] == "Bearer tok"
        assert seen["body"] == {
            "code": "from manim import *",
            "scene": "Demo",
            "quality": "low",
            "output_format": "gif",
            "session_id": "srv-7",
        }
        assert polls["n"] == 2  # polled until terminal

    async def test_render_failed_job_is_not_ok(self, monkeypatch) -> None:
        import cyberdyne_backend.adapters.outbound.python_interpreter.client as mod

        async def _no_sleep(_seconds: float) -> None:
            return None

        monkeypatch.setattr(mod.asyncio, "sleep", _no_sleep)

        def handler(request: httpx.Request) -> httpx.Response:
            if request.url.path == "/manim/render":
                return httpx.Response(200, json={"job_id": "j", "status": "queued"})
            return httpx.Response(
                200, json={"status": "failed", "error": "scene not found", "stderr": "boom"}
            )

        client = _client_with(handler)
        res = await client.render_manim(code="x", scene="Nope", session_id="s", bearer=None)
        assert res.ok is False
        assert res.status == "failed"
        assert res.error == "scene not found"
        assert res.artifacts == ()
