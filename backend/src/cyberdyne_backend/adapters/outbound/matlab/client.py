"""MATLAB-LLVM backend client for the chat agent.

Mirrors the frontend's ``matlabApi.ts`` contract (the same upstream:
``/v1/repl``, ``/v1/plot``) but server-side, so the agent can run
MATLAB and produce figures during a tool round.

The agent calls **as the signed-in user** — ``bearer`` is forwarded
from the chat request — so figures land in that user's per-session
workspace (``workspace_for(principal, session_id)`` upstream). We
return only the artifact filenames + session id; the frontend fetches
the actual PNG through the authed /api/matlab proxy. Inlining the
bytes here would round-trip the image back into the next LLM call.
"""

from __future__ import annotations

import logging
from typing import Any, cast

import httpx

from cyberdyne_backend.domain.ai_chat import (
    MatlabCheckResult,
    MatlabCodegenResult,
    MatlabDiagnostic,
    MatlabRunResult,
)

logger = logging.getLogger("cyberdyne_backend.matlab")


class MatlabBackendClient:
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

    async def run_repl(
        self, *, source: str, session_id: str, bearer: str | None
    ) -> MatlabRunResult:
        payload: dict[str, object] = {
            "source": source,
            "session_id": session_id,
            "stateful": True,
        }
        body = await self._post("/v1/repl", payload, bearer)
        return self._to_result(body, session_id)

    async def run_plot(
        self, *, source: str, session_id: str, bearer: str | None, fmt: str = "png"
    ) -> MatlabRunResult:
        payload: dict[str, object] = {
            "source": source,
            "session_id": session_id,
            "format": fmt,
        }
        body = await self._post("/v1/plot", payload, bearer)
        return self._to_result(body, session_id)

    async def check(self, *, source: str, session_id: str, bearer: str | None) -> MatlabCheckResult:
        payload: dict[str, object] = {"source": source, "session_id": session_id}
        body = await self._post("/v1/check", payload, bearer)
        return MatlabCheckResult(
            ok=bool(body.get("ok")),
            diagnostics=self._diagnostics(body.get("diagnostics")),
            stdout=str(body.get("stdout") or ""),
            stderr=str(body.get("stderr") or ""),
        )

    async def codegen(
        self, *, source: str, target: str, session_id: str, bearer: str | None
    ) -> MatlabCodegenResult:
        payload: dict[str, object] = {"source": source, "session_id": session_id}
        body = await self._post(f"/v1/codegen/{target}", payload, bearer)
        return MatlabCodegenResult(
            ok=bool(body.get("ok")),
            language=str(body.get("language") or target),
            code=str(body.get("code") or ""),
            diagnostics=self._diagnostics(body.get("diagnostics")),
            stderr=str(body.get("stderr") or ""),
        )

    @staticmethod
    def _diagnostics(raw: object) -> tuple[MatlabDiagnostic, ...]:
        if not isinstance(raw, list):
            return ()
        out: list[MatlabDiagnostic] = []
        for d in raw:
            if not isinstance(d, dict):
                continue
            out.append(
                MatlabDiagnostic(
                    severity=str(d.get("severity") or "error"),
                    message=str(d.get("message") or ""),
                    line=d.get("line") if isinstance(d.get("line"), int) else None,
                    col=d.get("col") if isinstance(d.get("col"), int) else None,
                )
            )
        return tuple(out)

    @staticmethod
    def _to_result(body: dict[str, Any], session_id: str) -> MatlabRunResult:
        return MatlabRunResult(
            ok=bool(body.get("ok")),
            stdout=str(body.get("stdout") or ""),
            stderr=str(body.get("stderr") or ""),
            artifacts=tuple(body.get("artifacts") or []),
            session_id=session_id,
            timed_out=bool(body.get("timed_out")),
        )

    async def _post(
        self, path: str, payload: dict[str, object], bearer: str | None
    ) -> dict[str, Any]:
        url = f"{self._base_url}{path}"
        response = await self._http.post(
            url, json=payload, headers=self._headers(bearer), timeout=self._timeout
        )
        if response.status_code >= 400:
            raise RuntimeError(f"matlab {path} {response.status_code}: {response.text[:240]}")
        return cast(dict[str, Any], response.json())
