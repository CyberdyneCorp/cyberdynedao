"""End-to-end tests for the code-interpreter endpoint (MATLAB-backed).

The MATLAB engine is external, so it's faked via a dependency override —
this verifies the route wiring, auth gate, request/response shapes, and
that the signed-in learner's id flows into the per-lesson session.
"""

from __future__ import annotations

import uuid
from collections.abc import AsyncIterator, Iterator
from datetime import UTC, datetime

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from cyberdyne_backend.adapters.inbound.api.code.router import get_run_code_uc
from cyberdyne_backend.adapters.inbound.middleware.auth import require_principal
from cyberdyne_backend.application.code import RunLessonCode
from cyberdyne_backend.domain.ai_chat import (
    CodeVariable,
    MatlabRunResult,
    PythonExecResult,
    RichOutput,
)
from cyberdyne_backend.domain.auth_identity import UserPrincipal

pytestmark = pytest.mark.integration

_LEARNER = UserPrincipal(
    user_id=uuid.UUID("99999999-9999-9999-9999-999999999999"),
    username="learner",
    scopes=frozenset(),
    audience=None,
    expires_at=datetime(2999, 1, 1, tzinfo=UTC),
)


class _FakeMatlab:
    async def run_repl(self, *, source, session_id, bearer):
        return MatlabRunResult(ok=True, stdout=f"ran: {source}", stderr="", session_id=session_id)

    async def run_plot(self, *, source, session_id, bearer, fmt="png"):
        return MatlabRunResult(ok=True, stdout="", stderr="", session_id=session_id)


@pytest.fixture
def code_client(app: FastAPI) -> Iterator[TestClient]:
    async def _uc() -> AsyncIterator[RunLessonCode]:
        yield RunLessonCode(matlab=_FakeMatlab())  # type: ignore[arg-type]

    app.dependency_overrides[get_run_code_uc] = _uc
    app.dependency_overrides[require_principal] = lambda: _LEARNER
    return TestClient(app)


def test_run_code(code_client: TestClient) -> None:
    lid = uuid.uuid4()
    resp = code_client.post(f"/api/v1/lessons/{lid}/code/run", json={"source": "2 + 2"})
    assert resp.status_code == 200, resp.text
    body = resp.json()
    assert body["ok"] is True
    assert body["stdout"] == "ran: 2 + 2"
    assert body["sessionId"] == f"lesson-{lid}-{_LEARNER.user_id}"


def test_empty_source_rejected(code_client: TestClient) -> None:
    resp = code_client.post(f"/api/v1/lessons/{uuid.uuid4()}/code/run", json={"source": ""})
    assert resp.status_code == 422


def test_requires_auth(client: TestClient) -> None:
    resp = client.post(f"/api/v1/lessons/{uuid.uuid4()}/code/run", json={"source": "1"})
    assert resp.status_code in (401, 403)


def test_matlab_run_returns_empty_variables_and_rich_outputs(
    code_client: TestClient,
) -> None:
    resp = code_client.post(
        f"/api/v1/lessons/{uuid.uuid4()}/code/run", json={"source": "x = 1"}
    )
    body = resp.json()
    # Additive fields present + backward compatible (empty for MATLAB).
    assert body["variables"] == []
    assert body["richOutputs"] == []


class _FakePython:
    async def create_session(self, *, bearer):
        return "srv-1"

    async def execute(self, *, code, session_id, bearer, restricted=True):
        return PythonExecResult(
            ok=True,
            stdout="done",
            stderr="",
            session_id=session_id,
            variables=(CodeVariable(name="x", type="int", repr="42", size_bytes=28),),
            rich_outputs=(RichOutput(mime_type="image/png", artifact="plot.png"),),
        )


def test_python_run_surfaces_variables_and_rich_outputs(app: FastAPI) -> None:
    async def _uc() -> AsyncIterator[RunLessonCode]:
        yield RunLessonCode(matlab=_FakeMatlab(), python=_FakePython())  # type: ignore[arg-type]

    app.dependency_overrides[get_run_code_uc] = _uc
    app.dependency_overrides[require_principal] = lambda: _LEARNER
    client = TestClient(app)

    resp = client.post(
        f"/api/v1/lessons/{uuid.uuid4()}/code/run",
        json={"source": "x = 42", "language": "python"},
    )
    assert resp.status_code == 200, resp.text
    body = resp.json()
    assert body["variables"] == [
        {"name": "x", "type": "int", "repr": "42", "sizeBytes": 28}
    ]
    assert body["richOutputs"] == [
        {"mimeType": "image/png", "artifact": "plot.png", "text": None}
    ]
