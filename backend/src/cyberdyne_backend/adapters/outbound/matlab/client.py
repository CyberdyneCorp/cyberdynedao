"""MATLAB-LLVM backend client for the chat agent.

Mirrors the frontend's ``matlabApi.ts`` contract (the same upstream:
``/v1/repl``, ``/v1/plot``, ``/v1/files/{path}``) but server-side, so
the agent can run MATLAB and capture figures during a tool round.

The agent calls **as the signed-in user** — ``bearer`` is forwarded
from the chat request — so figures land in that user's per-session
workspace (``workspace_for(principal, session_id)`` upstream). After a
plot, we pull the first artifact's bytes and base64-encode them into
the result so the frontend can render the figure inline without a
second authenticated round-trip.
"""

from __future__ import annotations

import base64
import logging
from typing import Any, cast

import httpx

from cyberdyne_backend.domain.ai_chat import MatlabRunResult

logger = logging.getLogger("cyberdyne_backend.matlab")


class MatlabBackendClient:
    def __init__(self, base_url: str, http_client: httpx.AsyncClient, timeout_s: float = 60.0) -> None:
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
        artifacts = tuple(body.get("artifacts") or [])
        # REPL turns can also emit figures (e.g. a saveas); surface the
        # first one inline just like /v1/plot does.
        image_b64, ctype = await self._maybe_fetch_image(artifacts, session_id, bearer)
        return MatlabRunResult(
            ok=bool(body.get("ok")),
            stdout=str(body.get("stdout") or ""),
            stderr=str(body.get("stderr") or ""),
            artifacts=artifacts,
            image_base64=image_b64,
            image_content_type=ctype,
            session_id=session_id,
            timed_out=bool(body.get("timed_out")),
        )

    async def run_plot(
        self, *, source: str, session_id: str, bearer: str | None, fmt: str = "png"
    ) -> MatlabRunResult:
        payload: dict[str, object] = {
            "source": source,
            "session_id": session_id,
            "format": fmt,
        }
        body = await self._post("/v1/plot", payload, bearer)
        artifacts = tuple(body.get("artifacts") or [])
        image_b64, ctype = await self._maybe_fetch_image(artifacts, session_id, bearer)
        return MatlabRunResult(
            ok=bool(body.get("ok")),
            stdout=str(body.get("stdout") or ""),
            stderr=str(body.get("stderr") or ""),
            artifacts=artifacts,
            image_base64=image_b64,
            image_content_type=ctype,
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

    async def _maybe_fetch_image(
        self, artifacts: tuple[str, ...], session_id: str, bearer: str | None
    ) -> tuple[str | None, str | None]:
        """Download the first image artifact and base64-encode it.
        Returns ``(None, None)`` when there's no image or the fetch
        fails — a missing figure shouldn't fail the whole tool call."""
        image_path = next(
            (a for a in artifacts if a.lower().endswith((".png", ".jpg", ".jpeg", ".svg"))),
            None,
        )
        if not image_path:
            return None, None
        url = f"{self._base_url}/v1/files/{image_path}"
        try:
            response = await self._http.get(
                url,
                params={"session_id": session_id},
                headers={"authorization": f"Bearer {bearer}"} if bearer else {},
                timeout=self._timeout,
            )
        except httpx.HTTPError as exc:
            logger.warning("matlab artifact fetch failed: %s", exc)
            return None, None
        if response.status_code != 200:
            logger.info("matlab artifact %s non-200: %s", image_path, response.status_code)
            return None, None
        ctype = response.headers.get("content-type", "image/png")
        return base64.b64encode(response.content).decode("ascii"), ctype
