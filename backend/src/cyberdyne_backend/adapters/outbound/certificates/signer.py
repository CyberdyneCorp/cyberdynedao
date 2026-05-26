"""Certificate signers — HMAC-SHA256 today, Ed25519 in a follow-up.

Why HMAC for now: stdlib-only, no extra dep, perfectly fine for the
"prove the holder hasn't tampered with the claims" use case at this
stage. Verifier holds the same shared secret. We swap to Ed25519
(public/private keypair) when external verifiers — partner LMSes, an
NFT minting service — need to verify without holding our secret.
"""

from __future__ import annotations

import base64
import hashlib
import hmac
import logging
import secrets

logger = logging.getLogger("cyberdyne_backend.certificates")


class HmacCertificateSigner:
    """HMAC-SHA256 over the verification hash. Output is a URL-safe
    base64 string suitable to embed in a JSON-shaped certificate."""

    def __init__(self, secret: str) -> None:
        if not secret:
            raise ValueError("certificate signer secret cannot be empty")
        self._secret = secret.encode("utf-8")

    def sign(self, message: str) -> str:
        digest = hmac.new(self._secret, message.encode("utf-8"), hashlib.sha256).digest()
        return base64.urlsafe_b64encode(digest).rstrip(b"=").decode("ascii")

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
