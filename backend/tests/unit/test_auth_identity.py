"""Tests for the auth_identity domain.

Specifically ``principal_from_introspection`` — the pure function that
maps a CyberdyneAuth ``IntrospectionResponse`` to a domain principal.
This is the hot path of the auth middleware so every branch is worth
covering.
"""

from __future__ import annotations

from datetime import UTC, datetime
from uuid import UUID

import pytest

from cyberdyne_backend.domain.auth_identity import (
    Principal,
    ServicePrincipal,
    UserPrincipal,
)
from cyberdyne_backend.domain.auth_identity.entities import (
    _parse_scopes,
    principal_from_introspection,
)

USER_ID = "550e8400-e29b-41d4-a716-446655440000"


def _base_introspect(**overrides: object) -> dict[str, object]:
    """An introspection payload skeleton that test cases extend."""
    payload: dict[str, object] = {
        "active": True,
        "sub": USER_ID,
        "username": "alice",
        "scope": "content:read",
        "aud": "https://api.coolify.cyberdynecorp.ai",
        "exp": 4102444800,  # 2100-01-01
        "iat": 4102441200,
        "token_type": "Bearer",
    }
    payload.update(overrides)
    return payload


# ── _parse_scopes ────────────────────────────────────────────────────


class TestParseScopes:
    def test_none_returns_empty(self) -> None:
        assert _parse_scopes(None) == frozenset()

    def test_empty_string_returns_empty(self) -> None:
        assert _parse_scopes("") == frozenset()

    def test_whitespace_only_returns_empty(self) -> None:
        assert _parse_scopes("   ") == frozenset()

    def test_single_scope(self) -> None:
        assert _parse_scopes("content:read") == frozenset({"content:read"})

    def test_space_separated_scopes(self) -> None:
        assert _parse_scopes("a:b c:d e:f") == frozenset({"a:b", "c:d", "e:f"})

    def test_duplicates_collapse(self) -> None:
        assert _parse_scopes("a b a b") == frozenset({"a", "b"})


# ── principal_from_introspection — user tokens ───────────────────────


class TestUserPrincipalParsing:
    def test_valid_user_token_maps_to_user_principal(self) -> None:
        principal = principal_from_introspection(_base_introspect())
        assert isinstance(principal, UserPrincipal)
        assert principal.user_id == UUID(USER_ID)
        assert principal.username == "alice"
        assert principal.scopes == frozenset({"content:read"})
        assert principal.audience == "https://api.coolify.cyberdynecorp.ai"
        assert principal.expires_at == datetime.fromtimestamp(4102444800, tz=UTC)
        assert principal.kind == "user"

    def test_username_missing_is_allowed(self) -> None:
        principal = principal_from_introspection(_base_introspect(username=None))
        assert isinstance(principal, UserPrincipal)
        assert principal.username is None

    def test_audience_missing(self) -> None:
        principal = principal_from_introspection(_base_introspect(aud=None))
        assert isinstance(principal, UserPrincipal)
        assert principal.audience is None

    def test_scope_missing(self) -> None:
        principal = principal_from_introspection(_base_introspect(scope=None))
        assert isinstance(principal, UserPrincipal)
        assert principal.scopes == frozenset()

    def test_sub_not_a_uuid_returns_none(self) -> None:
        principal = principal_from_introspection(_base_introspect(sub="not-a-uuid"))
        assert principal is None

    def test_sub_missing_returns_none(self) -> None:
        payload = _base_introspect()
        del payload["sub"]
        assert principal_from_introspection(payload) is None

    def test_sub_not_a_string_returns_none(self) -> None:
        principal = principal_from_introspection(_base_introspect(sub=12345))
        assert principal is None

    def test_audience_non_string_falls_back_to_none(self) -> None:
        # Some introspect implementations return aud as a list; v0.1.0
        # advertises a string, so anything else collapses to None.
        principal = principal_from_introspection(_base_introspect(aud=["a", "b"]))
        assert isinstance(principal, UserPrincipal)
        assert principal.audience is None

    def test_default_is_not_admin(self) -> None:
        principal = principal_from_introspection(_base_introspect())
        assert isinstance(principal, UserPrincipal)
        assert principal.is_admin is False

    @pytest.mark.parametrize("flag_key", ["is_superuser", "is_admin", "is_staff"])
    def test_admin_flag_sets_is_admin(self, flag_key: str) -> None:
        principal = principal_from_introspection(_base_introspect(**{flag_key: True}))
        assert isinstance(principal, UserPrincipal)
        assert principal.is_admin is True

    def test_falsy_admin_flag_stays_non_admin(self) -> None:
        principal = principal_from_introspection(_base_introspect(is_superuser=False))
        assert isinstance(principal, UserPrincipal)
        assert principal.is_admin is False


# ── principal_from_introspection — service tokens ────────────────────


class TestServicePrincipalParsing:
    def test_client_id_without_username_maps_to_service_principal(self) -> None:
        payload = _base_introspect(
            sub="client:cyb_chat_xxxxxxxx",
            client_id="cyb_chat_xxxxxxxx",
            username=None,
            scope="cyberrag:query iam:read.tier",
        )
        principal = principal_from_introspection(payload)
        assert isinstance(principal, ServicePrincipal)
        assert principal.client_id == "cyb_chat_xxxxxxxx"
        assert principal.scopes == frozenset({"cyberrag:query", "iam:read.tier"})
        assert principal.kind == "service"

    def test_client_id_with_username_is_treated_as_user(self) -> None:
        # Discriminator per §5.1: client_id without username = service.
        # If username is also set we treat it as a user token to avoid
        # mis-classifying impersonation flows.
        payload = _base_introspect(
            client_id="some_client",
            username="alice",
        )
        principal = principal_from_introspection(payload)
        assert isinstance(principal, UserPrincipal)


# ── principal_from_introspection — rejection paths ───────────────────


class TestRejection:
    def test_active_false_returns_none(self) -> None:
        principal = principal_from_introspection(_base_introspect(active=False))
        assert principal is None

    def test_active_missing_returns_none(self) -> None:
        payload = _base_introspect()
        del payload["active"]
        assert principal_from_introspection(payload) is None

    def test_exp_missing_returns_none(self) -> None:
        payload = _base_introspect()
        del payload["exp"]
        assert principal_from_introspection(payload) is None

    def test_exp_not_an_int_returns_none(self) -> None:
        principal = principal_from_introspection(_base_introspect(exp="never"))
        assert principal is None


# ── Principal union convenience ──────────────────────────────────────


@pytest.mark.parametrize(
    "principal,expected_kind",
    [
        (
            UserPrincipal(
                user_id=UUID(USER_ID),
                username="a",
                scopes=frozenset(),
                audience=None,
                expires_at=datetime.fromtimestamp(4102444800, tz=UTC),
            ),
            "user",
        ),
        (
            ServicePrincipal(
                client_id="c",
                scopes=frozenset(),
                audience=None,
                expires_at=datetime.fromtimestamp(4102444800, tz=UTC),
            ),
            "service",
        ),
    ],
)
def test_principal_kinds(principal: Principal, expected_kind: str) -> None:
    assert principal.kind == expected_kind
