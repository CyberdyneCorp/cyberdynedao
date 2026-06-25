"""Tests for the local RS256 JWKS access-token verifier.

Regression coverage for issue #222: after CyberdyneAuth started signing
access tokens with RS256 and locked introspection behind caller auth, the
DAO must verify tokens locally against the JWKS. These tests sign tokens
with a throwaway RSA keypair and serve the matching JWKS over a mocked
transport — no network.
"""

from __future__ import annotations

import json
import time
import uuid

import httpx
import jwt
import pytest
from cryptography.hazmat.primitives.asymmetric import rsa

from cyberdyne_backend.adapters.outbound.auth.jwks_verifier import JwksTokenVerifier
from cyberdyne_backend.domain.auth_identity import (
    AuthServiceUnavailableError,
    InvalidTokenError,
    ServicePrincipal,
    UserPrincipal,
)

ISSUER = "cyberdyne-auth"
ACCEPTED = frozenset({ISSUER, "https://auth.example"})
KID = "test-key-1"
JWKS_URL = "https://auth.example/.well-known/jwks.json"


def _keypair() -> rsa.RSAPrivateKey:
    return rsa.generate_private_key(public_exponent=65537, key_size=2048)


def _jwk(private_key: rsa.RSAPrivateKey, kid: str = KID) -> dict[str, object]:
    pub_pem = private_key.public_key()
    jwk = json.loads(jwt.algorithms.RSAAlgorithm.to_jwk(pub_pem))
    jwk.update({"kid": kid, "use": "sig", "alg": "RS256"})
    return jwk


def _sign(
    private_key: rsa.RSAPrivateKey,
    *,
    kid: str | None = KID,
    **claims: object,
) -> str:
    payload: dict[str, object] = {
        "iss": ISSUER,
        "type": "access",
        "sub": str(uuid.uuid4()),
        "scope": "content:read",
        "exp": int(time.time()) + 3600,
        "iat": int(time.time()),
    }
    payload.update(claims)
    headers = {"kid": kid} if kid is not None else None
    return jwt.encode(payload, private_key, algorithm="RS256", headers=headers)


def _verifier(
    jwks: list[dict[str, object]],
    *,
    fail: bool = False,
    status: int = 200,
) -> tuple[JwksTokenVerifier, dict[str, int]]:
    counter = {"fetches": 0}

    def handler(request: httpx.Request) -> httpx.Response:
        counter["fetches"] += 1
        if fail:
            raise httpx.ConnectError("boom", request=request)
        if status != 200:
            return httpx.Response(status, json={"detail": "nope"})
        return httpx.Response(200, json={"keys": jwks})

    http = httpx.AsyncClient(transport=httpx.MockTransport(handler))
    verifier = JwksTokenVerifier(
        base_url="https://auth.example",
        http_client=http,
        accepted_issuers=ACCEPTED,
        jwks_min_refresh_s=0.0,
    )
    return verifier, counter


class TestHappyPath:
    async def test_valid_user_token_resolves_user_principal(self) -> None:
        key = _keypair()
        uid = str(uuid.uuid4())
        verifier, counter = _verifier([_jwk(key)])
        principal = await verifier.introspect(_sign(key, sub=uid))
        assert isinstance(principal, UserPrincipal)
        assert str(principal.user_id) == uid
        assert principal.scopes == frozenset({"content:read"})
        assert counter["fetches"] == 1

    async def test_keys_are_cached_across_calls(self) -> None:
        key = _keypair()
        verifier, counter = _verifier([_jwk(key)])
        await verifier.introspect(_sign(key))
        await verifier.introspect(_sign(key))
        assert counter["fetches"] == 1

    async def test_service_token_resolves_service_principal(self) -> None:
        key = _keypair()
        verifier, _ = _verifier([_jwk(key)])
        token = _sign(key, type="service", sub="cyb_chat_x", client_id="cyb_chat_x")
        principal = await verifier.introspect(token)
        assert isinstance(principal, ServicePrincipal)
        assert principal.client_id == "cyb_chat_x"

    async def test_issuer_url_form_is_accepted(self) -> None:
        key = _keypair()
        verifier, _ = _verifier([_jwk(key)])
        principal = await verifier.introspect(_sign(key, iss="https://auth.example"))
        assert isinstance(principal, UserPrincipal)


class TestRejection:
    async def test_empty_token(self) -> None:
        verifier, _ = _verifier([])
        with pytest.raises(InvalidTokenError):
            await verifier.introspect("")

    async def test_garbage_token(self) -> None:
        verifier, _ = _verifier([])
        with pytest.raises(InvalidTokenError):
            await verifier.introspect("not.a.jwt")

    async def test_expired_token(self) -> None:
        key = _keypair()
        verifier, _ = _verifier([_jwk(key)])
        # Beyond the default 60s clock-skew leeway.
        with pytest.raises(InvalidTokenError):
            await verifier.introspect(_sign(key, exp=int(time.time()) - 600))

    async def test_untrusted_issuer(self) -> None:
        key = _keypair()
        verifier, _ = _verifier([_jwk(key)])
        with pytest.raises(InvalidTokenError):
            await verifier.introspect(_sign(key, iss="evil"))

    async def test_signature_from_unknown_key(self) -> None:
        signing_key = _keypair()
        published_key = _keypair()  # different key in the JWKS
        verifier, _ = _verifier([_jwk(published_key)])
        with pytest.raises(InvalidTokenError):
            await verifier.introspect(_sign(signing_key))

    async def test_hs256_token_is_rejected(self) -> None:
        key = _keypair()
        verifier, _ = _verifier([_jwk(key)])
        forged = jwt.encode(
            {"sub": "x", "exp": int(time.time()) + 60},
            "x" * 32,  # 32-byte HMAC key — only the alg matters to the test
            algorithm="HS256",
        )
        with pytest.raises(InvalidTokenError):
            await verifier.introspect(forged)


class TestKeyRotation:
    async def test_unknown_kid_triggers_one_refresh(self) -> None:
        old = _keypair()
        new = _keypair()
        # Verifier starts serving only the old key, then we rotate.
        verifier, counter = _verifier([_jwk(old)])
        await verifier.introspect(_sign(old))
        assert counter["fetches"] == 1

        # Rotate the served JWKS to a new kid and sign with the new key.
        verifier._http = httpx.AsyncClient(  # swap transport to serve new keys
            transport=httpx.MockTransport(
                lambda req: httpx.Response(200, json={"keys": [_jwk(new, kid="kid-2")]})
            )
        )
        principal = await verifier.introspect(_sign(new, kid="kid-2"))
        assert isinstance(principal, UserPrincipal)

    async def test_refresh_rate_limited_for_unknown_kid(self) -> None:
        key = _keypair()
        verifier, counter = _verifier([_jwk(key)])
        verifier._min_refresh = 999.0  # block re-fetch
        await verifier.introspect(_sign(key))  # one fetch, caches key
        assert counter["fetches"] == 1
        with pytest.raises(InvalidTokenError):
            await verifier.introspect(_sign(key, kid="unknown-kid"))
        # No second fetch — rate-limited because we already have keys.
        assert counter["fetches"] == 1


class TestUpstreamUnavailable:
    async def test_jwks_unreachable_with_no_cache_is_503(self) -> None:
        key = _keypair()
        verifier, _ = _verifier([_jwk(key)], fail=True)
        with pytest.raises(AuthServiceUnavailableError):
            await verifier.introspect(_sign(key))

    async def test_jwks_non_200_with_no_cache_is_503(self) -> None:
        key = _keypair()
        verifier, _ = _verifier([_jwk(key)], status=503)
        with pytest.raises(AuthServiceUnavailableError):
            await verifier.introspect(_sign(key))
