"""End-to-end tests for the public certificate-verify endpoint."""

from __future__ import annotations

import uuid
from collections.abc import AsyncIterator
from datetime import UTC, datetime

import pytest
import pytest_asyncio
from fastapi import FastAPI
from fastapi.testclient import TestClient

from cyberdyne_backend.adapters.inbound.api.learning.router import get_verify_certificate_uc
from cyberdyne_backend.adapters.outbound.certificates.signer import HmacCertificateSigner
from cyberdyne_backend.adapters.outbound.persistence.learning.models import CertificateRow
from cyberdyne_backend.adapters.outbound.persistence.learning.repository import (
    SqlAlchemyLearningRepository,
)
from cyberdyne_backend.application.learning import VerifyCertificate
from cyberdyne_backend.infrastructure.database.engine import get_session_factory, session_scope

pytestmark = pytest.mark.integration

_SIGNER = HmacCertificateSigner(secret="test-verify-secret")
_NOW = datetime(2026, 1, 1, tzinfo=UTC)
_VALID_ID = uuid.UUID("55555555-5555-5555-5555-555555555555")
_TAMPERED_ID = uuid.UUID("66666666-6666-6666-6666-666666666666")
_HASH = "deadbeefcafe"


@pytest_asyncio.fixture
async def seeded(_prepared_schema: None) -> AsyncIterator[None]:
    factory = get_session_factory()
    async with factory() as s:
        s.add_all(
            [
                CertificateRow(
                    id=_VALID_ID,
                    user_id=uuid.uuid4(),
                    path_slug="p1",
                    issued_at=_NOW,
                    verification_hash=_HASH,
                    signed_payload=_SIGNER.sign(_HASH),
                ),
                CertificateRow(
                    id=_TAMPERED_ID,
                    user_id=uuid.uuid4(),
                    path_slug="p1",
                    issued_at=_NOW,
                    verification_hash=_HASH,
                    signed_payload="not-a-valid-signature",
                ),
            ]
        )
        await s.commit()
    yield


@pytest.fixture
def verify_client(app: FastAPI) -> TestClient:
    async def _dep() -> AsyncIterator[VerifyCertificate]:
        async with session_scope() as session:
            yield VerifyCertificate(repo=SqlAlchemyLearningRepository(session), signer=_SIGNER)

    app.dependency_overrides[get_verify_certificate_uc] = _dep
    return TestClient(app)


def test_valid_certificate_verifies(seeded: None, verify_client: TestClient) -> None:
    resp = verify_client.get(f"/api/v1/learning/certificates/{_VALID_ID}/verify")
    assert resp.status_code == 200, resp.text
    body = resp.json()
    assert body["valid"] is True
    assert body["certificate"]["id"] == str(_VALID_ID)
    assert body["certificate"]["pathSlug"] == "p1"


def test_tampered_certificate_is_invalid(seeded: None, verify_client: TestClient) -> None:
    body = verify_client.get(f"/api/v1/learning/certificates/{_TAMPERED_ID}/verify").json()
    assert body["valid"] is False
    # Claims still returned so a verify page can show what was presented.
    assert body["certificate"]["id"] == str(_TAMPERED_ID)


def test_unknown_certificate_is_invalid_null(seeded: None, verify_client: TestClient) -> None:
    body = verify_client.get(f"/api/v1/learning/certificates/{uuid.uuid4()}/verify").json()
    assert body["valid"] is False
    assert body["certificate"] is None


def test_verify_is_public(seeded: None, verify_client: TestClient) -> None:
    # No auth dependency overridden / no token — still 200.
    assert verify_client.get(f"/api/v1/learning/certificates/{_VALID_ID}/verify").status_code == 200
