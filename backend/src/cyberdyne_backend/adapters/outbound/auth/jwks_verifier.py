"""Local RS256 access-token verification against CyberdyneAuth's JWKS.

CyberdyneAuth issues **RS256** access tokens and publishes its public
keys at ``/.well-known/jwks.json``. We verify tokens locally against
those keys — looked up by the token header's ``kid`` — instead of calling
the RFC 7662 introspection endpoint.

Why not introspection? After CyberdyneAuth's "fail closed on default/weak
secrets" hardening, ``POST /api/v1/auth/introspect`` requires the *caller*
(this backend) to authenticate. The old call sent only the token and so
started getting ``401 Not authenticated`` — which the DAO mis-reported as
``invalid token`` on every request, breaking all logins (issue #222).

Local JWKS verification needs no client credentials, removes a per-request
upstream round-trip, and is the standard way a resource server validates
access tokens. The key set is cached in-process and re-fetched on an
unknown ``kid`` (rate-limited), so upstream key rotation self-heals.
"""

from __future__ import annotations

import asyncio
import logging
import time

import httpx
import jwt

from cyberdyne_backend.domain.auth_identity import (
    AuthServiceUnavailableError,
    InvalidTokenError,
    Principal,
    principal_from_access_token,
)

logger = logging.getLogger("cyberdyne_backend.auth.jwks")

_RS256 = "RS256"


class JwksTokenVerifier:
    """Validates RS256 bearer tokens against CyberdyneAuth's JWKS.

    Implements the ``AuthPort`` protocol (``introspect`` keeps the name
    so the middleware and caching decorator are unchanged), but performs
    purely local signature/claim verification.
    """

    def __init__(
        self,
        base_url: str,
        http_client: httpx.AsyncClient,
        *,
        accepted_issuers: frozenset[str],
        jwks_path: str = "/.well-known/jwks.json",
        leeway_s: float = 60.0,
        jwks_min_refresh_s: float = 10.0,
        timeout_s: float = 5.0,
    ) -> None:
        self._jwks_url = f"{base_url.rstrip('/')}/{jwks_path.lstrip('/')}"
        self._http = http_client
        self._accepted_issuers = accepted_issuers
        self._leeway = leeway_s
        self._min_refresh = jwks_min_refresh_s
        self._timeout = timeout_s
        self._keys: dict[str, object] = {}
        self._last_refresh = 0.0
        self._lock = asyncio.Lock()

    async def introspect(self, token: str) -> Principal:
        if not token:
            raise InvalidTokenError("empty bearer token")

        try:
            header = jwt.get_unverified_header(token)
        except jwt.PyJWTError as exc:
            raise InvalidTokenError(f"malformed token header: {exc}") from exc
        if header.get("alg") != _RS256:
            raise InvalidTokenError(f"unsupported token alg {header.get('alg')!r}")

        key = await self._resolve_key(header.get("kid"))
        claims = self._decode(token, key)

        iss = claims.get("iss")
        if self._accepted_issuers and iss not in self._accepted_issuers:
            raise InvalidTokenError(f"untrusted issuer {iss!r}")

        principal = principal_from_access_token(claims)
        if principal is None:
            raise InvalidTokenError("token claims do not identify a principal")
        return principal

    def _decode(self, token: str, key: object) -> dict[str, object]:
        try:
            return jwt.decode(
                token,
                key,  # type: ignore[arg-type]
                algorithms=[_RS256],
                leeway=self._leeway,
                # CyberdyneAuth sets no ``aud`` on access tokens; don't
                # require one. ``iss`` is validated explicitly below
                # against the accepted set (which tolerates two values).
                options={"verify_aud": False, "require": ["exp"]},
            )
        except jwt.ExpiredSignatureError as exc:
            raise InvalidTokenError("token expired") from exc
        except jwt.PyJWTError as exc:
            raise InvalidTokenError(f"token verification failed: {exc}") from exc

    async def _resolve_key(self, kid: str | None) -> object:
        """Return the signing key for ``kid``, refreshing the JWKS once
        (rate-limited) if the key isn't already cached. Tolerates a
        missing ``kid`` only when the key set holds exactly one key."""
        async with self._lock:
            key = self._lookup(kid)
            if key is not None:
                return key

            now = time.monotonic()
            too_soon = self._keys and (now - self._last_refresh) < self._min_refresh
            if too_soon:
                raise InvalidTokenError(f"unknown signing key kid={kid!r}")

            await self._refresh()
            key = self._lookup(kid)
            if key is None:
                raise InvalidTokenError(f"unknown signing key kid={kid!r}")
            return key

    def _lookup(self, kid: str | None) -> object | None:
        if kid is not None:
            return self._keys.get(kid)
        # No kid in the header: only safe when the set is unambiguous.
        if len(self._keys) == 1:
            return next(iter(self._keys.values()))
        return None

    async def _refresh(self) -> None:
        """Fetch + cache the JWKS. Raises ``AuthServiceUnavailableError``
        when we can't reach it and have no usable cached key to fall back
        on; otherwise keeps the stale cache and lets the caller decide."""
        try:
            response = await self._http.get(self._jwks_url, timeout=self._timeout)
        except httpx.HTTPError as exc:
            self._fail_or_keep_cache(f"transport error fetching JWKS: {exc}", exc)
            return
        if response.status_code != 200:
            self._fail_or_keep_cache(
                f"JWKS endpoint returned {response.status_code}", None
            )
            return

        try:
            jwk_set = jwt.PyJWKSet.from_dict(response.json())
        except (ValueError, jwt.PyJWKError) as exc:
            self._fail_or_keep_cache(f"malformed JWKS document: {exc}", exc)
            return

        keys: dict[str, object] = {}
        for jwk in jwk_set.keys:
            if jwk.key_id:
                keys[jwk.key_id] = jwk.key
        self._keys = keys
        self._last_refresh = time.monotonic()
        logger.info("refreshed JWKS: %d key(s)", len(keys))

    def _fail_or_keep_cache(self, message: str, cause: Exception | None) -> None:
        if self._keys:
            logger.warning("%s; keeping cached keys", message)
            return
        raise AuthServiceUnavailableError(message) from cause
