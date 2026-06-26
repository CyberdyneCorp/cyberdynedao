"""Pro-entitlement parsing on the principal (issue #230)."""

from __future__ import annotations

import pytest

from cyberdyne_backend.domain.auth_identity import UserPrincipal, has_pro_entitlement
from cyberdyne_backend.domain.auth_identity.entities import (
    principal_from_access_token,
    principal_from_introspection,
)

pytestmark = pytest.mark.unit

_EXP = 4102444800  # 2100-01-01, comfortably in the future


def test_has_pro_entitlement_variants() -> None:
    assert has_pro_entitlement(frozenset({"pro"}))
    assert has_pro_entitlement(frozenset({"pro:annual"}))
    assert has_pro_entitlement(frozenset({"foo", "pro:monthly"}))
    assert not has_pro_entitlement(frozenset())
    assert not has_pro_entitlement(frozenset({"propro", "basic"}))


def test_introspection_parses_entitlements_array() -> None:
    principal = principal_from_introspection(
        {
            "active": True,
            "exp": _EXP,
            "sub": "11111111-1111-1111-1111-111111111111",
            "username": "leo",
            "entitlements": ["pro:annual"],
        }
    )
    assert isinstance(principal, UserPrincipal)
    assert principal.is_pro is True
    assert principal.entitlements == frozenset({"pro:annual"})


def test_access_token_without_entitlements_is_not_pro() -> None:
    principal = principal_from_access_token(
        {
            "exp": _EXP,
            "sub": "11111111-1111-1111-1111-111111111111",
            "username": "leo",
        }
    )
    assert isinstance(principal, UserPrincipal)
    assert principal.is_pro is False
    assert principal.entitlements == frozenset()
