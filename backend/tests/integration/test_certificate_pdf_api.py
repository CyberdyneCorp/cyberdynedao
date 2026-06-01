"""End-to-end test for the certificate PDF download endpoint."""

from __future__ import annotations

import uuid
from collections.abc import AsyncIterator
from datetime import UTC, datetime

import pytest
import pytest_asyncio
from fastapi import FastAPI
from fastapi.testclient import TestClient

from cyberdyne_backend.adapters.inbound.api.learning.router import get_render_pdf_uc
from cyberdyne_backend.adapters.outbound.certificates.pdf import ReportlabCertificateRenderer
from cyberdyne_backend.adapters.outbound.persistence.learning.models import CertificateRow
from cyberdyne_backend.adapters.outbound.persistence.learning.repository import (
    SqlAlchemyLearningRepository,
)
from cyberdyne_backend.application.learning import RenderCertificatePdf
from cyberdyne_backend.infrastructure.database.engine import get_session_factory, session_scope

pytestmark = pytest.mark.integration

_CERT_ID = uuid.UUID("77777777-7777-7777-7777-777777777777")
_NOW = datetime(2026, 1, 1, tzinfo=UTC)


@pytest_asyncio.fixture
async def seeded(_prepared_schema: None) -> AsyncIterator[None]:
    factory = get_session_factory()
    async with factory() as s:
        s.add(
            CertificateRow(
                id=_CERT_ID,
                user_id=uuid.uuid4(),
                path_slug="p1",
                issued_at=_NOW,
                verification_hash="hash",
                signed_payload="sig",
            )
        )
        await s.commit()
    yield


@pytest.fixture
def pdf_client(app: FastAPI) -> TestClient:
    async def _dep() -> AsyncIterator[RenderCertificatePdf]:
        async with session_scope() as session:
            yield RenderCertificatePdf(
                repo=SqlAlchemyLearningRepository(session),
                renderer=ReportlabCertificateRenderer(),
                verify_url_base="https://academy.test",
            )

    app.dependency_overrides[get_render_pdf_uc] = _dep
    return TestClient(app)


def test_download_pdf(seeded: None, pdf_client: TestClient) -> None:
    resp = pdf_client.get(f"/api/v1/learning/certificates/{_CERT_ID}/pdf")
    assert resp.status_code == 200, resp.text
    assert resp.headers["content-type"] == "application/pdf"
    assert resp.headers["content-disposition"].startswith("attachment;")
    assert resp.content.startswith(b"%PDF")


def test_unknown_certificate_404(seeded: None, pdf_client: TestClient) -> None:
    resp = pdf_client.get(f"/api/v1/learning/certificates/{uuid.uuid4()}/pdf")
    assert resp.status_code == 404
