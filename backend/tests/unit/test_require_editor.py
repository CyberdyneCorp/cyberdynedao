"""Unit tests for the ``require_editor`` authoring guard.

The guard admits a human caller who either carries the ``editor`` scope
or is flagged as an admin by CyberdyneAuth. Service tokens are always
rejected. The admin path matters because the on-chain policy engine that
would grant the ``editor`` scope is currently disabled.
"""

from __future__ import annotations

from datetime import UTC, datetime
from uuid import uuid4

import pytest
from fastapi import HTTPException, Request

from cyberdyne_backend.adapters.inbound.middleware.auth import require_editor
from cyberdyne_backend.domain.auth_identity import ServicePrincipal, UserPrincipal

_EXPIRES = datetime(2999, 1, 1, tzinfo=UTC)


def _request_with(principal: object) -> Request:
    """A bare Request whose ``state.principal`` the middleware would set."""
    req = Request({"type": "http", "headers": []})
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


def test_editor_scope_is_admitted() -> None:
    principal = _user(scopes=frozenset({"editor"}))
    assert require_editor(_request_with(principal)) is principal


def test_admin_flag_is_admitted_without_editor_scope() -> None:
    principal = _user(is_admin=True)
    assert require_editor(_request_with(principal)) is principal


def test_plain_user_is_rejected() -> None:
    with pytest.raises(HTTPException) as exc:
        require_editor(_request_with(_user()))
    assert exc.value.status_code == 403


def test_service_token_is_rejected_even_with_editor_scope() -> None:
    service = ServicePrincipal(
        client_id="cyb_x",
        scopes=frozenset({"editor"}),
        audience=None,
        expires_at=_EXPIRES,
    )
    with pytest.raises(HTTPException) as exc:
        require_editor(_request_with(service))
    assert exc.value.status_code == 403


def test_missing_principal_is_unauthenticated() -> None:
    req = Request({"type": "http", "headers": []})
    req.state.principal = None
    with pytest.raises(HTTPException) as exc:
        require_editor(req)
    assert exc.value.status_code == 401
