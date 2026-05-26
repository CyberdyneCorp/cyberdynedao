"""Stripe webhook signature verifier.

Stripe signs every webhook body with a per-endpoint ``whsec_…`` secret.
The header looks like::

    Stripe-Signature: t=1614036000,v1=<hex>,v1=<hex>

We implement the same algorithm Stripe documents — `t.<raw_body>`
HMAC-SHA256 with the secret, then constant-time compared against the
``v1`` values. Reject if no ``v1`` matches; reject if ``t`` is too old.

Mock variant always returns the parsed event without verification —
used in tests and dev.
"""

from __future__ import annotations

import hashlib
import hmac
import json
import time
from typing import cast

from cyberdyne_backend.domain.marketplace import StripeSignatureError, StripeWebhookEvent

DEFAULT_TOLERANCE_SECONDS = 300


class StripeWebhookVerifier:
    def __init__(
        self,
        *,
        signing_secret: str,
        tolerance_seconds: int = DEFAULT_TOLERANCE_SECONDS,
        now: float | None = None,
    ) -> None:
        if not signing_secret:
            raise ValueError("Stripe webhook signing_secret is required")
        self._secret = signing_secret.encode("utf-8")
        self._tolerance = tolerance_seconds
        self._now = now  # frozen-time hook for tests; None ⇒ time.time()

    def verify(
        self,
        *,
        raw_body: bytes,
        signature_header: str,
    ) -> StripeWebhookEvent:
        timestamp, sigs = self._parse_signature_header(signature_header)
        moment = self._now if self._now is not None else time.time()
        if abs(moment - timestamp) > self._tolerance:
            raise StripeSignatureError("stripe webhook timestamp outside tolerance")
        payload_to_sign = f"{timestamp}.".encode() + raw_body
        expected = hmac.new(self._secret, payload_to_sign, hashlib.sha256).hexdigest()
        if not any(hmac.compare_digest(expected, candidate) for candidate in sigs):
            raise StripeSignatureError("stripe webhook signature mismatch")
        body = cast(dict[str, object], json.loads(raw_body.decode("utf-8")))
        event_id = cast(str, body.get("id", ""))
        event_type = cast(str, body.get("type", ""))
        if not event_id or not event_type:
            raise StripeSignatureError("stripe webhook body missing id / type")
        return StripeWebhookEvent(
            stripe_event_id=event_id,
            type=event_type,
            payload=body,
        )

    @staticmethod
    def _parse_signature_header(header: str) -> tuple[int, list[str]]:
        if not header:
            raise StripeSignatureError("missing Stripe-Signature header")
        timestamp: int | None = None
        sigs: list[str] = []
        for part in header.split(","):
            if not part or "=" not in part:
                continue
            key, _, value = part.partition("=")
            key = key.strip()
            value = value.strip()
            if key == "t":
                try:
                    timestamp = int(value)
                except ValueError as exc:
                    raise StripeSignatureError("invalid Stripe-Signature timestamp") from exc
            elif key == "v1":
                sigs.append(value)
        if timestamp is None or not sigs:
            raise StripeSignatureError("Stripe-Signature header malformed")
        return timestamp, sigs


class MockStripeWebhookVerifier:
    """No-op verifier — used when ``STRIPE_WEBHOOK_SECRET`` is unset.

    Trusts whatever the caller sends. Local dev only; will refuse to
    initialise in staging/production via a settings-side guard.
    """

    def verify(
        self,
        *,
        raw_body: bytes,
        signature_header: str,
    ) -> StripeWebhookEvent:
        body = cast(dict[str, object], json.loads(raw_body.decode("utf-8")))
        return StripeWebhookEvent(
            stripe_event_id=cast(str, body.get("id", "evt_mock")),
            type=cast(str, body.get("type", "")),
            payload=body,
        )
