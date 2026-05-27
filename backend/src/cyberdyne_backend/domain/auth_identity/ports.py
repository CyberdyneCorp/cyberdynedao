"""Ports the auth_identity context depends on.

Concrete impls live in ``adapters/outbound/auth/``. A FakeAuthPort
lives in ``tests/fakes/auth.py`` for unit tests.
"""

from __future__ import annotations

from typing import Protocol, runtime_checkable

from cyberdyne_backend.domain.auth_identity.entities import Principal, UserProfile


class AuthError(Exception):
    """Base — caller turns this into either 401 or 503."""


class InvalidTokenError(AuthError):
    """Token is missing, malformed, expired, or rejected upstream. 401."""


class AuthServiceUnavailableError(AuthError):
    """Upstream CyberdyneAuth is unreachable / 5xx / timing out. 503."""


@runtime_checkable
class AuthPort(Protocol):
    async def introspect(self, token: str) -> Principal:
        """Validate ``token`` and return the resolved principal.

        Raises ``InvalidTokenError`` for 401-class outcomes (also when
        ``active`` is false on the introspection response) and
        ``AuthServiceUnavailableError`` for transport / 5xx outcomes.
        """
        ...


@runtime_checkable
class UserProfilePort(Protocol):
    async def get_profile(self, token: str) -> UserProfile | None:
        """Fetch the full user profile for the bearer ``token``.

        Returns ``None`` when the token doesn't resolve to a user
        profile (e.g. a service token, or the upstream is unreachable);
        callers degrade to anonymous rather than failing the request.
        Implementations should never raise — a profile lookup is always
        best-effort enrichment, not an auth gate.
        """
        ...
