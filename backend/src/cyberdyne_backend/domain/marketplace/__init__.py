"""Marketplace bounded context.

Three product types behave very differently:
- ``service`` — routes to lead capture (creates an Ask), no payment.
- ``training`` — Stripe one-time charge, on paid grants enrollment in
  the linked LearningPath (auto-grant bridge to the Learning context).
- ``license`` — Stripe one-time charge, on paid provisions a
  ``LicenseKey`` returned + emailed to the user.

The Stripe webhook is dispatched through a dedicated idempotency table
(``WebhookEvent``) so retries from Stripe never double-fulfill an order.
"""

from cyberdyne_backend.domain.marketplace.entities import (
    LicenseKey,
    Order,
    OrderStatus,
    Product,
    ProductStatus,
    ProductType,
    WebhookEvent,
    new_license_key,
    new_order,
    new_webhook_event,
)
from cyberdyne_backend.domain.marketplace.errors import (
    DuplicateWebhookError,
    InvalidProductForCheckoutError,
    LicenseAlreadyRevokedError,
    OrderNotFoundError,
    OrderStateTransitionError,
    ProductNotFoundError,
    StripeSignatureError,
)
from cyberdyne_backend.domain.marketplace.ports import (
    CheckoutSession,
    LicenseEmailNotifierPort,
    MarketplaceRepository,
    StripeCheckoutPort,
    StripeWebhookEvent,
    StripeWebhookVerifierPort,
)

__all__ = [
    "CheckoutSession",
    "DuplicateWebhookError",
    "InvalidProductForCheckoutError",
    "LicenseAlreadyRevokedError",
    "LicenseEmailNotifierPort",
    "LicenseKey",
    "MarketplaceRepository",
    "Order",
    "OrderNotFoundError",
    "OrderStateTransitionError",
    "OrderStatus",
    "Product",
    "ProductNotFoundError",
    "ProductStatus",
    "ProductType",
    "StripeCheckoutPort",
    "StripeSignatureError",
    "StripeWebhookEvent",
    "StripeWebhookVerifierPort",
    "WebhookEvent",
    "new_license_key",
    "new_order",
    "new_webhook_event",
]
