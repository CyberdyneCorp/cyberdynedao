"""Regression: draft visibility must mirror ``require_editor``.

An admin (CyberdyneAuth ``is_admin``, no ``editor`` scope) can author
courses, so they must also see the drafts they author. Before the fix,
``_viewer_can_see_drafts`` checked only the ``editor`` scope, so an admin
could create a draft (201) but the catalogue never showed it.
"""

from __future__ import annotations

from datetime import UTC, datetime
from uuid import uuid4

from fastapi import Request

from cyberdyne_backend.adapters.inbound.api.courses.router import _viewer_can_see_drafts
from cyberdyne_backend.domain.auth_identity import ServicePrincipal, UserPrincipal

_EXPIRES = datetime(2999, 1, 1, tzinfo=UTC)


def _request_with(principal: object) -> Request:
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


def test_editor_scope_sees_drafts() -> None:
    assert _viewer_can_see_drafts(_request_with(_user(scopes=frozenset({"editor"})))) is True


def test_admin_flag_sees_drafts() -> None:
    assert _viewer_can_see_drafts(_request_with(_user(is_admin=True))) is True


def test_plain_user_does_not_see_drafts() -> None:
    assert _viewer_can_see_drafts(_request_with(_user())) is False


def test_anonymous_does_not_see_drafts() -> None:
    assert _viewer_can_see_drafts(_request_with(None)) is False


def test_service_principal_does_not_see_drafts() -> None:
    service = ServicePrincipal(
        client_id="cyb_x",
        scopes=frozenset({"editor"}),
        audience=None,
        expires_at=_EXPIRES,
    )
    assert _viewer_can_see_drafts(_request_with(service)) is False
