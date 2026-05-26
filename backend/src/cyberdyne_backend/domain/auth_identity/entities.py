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
    )
