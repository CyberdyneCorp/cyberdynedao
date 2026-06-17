"""The container picks the certificate signer per settings (issue #7)."""

from __future__ import annotations

import base64

import pytest

from cyberdyne_backend.adapters.outbound.certificates.signer import (
    Ed25519CertificateSigner,
    EphemeralCertificateSigner,
    HmacCertificateSigner,
)
from cyberdyne_backend.infrastructure.container import Container
from cyberdyne_backend.infrastructure.settings import Settings

_SEED = base64.urlsafe_b64encode(b"\x02" * 32).rstrip(b"=").decode()


def test_default_is_ephemeral_hmac() -> None:
    signer = Container(Settings(environment="local")).certificate_signer
    assert isinstance(signer, EphemeralCertificateSigner)


def test_hmac_when_secret_set() -> None:
    signer = Container(Settings(environment="local", cert_signing_key="shared")).certificate_signer
    assert isinstance(signer, HmacCertificateSigner)
    assert not isinstance(signer, EphemeralCertificateSigner)


def test_ed25519_when_selected() -> None:
    signer = Container(
        Settings(
            environment="local",
            cert_signer="ed25519",
            cert_ed25519_private_key=_SEED,
        )
    ).certificate_signer
    assert isinstance(signer, Ed25519CertificateSigner)


def test_ed25519_without_key_raises() -> None:
    container = Container(Settings(environment="local", cert_signer="ed25519"))
    with pytest.raises(ValueError, match="CERT_ED25519_PRIVATE_KEY"):
        _ = container.certificate_signer
