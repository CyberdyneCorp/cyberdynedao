"""The Stripe webhook caps its payload size before verifying (issue #7)."""

from __future__ import annotations

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from cyberdyne_backend.adapters.inbound.api.marketplace.router import (
    _MAX_WEBHOOK_BYTES,
)

pytestmark = pytest.mark.integration


def test_oversized_webhook_is_rejected_413(app: FastAPI) -> None:
    client = TestClient(app)
    big = b"x" * (_MAX_WEBHOOK_BYTES + 1)
    resp = client.post(
        "/api/v1/stripe/webhook",
        content=big,
        headers={"Stripe-Signature": "t=1,v1=deadbeef"},
    )
    assert resp.status_code == 413
    assert resp.json()["detail"] == "webhook payload too large"


def test_normal_body_passes_the_cap(app: FastAPI) -> None:
    # A small body within the cap is read fine; with no signature header it
    # then fails the missing-signature check (400) — proving the cap let it
    # through rather than blocking it.
    client = TestClient(app)
    resp = client.post("/api/v1/stripe/webhook", content=b'{"id": "evt_1"}')
    assert resp.status_code == 400
    assert resp.json()["detail"] == "missing Stripe-Signature header"
