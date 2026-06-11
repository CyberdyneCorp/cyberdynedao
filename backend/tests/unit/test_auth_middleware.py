"""AuthMiddleware + require_principal behaviour, driven by a FakeAuthPort.

Covers the request-path outcomes the integration suite bypasses (it
overrides the guards): valid token => 200, missing => 401, invalid => 401,
upstream unavailable => 503. Pure in-process (no real HTTP / DB), so it runs
under the default ``unit`` selection.
"""

from __future__ import annotations

import uuid
from datetime import UTC, datetime, timedelta
from typing import Annotated

import pytest
from fastapi import Depends, FastAPI
from fastapi.testclient import TestClient

from cyberdyne_backend.adapters.inbound.middleware.auth import (
    AuthMiddleware,
    require_principal,
)
from cyberdyne_backend.domain.auth_identity import (
    AuthServiceUnavailableError,
    InvalidTokenError,
    Principal,
    UserPrincipal,
)


class FakeAuthPort:
    """Stand-in AuthPort: returns a fixed principal or raises a fixed error."""

    def __init__(
        self,
        *,
        principal: Principal | None = None,
        error: Exception | None = None,
    ) -> None:
        self._principal = principal
        self._error = error
        self.calls = 0

    async def introspect(self, token: str) -> Principal:
        self.calls += 1
        if self._error is not None:
            raise self._error
        assert self._principal is not None
        return self._principal


def _user() -> UserPrincipal:
    return UserPrincipal(
        user_id=uuid.uuid4(),
        username="alice",
        scopes=frozenset(),
        audience=None,
        expires_at=datetime.now(UTC) + timedelta(minutes=5),
    )


def _app(port: FakeAuthPort) -> TestClient:
    app = FastAPI()
    app.add_middleware(AuthMiddleware, auth_port=port)

    @app.get("/guarded")
    def guarded(principal: Annotated[Principal, Depends(require_principal)]) -> dict[str, str]:
        return {"ok": "yes"}

    return TestClient(app, raise_server_exceptions=False)


def test_valid_token_passes() -> None:
    port = FakeAuthPort(principal=_user())
    client = _app(port)
    resp = client.get("/guarded", headers={"Authorization": "Bearer good"})
    assert resp.status_code == 200
    assert port.calls == 1


def test_missing_token_is_401_without_calling_upstream() -> None:
    port = FakeAuthPort(principal=_user())
    client = _app(port)
    resp = client.get("/guarded")
    assert resp.status_code == 401
    assert port.calls == 0


def test_cookie_token_is_accepted() -> None:
    port = FakeAuthPort(principal=_user())
    client = _app(port)
    client.cookies.set("access_token", "good")
    resp = client.get("/guarded")
    assert resp.status_code == 200
    assert port.calls == 1


def test_invalid_token_is_401() -> None:
    port = FakeAuthPort(error=InvalidTokenError("nope"))
    client = _app(port)
    resp = client.get("/guarded", headers={"Authorization": "Bearer bad"})
    assert resp.status_code == 401


def test_upstream_unavailable_is_503() -> None:
    port = FakeAuthPort(error=AuthServiceUnavailableError("down"))
    client = _app(port)
    resp = client.get("/guarded", headers={"Authorization": "Bearer x"})
    assert resp.status_code == 503


@pytest.mark.parametrize("scheme", ["Token", "bearer", "Basic"])
def test_non_bearer_authorization_is_treated_as_missing(scheme: str) -> None:
    port = FakeAuthPort(principal=_user())
    client = _app(port)
    resp = client.get("/guarded", headers={"Authorization": f"{scheme} good"})
    assert resp.status_code == 401
    assert port.calls == 0
