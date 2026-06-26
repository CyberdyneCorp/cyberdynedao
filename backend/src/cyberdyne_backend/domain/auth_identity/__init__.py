"""Auth identity bounded context.

Two kinds of authenticated callers — humans (``UserPrincipal``) and
services (``ServicePrincipal``) — backed by the same RFC 7662
introspection. CyberdyneAuth v0.1.0 distinguishes them via the
``client_id`` vs ``username`` claim on the introspection response.
"""

from cyberdyne_backend.domain.auth_identity.entities import (
    Principal,
    ServicePrincipal,
    UserPrincipal,
    UserProfile,
    has_pro_entitlement,
    principal_from_access_token,
    profile_from_users_me,
)
from cyberdyne_backend.domain.auth_identity.ports import (
    AuthError,
    AuthPort,
    AuthServiceUnavailableError,
    InvalidTokenError,
    UserProfilePort,
)

__all__ = [
    "AuthError",
    "AuthPort",
    "AuthServiceUnavailableError",
    "InvalidTokenError",
    "Principal",
    "ServicePrincipal",
    "UserPrincipal",
    "UserProfile",
    "UserProfilePort",
    "has_pro_entitlement",
    "principal_from_access_token",
    "profile_from_users_me",
]
