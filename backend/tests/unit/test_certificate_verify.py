"""Use-case tests for public certificate verification."""

from __future__ import annotations

import uuid
from datetime import UTC, datetime
from uuid import UUID

from cyberdyne_backend.application.learning import VerifyCertificate
from cyberdyne_backend.domain.learning import Certificate


class _FakeSigner:
    """Deterministic toy signer: signature is ``sig:<message>``."""

    def sign(self, message: str) -> str:
        return f"sig:{message}"

    def verify(self, message: str, signature: str) -> bool:
        return signature == self.sign(message)


class _FakeRepo:
    def __init__(self, cert: Certificate | None = None) -> None:
        self._cert = cert

    async def get_certificate_by_id(self, certificate_id: UUID) -> Certificate | None:
        if self._cert is not None and self._cert.id == certificate_id:
            return self._cert
        return None


def _cert(signed_payload: str) -> Certificate:
    return Certificate(
        id=uuid.uuid4(),
        user_id=uuid.uuid4(),
        path_slug="p1",
        issued_at=datetime(2026, 1, 1, tzinfo=UTC),
        verification_hash="abc123",
        signed_payload=signed_payload,
    )


class TestVerifyCertificate:
    async def test_valid_signature(self) -> None:
        signer = _FakeSigner()
        cert = _cert(signed_payload=signer.sign("abc123"))
        result = await VerifyCertificate(repo=_FakeRepo(cert), signer=signer).execute(cert.id)
        assert result.valid is True
        assert result.certificate is not None
        assert result.certificate.id == cert.id

    async def test_tampered_signature_invalid(self) -> None:
        signer = _FakeSigner()
        cert = _cert(signed_payload="sig:WRONG")
        result = await VerifyCertificate(repo=_FakeRepo(cert), signer=signer).execute(cert.id)
        assert result.valid is False
        assert result.certificate is not None  # returned so the page can show the (invalid) claims

    async def test_missing_certificate(self) -> None:
        signer = _FakeSigner()
        result = await VerifyCertificate(repo=_FakeRepo(None), signer=signer).execute(uuid.uuid4())
        assert result.valid is False
        assert result.certificate is None
