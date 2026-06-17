"""Redaction of Stripe webhook payloads before they're persisted.

The stored copy in ``stripe_webhook_events.payload`` is for idempotency +
audit/debug only — order fulfillment reads the live verified event, never
this row (see ``application/marketplace/use_cases.py``). So we strip PII /
regulated fields from the stored copy: a Stripe event can carry customer
emails, billing addresses, and card identifiers (last4 / BIN) that
shouldn't accumulate in our database. Structural fields (ids, type,
amounts, status) are preserved so the row stays useful for debugging.
Issue #7.
"""

from __future__ import annotations

from typing import cast

# Values under these keys are masked anywhere they appear in the payload
# tree. Matched case-insensitively.
_SENSITIVE_KEYS = frozenset(
    {
        "email",
        "customer_email",
        "receipt_email",
        "name",
        "phone",
        "address",
        "line1",
        "line2",
        "city",
        "state",
        "postal_code",
        "last4",
        "dynamic_last4",
        "iin",
        "bin",
        "fingerprint",
    }
)

_REDACTED = "[redacted]"


def _redact(value: object) -> object:
    if isinstance(value, dict):
        return {
            key: (_REDACTED if key.lower() in _SENSITIVE_KEYS else _redact(val))
            for key, val in value.items()
        }
    if isinstance(value, list):
        return [_redact(item) for item in value]
    return value


def redact_webhook_payload(payload: dict[str, object]) -> dict[str, object]:
    """Return a deep copy of ``payload`` with sensitive values masked by key
    name, preserving the rest of the structure."""
    return cast(dict[str, object], _redact(payload))
