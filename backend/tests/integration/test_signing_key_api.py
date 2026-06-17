"""The public signing-key endpoint publishes the verification key (#7)."""

from __future__ import annotations

import base64

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from cyberdyne_backend.adapters.inbound.api.learning.router import get_signing_key_info
from cyberdyne_backend.adapters.inbound.api.learning.schemas import SigningKeyResponse
from cyberdyne_backend.adapters.outbound.certificates.signer import (
    Ed25519CertificateSigner,
    verify_with_public_key,
)

pytestmark = pytest.mark.integration


def test_hmac_publishes_no_key(app: FastAPI) -> None:
    app.dependency_overrides[get_signing_key_info] = lambda: SigningKeyResponse(
        algorithm="hmac-sha256", public_key=None
    )
    resp = TestClient(app).get("/api/v1/learning/certificates/signing-key")
    assert resp.status_code == 200
    body = resp.json()
    assert body["algorithm"] == "hmac-sha256"
    assert body["publicKey"] is None


def test_ed25519_publishes_a_usable_public_key(app: FastAPI) -> None:
    seed = base64.urlsafe_b64encode(b"\x03" * 32).rstrip(b"=").decode()
    signer = Ed25519CertificateSigner(seed)
    app.dependency_overrides[get_signing_key_info] = lambda: SigningKeyResponse(
        algorithm="ed25519", public_key=signer.public_key_b64
    )

    resp = TestClient(app).get("/api/v1/learning/certificates/signing-key")
    assert resp.status_code == 200
    published = resp.json()["publicKey"]
    assert published == signer.public_key_b64

    # The published key actually verifies a signature this signer makes —
    # i.e. an external verifier could use it.
    sig = signer.sign("sub=u1;course=c1")
    assert (
        verify_with_public_key(message="sub=u1;course=c1", signature=sig, public_key_b64=published)
        is True
    )
