"""Tests for certificate PDF rendering (use case + ReportLab adapter)."""

from __future__ import annotations

import uuid
from datetime import UTC, datetime
from uuid import UUID

import pytest

from cyberdyne_backend.adapters.outbound.certificates.pdf import ReportlabCertificateRenderer
from cyberdyne_backend.application.learning import RenderCertificatePdf
from cyberdyne_backend.domain.learning import (
    Certificate,
    CertificateNotFoundError,
    LearningContentNotFoundError,
    LearningPath,
)


def _cert() -> Certificate:
    return Certificate(
        id=uuid.uuid4(),
        user_id=uuid.uuid4(),
        path_slug="blockchain-dev",
        issued_at=datetime(2026, 1, 1, tzinfo=UTC),
        verification_hash="abc123",
        signed_payload="sig",
    )


def _path(slug: str, title: str) -> LearningPath:
    return LearningPath(
        slug=slug,
        title=title,
        description="d",
        module_slugs=("m1",),
        estimated_time="4w",
        icon="x",
    )


class _FakeRenderer:
    def __init__(self) -> None:
        self.calls: list[tuple[str, str]] = []

    def render(self, *, certificate: Certificate, path_title: str, verify_url: str) -> bytes:
        self.calls.append((path_title, verify_url))
        return b"%PDF-FAKE"


class _FakeRepo:
    def __init__(self, cert: Certificate | None, path: LearningPath | None) -> None:
        self._cert = cert
        self._path = path

    async def get_certificate_by_id(self, certificate_id: UUID) -> Certificate | None:
        return self._cert if self._cert and self._cert.id == certificate_id else None

    async def get_path(self, slug: str) -> LearningPath:
        if self._path is None:
            raise LearningContentNotFoundError(slug)
        return self._path


class TestRenderCertificatePdf:
    async def test_renders_with_path_title_and_verify_url(self) -> None:
        cert = _cert()
        renderer = _FakeRenderer()
        repo = _FakeRepo(cert, _path("blockchain-dev", "Blockchain Developer"))
        uc = RenderCertificatePdf(repo=repo, renderer=renderer, verify_url_base="https://x.test/")
        out = await uc.execute(cert.id)
        assert out == b"%PDF-FAKE"
        title, verify_url = renderer.calls[0]
        assert title == "Blockchain Developer"
        assert verify_url == f"https://x.test/api/v1/learning/certificates/{cert.id}/verify"

    async def test_falls_back_to_slug_when_path_gone(self) -> None:
        cert = _cert()
        renderer = _FakeRenderer()
        uc = RenderCertificatePdf(
            repo=_FakeRepo(cert, None), renderer=renderer, verify_url_base="https://x.test"
        )
        await uc.execute(cert.id)
        assert renderer.calls[0][0] == "blockchain-dev"

    async def test_missing_certificate_raises(self) -> None:
        uc = RenderCertificatePdf(
            repo=_FakeRepo(None, None),
            renderer=_FakeRenderer(),
            verify_url_base="https://x.test",
        )
        with pytest.raises(CertificateNotFoundError):
            await uc.execute(uuid.uuid4())


class TestReportlabRenderer:
    def test_produces_a_pdf(self) -> None:
        pdf = ReportlabCertificateRenderer().render(
            certificate=_cert(),
            path_title="Blockchain Developer",
            verify_url="https://x.test/verify",
        )
        assert pdf.startswith(b"%PDF")
        assert len(pdf) > 500  # a real document, not an empty stub
