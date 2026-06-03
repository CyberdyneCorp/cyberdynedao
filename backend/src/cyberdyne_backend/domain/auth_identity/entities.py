"""Principal value objects.

Built from CyberdyneAuth's RFC 7662 ``IntrospectionResponse``. The
discriminator is ``client_id`` vs ``username`` per the upstream spec
(`docs/backend-roadmap.md` §4 and §5.1).

Both kinds carry ``scopes``, ``audience``, and ``expires_at``; full
profile data (user email, organization, client name, allowed audiences)
is lazy-loaded by their respective profile lookups (`/users/me` or
`/clients/me`) only when a route actually needs it.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, datetime
from typing import Any
from uuid import UUID


@dataclass(frozen=True, slots=True)
class UserPrincipal:
    user_id: UUID
    username: str | None
    scopes: frozenset[str]
    audience: str | None
    expires_at: datetime
    is_admin: bool = False

    @property
    def kind(self) -> str:
        return "user"


@dataclass(frozen=True, slots=True)
class ServicePrincipal:
    client_id: str
    scopes: frozenset[str]
    audience: str | None
    expires_at: datetime

    @property
    def kind(self) -> str:
        return "service"


Principal = UserPrincipal | ServicePrincipal


@dataclass(frozen=True, slots=True)
class UserProfile:
    """Full user profile from CyberdyneAuth's ``/users/me``.

    Distinct from ``UserPrincipal`` (which is just the introspected
    token claims): this is the richer record a route fetches when it
    actually needs contact details — e.g. the chat agent personalizing
    a reply or pre-filling a lead. CyberdyneAuth has no display-name
    field, so ``email`` (or its local part via ``display_name``) is the
    closest human-readable handle.
    """

    user_id: UUID
    email: str | None
    wallet_address: str | None = None
    organization_id: str | None = None
    is_email_verified: bool = False
    is_admin: bool = False

    @property
    def display_name(self) -> str | None:
        if self.email:
            return self.email.split("@", 1)[0]
        if self.wallet_address:
            return f"{self.wallet_address[:6]}…{self.wallet_address[-4:]}"
        return None


# CyberdyneAuth marks privileged users with a boolean flag rather than a
# scope. The key has drifted across versions, so we accept the first of
# these that is present and truthy. With the on-chain policy engine (which
# would otherwise grant the ``editor`` scope) disabled, this flag is the
# only signal that lets an admin through the authoring guard.
_ADMIN_FLAG_KEYS = ("is_superuser", "is_admin", "is_staff")


def _parse_admin_flag(payload: dict[str, Any]) -> bool:
    return any(bool(payload.get(key)) for key in _ADMIN_FLAG_KEYS)


def profile_from_users_me(payload: dict[str, Any]) -> UserProfile | None:
    """Map CyberdyneAuth's ``GET /users/me`` body to a ``UserProfile``.

    Returns ``None`` when the payload lacks a usable ``id`` — callers
    treat that as "no profile available" and degrade to anonymous.
    """
    raw_id = payload.get("id")
    if not isinstance(raw_id, str):
        return None
    try:
        user_id = UUID(raw_id)
    except ValueError:
        return None
    email = payload.get("email")
    wallet = payload.get("wallet_address")
    org = payload.get("organization_id")
    return UserProfile(
        user_id=user_id,
        email=email if isinstance(email, str) else None,
        wallet_address=wallet if isinstance(wallet, str) else None,
        organization_id=org if isinstance(org, str) else None,
        is_email_verified=bool(payload.get("is_email_verified", False)),
        is_admin=_parse_admin_flag(payload),
    )


def _parse_scopes(raw: str | None) -> frozenset[str]:
    if not raw:
        return frozenset()
    return frozenset(s for s in raw.split() if s)


def principal_from_introspection(payload: dict[str, Any]) -> Principal | None:
    """Map an RFC 7662 ``IntrospectionResponse`` to a domain principal.

    Returns ``None`` when ``active`` is false or the payload doesn't
    carry enough to identify either a user or a client. Callers turn
    ``None`` into 401.
    """
    if not payload.get("active"):
        return None

    exp = payload.get("exp")
    if not isinstance(exp, int):
        return None
    expires_at = datetime.fromtimestamp(exp, tz=UTC)

    scopes = _parse_scopes(payload.get("scope"))
    audience = payload.get("aud") if isinstance(payload.get("aud"), str) else None

    client_id = payload.get("client_id")
    sub = payload.get("sub")
    username = payload.get("username")

    if isinstance(client_id, str) and client_id and not username:
        return ServicePrincipal(
            client_id=client_id,
            scopes=scopes,
            audience=audience,
            expires_at=expires_at,
        )

    raw_user_id = sub if isinstance(sub, str) else None
    if raw_user_id is None:
        return None
    try:
        user_id = UUID(raw_user_id)
    except ValueError:
        return None
    return UserPrincipal(
        user_id=user_id,
        username=username if isinstance(username, str) else None,
        scopes=scopes,
        audience=audience,
        expires_at=expires_at,
        is_admin=_parse_admin_flag(payload),
    )
