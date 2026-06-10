"""Python interpreter backend client for the chat agent.

Mirrors the frontend's ``interpreterApi.ts`` contract (the same upstream:
``POST /execute``) but server-side, so the agent can run Python and
produce files during a tool round.

The agent calls **as the signed-in user** — ``bearer`` is forwarded from
the chat request — so files land in that user's per-session workspace.
We return only the artifact filenames + session id; the frontend fetches
the actual file through the authed /api/interpreter proxy. Inlining the
bytes here would round-trip the file back into the next LLM call.
"""

from __future__ import annotations

import asyncio
import logging
from typing import Any, cast

import httpx

from cyberdyne_backend.domain.ai_chat import ManimRenderResult, PythonExecResult

logger = logging.getLogger("cyberdyne_backend.python_interpreter")

# Manim renders run as an async job on the backend; we poll until terminal.
_MANIM_POLL_INTERVAL_S = 2.0
_MANIM_POLL_BUDGET_S = 150.0
_MANIM_TERMINAL = {"succeeded", "failed", "error", "cancelled"}


class PythonInterpreterClient:
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

    async def create_session(self, *, bearer: str | None) -> str:
        body = await self._post("/sessions", {}, bearer)
        return str(body["session_id"])

    async def execute(
        self, *, code: str, session_id: str, bearer: str | None, restricted: bool = True
    ) -> PythonExecResult:
        payload: dict[str, object] = {
            "code": code,
            "session_id": session_id,
            "restricted": restricted,
        }
        body = await self._post("/execute", payload, bearer)
        return self._to_result(body, session_id)

    async def render_manim(
        self,
        *,
        code: str,
        scene: str,
        session_id: str,
        bearer: str | None,
        quality: str = "medium",
        output_format: str = "gif",
    ) -> ManimRenderResult:
        payload: dict[str, object] = {
            "code": code,
            "scene": scene,
            "quality": quality,
            "output_format": output_format,
            "session_id": session_id,
        }
        accepted = await self._post("/manim/render", payload, bearer)
        job_id = str(accepted.get("job_id") or "")
        sid = str(accepted.get("session_id") or session_id)
        if not job_id:
            return ManimRenderResult(
                ok=False, scene=scene, status="failed", session_id=sid, error="no job id returned"
            )
        # Poll the job to a terminal state. The render is genuinely async on
        # the backend (a low-quality scene is ~10s); cap the wait so a stuck
        # job can't hang the chat turn.
        max_polls = int(_MANIM_POLL_BUDGET_S / _MANIM_POLL_INTERVAL_S)
        job: dict[str, Any] = {}
        for _ in range(max_polls):
            job = await self._get(f"/manim/jobs/{job_id}", bearer)
            status = str(job.get("status") or "")
            if status in _MANIM_TERMINAL:
                return self._to_manim_result(job, scene, sid)
            await asyncio.sleep(_MANIM_POLL_INTERVAL_S)
        return ManimRenderResult(
            ok=False,
            scene=scene,
            status="timeout",
            session_id=sid,
            error=f"render did not finish within {int(_MANIM_POLL_BUDGET_S)}s",
        )

    async def upload_file(
        self,
        *,
        session_id: str,
        filename: str,
        content: bytes,
        content_type: str,
        bearer: str | None,
    ) -> str:
        headers: dict[str, str] = {"accept": "application/json"}
        if bearer:
            headers["authorization"] = f"Bearer {bearer}"
        url = f"{self._base_url}/files?session_id={session_id}"
        response = await self._http.post(
            url,
            files={"file": (filename, content, content_type)},
            headers=headers,
            timeout=self._timeout,
        )
        if response.status_code >= 400:
            raise RuntimeError(
                f"python_interpreter /files {response.status_code}: {response.text[:240]}"
            )
        body = cast(dict[str, Any], response.json())
        file_meta = body.get("file")
        if isinstance(file_meta, dict) and isinstance(file_meta.get("name"), str):
            return cast(str, file_meta["name"])
        return filename

    @staticmethod
    def _artifact_names(raw_artifacts: object) -> list[str]:
        # Upstream artifacts are FileMeta objects ({name, size_bytes,
        # modified_at}); keep just the names, like the MATLAB client.
        names: list[str] = []
        if isinstance(raw_artifacts, list):
            for a in raw_artifacts:
                if isinstance(a, dict) and isinstance(a.get("name"), str):
                    names.append(a["name"])
                elif isinstance(a, str):
                    names.append(a)
        return names

    def _to_manim_result(
        self, job: dict[str, Any], scene: str, session_id: str
    ) -> ManimRenderResult:
        status = str(job.get("status") or "")
        names = self._artifact_names(job.get("artifacts"))
        error = job.get("error")
        return ManimRenderResult(
            ok=status == "succeeded" and bool(names),
            scene=scene,
            status=status,
            artifacts=tuple(names),
            session_id=session_id,
            error=str(error) if error is not None else None,
            stdout=str(job.get("stdout") or ""),
            stderr=str(job.get("stderr") or ""),
        )

    def _to_result(self, body: dict[str, Any], session_id: str) -> PythonExecResult:
        names = self._artifact_names(body.get("artifacts"))
        result = body.get("result")
        error = body.get("error")
        return PythonExecResult(
            ok=bool(body.get("success")),
            stdout=str(body.get("stdout") or ""),
            stderr=str(body.get("stderr") or ""),
            result=str(result) if result is not None else None,
            error=str(error) if error is not None else None,
            artifacts=tuple(names),
            session_id=session_id,
        )

    async def _post(
        self, path: str, payload: dict[str, object], bearer: str | None
    ) -> dict[str, Any]:
        url = f"{self._base_url}{path}"
        response = await self._http.post(
            url, json=payload, headers=self._headers(bearer), timeout=self._timeout
        )
        if response.status_code >= 400:
            raise RuntimeError(
                f"python_interpreter {path} {response.status_code}: {response.text[:240]}"
            )
        return cast(dict[str, Any], response.json())

    async def _get(self, path: str, bearer: str | None) -> dict[str, Any]:
        url = f"{self._base_url}{path}"
        response = await self._http.get(url, headers=self._headers(bearer), timeout=self._timeout)
        if response.status_code >= 400:
            raise RuntimeError(
                f"python_interpreter {path} {response.status_code}: {response.text[:240]}"
            )
        return cast(dict[str, Any], response.json())
