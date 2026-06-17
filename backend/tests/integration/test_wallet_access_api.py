"""End-to-end tests for the wallet access-tier endpoint (issue #7)."""

from __future__ import annotations

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from cyberdyne_backend.adapters.inbound.api.wallet.router import get_wallet_access_uc
from cyberdyne_backend.adapters.outbound.access.fake_reader import FakeAccessReader
from cyberdyne_backend.application.access import GetWalletAccess
from cyberdyne_backend.domain.access import AccessTraits, WalletAccess

pytestmark = pytest.mark.integration

_ADDR = "0x1111111111111111111111111111111111111111"


def test_default_reports_no_access(app: FastAPI) -> None:
    # Real wiring → stub reader → no NFT for any address.
    client = TestClient(app)
    resp = client.get(f"/api/v1/wallet/{_ADDR}/access-tier")
    assert resp.status_code == 200
    body = resp.json()
    assert body["address"] == _ADDR
    assert body["hasAccessNft"] is False
    assert body["tokenCount"] == 0
    assert body["traits"] == {
        "learning": False,
        "frontend": False,
        "backend": False,
        "blogCreator": False,
        "admin": False,
        "marketplace": False,
    }


def test_rejects_malformed_address(app: FastAPI) -> None:
    client = TestClient(app)
    resp = client.get("/api/v1/wallet/not-an-address/access-tier")
    assert resp.status_code == 400


def test_surfaces_granted_traits(app: FastAPI) -> None:
    granted = WalletAccess(
        address=_ADDR,
        has_access_nft=True,
        token_count=2,
        traits=AccessTraits(learning=True, blog_creator=True),
    )
    reader = FakeAccessReader({_ADDR: granted})
    app.dependency_overrides[get_wallet_access_uc] = lambda: GetWalletAccess(reader=reader)
    try:
        resp = TestClient(app).get(f"/api/v1/wallet/{_ADDR}/access-tier")
    finally:
        app.dependency_overrides.pop(get_wallet_access_uc, None)
    assert resp.status_code == 200
    body = resp.json()
    assert body["hasAccessNft"] is True
    assert body["tokenCount"] == 2
    assert body["traits"]["learning"] is True
    assert body["traits"]["blogCreator"] is True  # camelCase aliasing
    assert body["traits"]["admin"] is False
