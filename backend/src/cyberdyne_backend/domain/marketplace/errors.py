"""Domain errors for the marketplace context."""

from __future__ import annotations


class ProductNotFoundError(LookupError):
    """No product with that slug exists."""


class OrderNotFoundError(LookupError):
    """No order with that id exists."""


class InvalidProductForCheckoutError(ValueError):
    """``service``-type products don't go through Stripe — they route to
    lead capture instead. Raised when checkout is requested for one."""


class OrderStateTransitionError(ValueError):
    """An order can only move through pending → {paid, failed, refunded}.
    Any other transition is a bug."""


class LicenseAlreadyRevokedError(ValueError):
    """Idempotent revocation: a second revoke against the same license is
    a no-op at the use-case layer, but the entity itself raises."""


class DuplicateWebhookError(RuntimeError):
    """A Stripe webhook with this event id was already processed. Caller
    should treat as success (Stripe retries are normal)."""


class StripeSignatureError(ValueError):
    """Webhook signature did not verify against the configured secret."""
