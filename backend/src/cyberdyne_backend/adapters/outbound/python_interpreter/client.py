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

import logging
from typing import Any, cast

import httpx

from cyberdyne_backend.domain.ai_chat import PythonExecResult

logger = logging.getLogger("cyberdyne_backend.python_interpreter")


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
    def _to_result(body: dict[str, Any], session_id: str) -> PythonExecResult:
        # Upstream artifacts are FileMeta objects ({name, size_bytes,
        # modified_at}); keep just the names, like the MATLAB client.
        raw_artifacts = body.get("artifacts")
        names: list[str] = []
        if isinstance(raw_artifacts, list):
            for a in raw_artifacts:
                if isinstance(a, dict) and isinstance(a.get("name"), str):
                    names.append(a["name"])
                elif isinstance(a, str):
                    names.append(a)
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
