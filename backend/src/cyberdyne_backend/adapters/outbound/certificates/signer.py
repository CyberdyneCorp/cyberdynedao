"""Certificate signers.

``HmacCertificateSigner`` (HMAC-SHA256, shared secret) is the default —
stdlib-only, fine for "prove the holder hasn't tampered with the claims"
when our own backend is the only verifier.

``Ed25519CertificateSigner`` (public/private keypair) is for when external
verifiers — partner LMSes, an NFT minting service — must verify WITHOUT
holding our secret: we publish the public key, they verify, only we can
sign. Selected via ``CERT_SIGNER=ed25519`` + ``CERT_ED25519_PRIVATE_KEY``.
"""

from __future__ import annotations

import base64
import binascii
import hashlib
import hmac
import logging
import secrets

from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives.asymmetric.ed25519 import (
    Ed25519PrivateKey,
    Ed25519PublicKey,
)

logger = logging.getLogger("cyberdyne_backend.certificates")


def _b64url_encode(raw: bytes) -> str:
    return base64.urlsafe_b64encode(raw).rstrip(b"=").decode("ascii")


def _b64url_decode(value: str) -> bytes:
    padded = value + "=" * (-len(value) % 4)
    return base64.urlsafe_b64decode(padded.encode("ascii"))


class HmacCertificateSigner:
    """HMAC-SHA256 over the verification hash. Output is a URL-safe
    base64 string suitable to embed in a JSON-shaped certificate."""

    def __init__(self, secret: str) -> None:
        if not secret:
            raise ValueError("certificate signer secret cannot be empty")
        self._secret = secret.encode("utf-8")

    def sign(self, message: str) -> str:
        digest = hmac.new(self._secret, message.encode("utf-8"), hashlib.sha256).digest()
        return _b64url_encode(digest)

    def verify(self, message: str, signature: str) -> bool:
        expected = self.sign(message)
        return hmac.compare_digest(expected, signature)


class EphemeralCertificateSigner(HmacCertificateSigner):
    """Used when ``CERT_SIGNING_KEY`` isn't configured. The secret is
    re-generated on every process start, which means any signature it
    issues only validates within the lifetime of this process. Fine
    for local dev; logs a warning in non-local environments so
    misconfigured prod is loud."""

    def __init__(self, environment: str = "local") -> None:
        if environment in ("staging", "production"):
            logger.warning(
                "EphemeralCertificateSigner active in %s — set CERT_SIGNING_KEY",
                environment,
            )
        super().__init__(secret=secrets.token_urlsafe(32))


class Ed25519CertificateSigner:
    """Ed25519 signatures over the verification hash. We hold the private
    key; verifiers need only the public key (exposed via
    ``public_key_b64``), so partners can verify a certificate without our
    secret. Signature + public key are URL-safe base64 (no padding)."""

    def __init__(self, private_key_b64: str) -> None:
        try:
            seed = _b64url_decode(private_key_b64)
        except (ValueError, binascii.Error) as exc:
            raise ValueError("CERT_ED25519_PRIVATE_KEY is not valid base64") from exc
        if len(seed) != 32:
            raise ValueError("CERT_ED25519_PRIVATE_KEY must be a 32-byte seed (base64url-encoded)")
        self._private = Ed25519PrivateKey.from_private_bytes(seed)
        self._public = self._private.public_key()

    @classmethod
    def generate(cls) -> Ed25519CertificateSigner:
        """Mint a random keypair — used by tests and key-provisioning."""
        seed = Ed25519PrivateKey.generate().private_bytes_raw()
        return cls(_b64url_encode(seed))

    @property
    def public_key_b64(self) -> str:
        return _b64url_encode(self._public.public_bytes_raw())

    def sign(self, message: str) -> str:
        return _b64url_encode(self._private.sign(message.encode("utf-8")))

    def verify(self, message: str, signature: str) -> bool:
        try:
            self._public.verify(_b64url_decode(signature), message.encode("utf-8"))
        except (InvalidSignature, ValueError, binascii.Error):
            return False
        return True


def verify_with_public_key(*, message: str, signature: str, public_key_b64: str) -> bool:
    """Standalone verification for an external holder of just the public
    key (mirrors what a partner verifier would run)."""
    try:
        public = Ed25519PublicKey.from_public_bytes(_b64url_decode(public_key_b64))
        public.verify(_b64url_decode(signature), message.encode("utf-8"))
    except (InvalidSignature, ValueError, binascii.Error):
        return False
    return True
