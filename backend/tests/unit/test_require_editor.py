"""Unit tests for the ``require_editor`` authoring guard.

The guard admits a human caller who carries the ``editor`` scope, is
flagged as an admin by introspection, or is flagged as an admin on their
``/users/me`` profile (best-effort fallback). Service tokens are always
rejected. The admin paths matter because the on-chain policy engine that
would grant the ``editor`` scope is currently disabled.
"""

from __future__ import annotations

from datetime import UTC, datetime
from uuid import uuid4

import pytest
from fastapi import HTTPException, Request

from cyberdyne_backend.adapters.inbound.middleware.auth import require_editor
from cyberdyne_backend.domain.auth_identity import (
    ServicePrincipal,
    UserPrincipal,
    UserProfile,
)

_EXPIRES = datetime(2999, 1, 1, tzinfo=UTC)


def _request_with(principal: object, *, token: str | None = None) -> Request:
    """A bare Request whose ``state.principal`` the middleware would set.

    Pass ``token`` to make ``extract_token`` resolve a bearer — needed to
    exercise the /users/me profile fallback.
    """
    headers = [(b"authorization", f"Bearer {token}".encode())] if token else []
    req = Request({"type": "http", "headers": headers})
    req.state.principal = principal
    return req


def _user(*, scopes: frozenset[str] = frozenset(), is_admin: bool = False) -> UserPrincipal:
    return UserPrincipal(
        user_id=uuid4(),
        username="u",
        scopes=scopes,
        audience=None,
        expires_at=_EXPIRES,
        is_admin=is_admin,
    )


class _FakeProfilePort:
    """Records calls and returns a preset profile (or None)."""

    def __init__(self, profile: UserProfile | None) -> None:
        self._profile = profile
        self.calls = 0

    async def get_profile(self, token: str) -> UserProfile | None:
        self.calls += 1
        return self._profile


def _profile(*, is_admin: bool) -> UserProfile:
    return UserProfile(user_id=uuid4(), email="a@b.c", is_admin=is_admin)


async def test_editor_scope_is_admitted() -> None:
    principal = _user(scopes=frozenset({"editor"}))
    assert await require_editor(_request_with(principal)) is principal


async def test_introspection_admin_flag_is_admitted() -> None:
    principal = _user(is_admin=True)
    assert await require_editor(_request_with(principal)) is principal


async def test_admin_paths_skip_the_profile_lookup() -> None:
    # An editor/admin already qualifies, so the /users/me port is untouched.
    port = _FakeProfilePort(_profile(is_admin=True))
    principal = _user(scopes=frozenset({"editor"}))
    assert await require_editor(_request_with(principal), port) is principal
    assert port.calls == 0


async def test_profile_admin_flag_is_admitted_as_fallback() -> None:
    # Introspection carries neither editor scope nor admin flag, but
    # /users/me marks the user as an admin.
    port = _FakeProfilePort(_profile(is_admin=True))
    principal = _user()
    result = await require_editor(_request_with(principal, token="tok"), port)
    assert result is principal
    assert port.calls == 1


async def test_non_admin_profile_is_rejected() -> None:
    port = _FakeProfilePort(_profile(is_admin=False))
    with pytest.raises(HTTPException) as exc:
        await require_editor(_request_with(_user(), token="tok"), port)
    assert exc.value.status_code == 403


async def test_missing_profile_is_rejected() -> None:
    port = _FakeProfilePort(None)
    with pytest.raises(HTTPException) as exc:
        await require_editor(_request_with(_user(), token="tok"), port)
    assert exc.value.status_code == 403


async def test_plain_user_without_profile_port_is_rejected() -> None:
    with pytest.raises(HTTPException) as exc:
        await require_editor(_request_with(_user()))
    assert exc.value.status_code == 403


async def test_service_token_is_rejected_even_with_editor_scope() -> None:
    service = ServicePrincipal(
        client_id="cyb_x",
        scopes=frozenset({"editor"}),
        audience=None,
        expires_at=_EXPIRES,
    )
    with pytest.raises(HTTPException) as exc:
        await require_editor(_request_with(service))
    assert exc.value.status_code == 403


async def test_missing_principal_is_unauthenticated() -> None:
    req = Request({"type": "http", "headers": []})
    req.state.principal = None
    with pytest.raises(HTTPException) as exc:
        await require_editor(req)
    assert exc.value.status_code == 401
