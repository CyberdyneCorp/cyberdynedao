"""The persisted Stripe webhook row stores a redacted payload (issue #7).

Order fulfillment reads the live verified event, so the stored row is
audit-only and must not accumulate customer PII / card data.
"""

from __future__ import annotations

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from cyberdyne_backend.adapters.outbound.persistence.marketplace.models import (
    StripeWebhookEventRow,
)
from cyberdyne_backend.adapters.outbound.persistence.marketplace.repository import (
    SqlAlchemyMarketplaceRepository,
)
from cyberdyne_backend.domain.marketplace import new_webhook_event

pytestmark = pytest.mark.integration


async def test_stored_payload_is_redacted(db_session: AsyncSession, _prepared_schema: None) -> None:
    repo = SqlAlchemyMarketplaceRepository(db_session)
    payload = {
        "id": "evt_redact_1",
        "type": "checkout.session.completed",
        "data": {
            "object": {
                "id": "cs_xyz",
                "amount_total": 4900,
                "customer_details": {"email": "buyer@example.com", "name": "Ada"},
            }
        },
    }
    was_new = await repo.record_webhook_event(
        new_webhook_event(
            stripe_event_id="evt_redact_1",
            type="checkout.session.completed",
            payload=payload,
        )
    )
    assert was_new is True
    await db_session.flush()

    row = await db_session.get(StripeWebhookEventRow, "evt_redact_1")
    assert row is not None
    obj = row.payload["data"]["object"]
    # Structural fields kept; PII masked.
    assert obj["id"] == "cs_xyz"
    assert obj["amount_total"] == 4900
    assert obj["customer_details"]["email"] == "[redacted]"
    assert obj["customer_details"]["name"] == "[redacted]"
