"""Ports for the marketplace context."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol, runtime_checkable
from uuid import UUID

from cyberdyne_backend.domain.marketplace.entities import (
    LicenseKey,
    Order,
    Product,
    WebhookEvent,
)


@dataclass(frozen=True, slots=True)
class CheckoutSession:
    """Returned by the Stripe checkout port. The router serializes
    ``url`` back to the browser for redirect."""

    session_id: str
    url: str


@dataclass(frozen=True, slots=True)
class StripeWebhookEvent:
    """Parsed + signature-verified Stripe event. ``payload`` is the raw
    decoded JSON body so the dispatcher can pull whatever fields it
    needs per event type."""

    stripe_event_id: str
    type: str
    payload: dict[str, object]


@runtime_checkable
class StripeCheckoutPort(Protocol):
    async def create_checkout_session(
        self,
        *,
        product: Product,
        user_id: UUID,
        success_url: str,
        cancel_url: str,
        client_reference_id: str | None = None,
    ) -> CheckoutSession: ...


@runtime_checkable
class StripeWebhookVerifierPort(Protocol):
    def verify(
        self,
        *,
        raw_body: bytes,
        signature_header: str,
    ) -> StripeWebhookEvent:
        """Verifies the ``Stripe-Signature`` header against ``raw_body``
        using the configured signing secret. Raises
        ``StripeSignatureError`` on mismatch."""
        ...


@runtime_checkable
class LicenseEmailNotifierPort(Protocol):
    async def send_license_email(
        self,
        *,
        to_email: str,
        product_title: str,
        plaintext_key: str,
        expires_at_iso: str | None,
    ) -> None: ...


@runtime_checkable
class MarketplaceRepository(Protocol):
    # Catalogue (seeded, read-only at runtime)
    async def list_products(
        self,
        *,
        category: str | None = None,
        product_type: str | None = None,
    ) -> list[Product]: ...
    async def get_product(self, slug: str) -> Product: ...

    # Orders
    async def save_order(self, order: Order) -> None: ...
    async def get_order(self, order_id: UUID) -> Order: ...
    async def get_order_by_session_id(self, session_id: str) -> Order | None: ...
    async def get_order_by_payment_intent(self, payment_intent_id: str) -> Order | None: ...
    async def list_orders_for_user(self, user_id: UUID) -> list[Order]: ...

    # Licenses
    async def save_license(self, license_key: LicenseKey) -> None: ...
    async def get_license(self, license_id: UUID) -> LicenseKey: ...
    async def list_licenses_for_user(self, user_id: UUID) -> list[LicenseKey]: ...

    # Webhook idempotency
    async def record_webhook_event(self, event: WebhookEvent) -> bool:
        """Returns ``True`` if newly recorded, ``False`` if the event id
        was already seen. ``INSERT … ON CONFLICT DO NOTHING`` shape."""
        ...
