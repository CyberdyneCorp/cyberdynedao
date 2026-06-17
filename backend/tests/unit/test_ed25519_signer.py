"""Unit tests for the Ed25519 certificate signer (issue #7)."""

from __future__ import annotations

import pytest

from cyberdyne_backend.adapters.outbound.certificates.signer import (
    Ed25519CertificateSigner,
    HmacCertificateSigner,
    verify_with_public_key,
)


def test_sign_then_verify_roundtrip() -> None:
    signer = Ed25519CertificateSigner.generate()
    sig = signer.sign("sub=u1;course=c1")
    assert signer.verify("sub=u1;course=c1", sig) is True


def test_tampered_message_fails() -> None:
    signer = Ed25519CertificateSigner.generate()
    sig = signer.sign("sub=u1;course=c1")
    assert signer.verify("sub=u1;course=TAMPERED", sig) is False


def test_garbage_signature_fails_not_raises() -> None:
    signer = Ed25519CertificateSigner.generate()
    assert signer.verify("m", "not-base64-???") is False
    assert signer.verify("m", "") is False


def test_external_verifier_with_public_key_only() -> None:
    signer = Ed25519CertificateSigner.generate()
    msg = "sub=u1;course=c1"
    sig = signer.sign(msg)
    # A partner holding only the published public key can verify.
    assert (
        verify_with_public_key(message=msg, signature=sig, public_key_b64=signer.public_key_b64)
        is True
    )
    # A different key does not verify.
    other = Ed25519CertificateSigner.generate()
    assert (
        verify_with_public_key(message=msg, signature=sig, public_key_b64=other.public_key_b64)
        is False
    )


def test_same_seed_yields_same_key_and_cross_verifies() -> None:
    # Two signers built from the same 32-byte seed share a public key, and
    # one verifies the other's signatures.
    import base64

    seed = base64.urlsafe_b64encode(b"\x01" * 32).rstrip(b"=").decode()
    a = Ed25519CertificateSigner(seed)
    b = Ed25519CertificateSigner(seed)
    assert a.public_key_b64 == b.public_key_b64
    assert b.verify("m", a.sign("m")) is True


def test_bad_key_material_rejected() -> None:
    with pytest.raises(ValueError, match="32-byte"):
        Ed25519CertificateSigner("c2hvcnQ")  # decodes to <32 bytes
    with pytest.raises(ValueError, match="base64"):
        Ed25519CertificateSigner("not valid base64 !!!")


def test_hmac_and_ed25519_signatures_do_not_cross_verify() -> None:
    ed = Ed25519CertificateSigner.generate()
    hm = HmacCertificateSigner(secret="s3cret")
    msg = "sub=u1"
    assert ed.verify(msg, hm.sign(msg)) is False
    assert hm.verify(msg, ed.sign(msg)) is False
