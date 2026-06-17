"""Unit tests for Stripe webhook payload redaction (issue #7)."""

from __future__ import annotations

import pytest

from cyberdyne_backend.adapters.outbound.persistence.marketplace.redaction import (
    redact_webhook_payload,
)

pytestmark = pytest.mark.unit


def test_masks_sensitive_keys_at_any_depth() -> None:
    payload = {
        "id": "evt_1",
        "type": "checkout.session.completed",
        "data": {
            "object": {
                "id": "cs_123",
                "amount_total": 4900,
                "customer_email": "buyer@example.com",
                "customer_details": {
                    "email": "buyer@example.com",
                    "name": "Ada Lovelace",
                    "phone": "+15551234567",
                    "address": {"line1": "1 Infinite Loop", "postal_code": "95014"},
                    "tax_ids": [{"type": "eu_vat", "value": "DE123"}],
                },
            }
        },
    }
    out = redact_webhook_payload(payload)
    obj = out["data"]["object"]  # type: ignore[index]
    # Structural fields preserved.
    assert out["id"] == "evt_1"
    assert out["type"] == "checkout.session.completed"
    assert obj["id"] == "cs_123"
    assert obj["amount_total"] == 4900
    # PII masked at every depth.
    assert obj["customer_email"] == "[redacted]"
    details = obj["customer_details"]
    assert details["email"] == "[redacted]"
    assert details["name"] == "[redacted]"
    assert details["phone"] == "[redacted]"
    # The whole address block is a sensitive key → fully masked.
    assert details["address"] == "[redacted]"
    # Non-sensitive nested structures (and lists) are walked, not dropped.
    assert details["tax_ids"][0]["type"] == "eu_vat"


def test_masks_card_identifiers_inside_lists() -> None:
    payload = {
        "data": {
            "object": {
                "charges": [
                    {
                        "id": "ch_1",
                        "payment_method_details": {
                            "card": {"brand": "visa", "last4": "4242", "fingerprint": "abc"}
                        },
                    }
                ]
            }
        }
    }
    out = redact_webhook_payload(payload)
    card = out["data"]["object"]["charges"][0]["payment_method_details"]["card"]  # type: ignore[index]
    assert card["brand"] == "visa"  # structural kept
    assert card["last4"] == "[redacted]"
    assert card["fingerprint"] == "[redacted]"


def test_does_not_mutate_input_and_handles_scalars() -> None:
    payload = {"id": "evt_1", "email": "x@y.com", "live": True, "n": 3}
    out = redact_webhook_payload(payload)
    assert out == {"id": "evt_1", "email": "[redacted]", "live": True, "n": 3}
    # original untouched (fulfillment still reads the live event)
    assert payload["email"] == "x@y.com"
