"""Tests for the UserProfile entity + CyberdyneAuth /users/me client."""

from __future__ import annotations

import uuid

import httpx
import pytest

from cyberdyne_backend.adapters.outbound.auth.profile_client import CyberdyneAuthProfileClient
from cyberdyne_backend.domain.auth_identity import UserProfile, profile_from_users_me


class TestProfileEntity:
    def test_maps_users_me_payload(self) -> None:
        payload = {
            "id": str(uuid.uuid4()),
            "email": "leo@amini.ai",
            "wallet_address": "0xABC",
            "organization_id": None,
            "is_email_verified": True,
        }
        profile = profile_from_users_me(payload)
        assert profile is not None
        assert profile.email == "leo@amini.ai"
        assert profile.wallet_address == "0xABC"
        assert profile.is_email_verified is True

    def test_missing_id_returns_none(self) -> None:
        assert profile_from_users_me({"email": "x@y.z"}) is None

    def test_invalid_id_returns_none(self) -> None:
        assert profile_from_users_me({"id": "not-a-uuid"}) is None

    def test_display_name_prefers_email_local_part(self) -> None:
        p = UserProfile(user_id=uuid.uuid4(), email="leo@amini.ai")
        assert p.display_name == "leo"

    def test_display_name_falls_back_to_wallet(self) -> None:
        p = UserProfile(
            user_id=uuid.uuid4(),
            email=None,
            wallet_address="0x1234567890abcdef1234",
        )
        assert p.display_name == "0x1234…1234"

    def test_display_name_none_when_no_handle(self) -> None:
        assert UserProfile(user_id=uuid.uuid4(), email=None).display_name is None


def _client_with(handler, ttl_s: float = 60.0) -> tuple[CyberdyneAuthProfileClient, dict[str, int]]:
    counter = {"calls": 0}

    def _wrapped(request: httpx.Request) -> httpx.Response:
        counter["calls"] += 1
        return handler(request)

    transport = httpx.MockTransport(_wrapped)
    http = httpx.AsyncClient(transport=transport)
    client = CyberdyneAuthProfileClient(
        base_url="https://auth.example", http_client=http, ttl_s=ttl_s
    )
    return client, counter


class TestProfileClient:
    async def test_fetches_and_maps_profile(self) -> None:
        uid = str(uuid.uuid4())

        def handler(request: httpx.Request) -> httpx.Response:
            assert request.headers["Authorization"] == "Bearer tok"
            assert request.url.path == "/api/v1/users/me"
            return httpx.Response(200, json={"id": uid, "email": "a@b.c"})

        client, counter = _client_with(handler)
        profile = await client.get_profile("tok")
        assert profile is not None
        assert profile.email == "a@b.c"
        assert counter["calls"] == 1

    async def test_caches_within_ttl(self) -> None:
        def handler(request: httpx.Request) -> httpx.Response:
            return httpx.Response(200, json={"id": str(uuid.uuid4()), "email": "a@b.c"})

        client, counter = _client_with(handler)
        await client.get_profile("tok")
        await client.get_profile("tok")
        assert counter["calls"] == 1  # second call served from cache

    async def test_empty_token_returns_none_without_call(self) -> None:
        client, counter = _client_with(lambda r: httpx.Response(200, json={}))
        assert await client.get_profile("") is None
        assert counter["calls"] == 0

    async def test_non_200_resolves_to_none(self) -> None:
        client, _ = _client_with(lambda r: httpx.Response(401, json={"detail": "nope"}))
        assert await client.get_profile("tok") is None

    async def test_transport_error_resolves_to_none(self) -> None:
        def handler(request: httpx.Request) -> httpx.Response:
            raise httpx.ConnectError("boom")

        client, _ = _client_with(handler)
        assert await client.get_profile("tok") is None


# Suppress unused-import lint.
_ = pytest
