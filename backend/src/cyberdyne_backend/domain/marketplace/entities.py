"""Marketplace entities + invariants.

Money is integer cents — never float. The frontend formats with
``Intl.NumberFormat``; never with hand-rolled arithmetic.

License keys are stored as bcrypt-style hashes once persisted. The
plaintext only exists in two places: (a) the response to the user
immediately after a successful purchase, and (b) the email we send
them. The entity carries the plaintext optionally — the repository is
expected to strip it before persisting after the first emission.
"""

from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from datetime import UTC, datetime
from enum import StrEnum
from uuid import UUID

from cyberdyne_backend.domain.marketplace.errors import (
    InvalidProductForCheckoutError,
    LicenseAlreadyRevokedError,
    OrderStateTransitionError,
)

# ── Product ──────────────────────────────────────────────────────────


class ProductType(StrEnum):
    SERVICE = "service"
    TRAINING = "training"
    LICENSE = "license"


class ProductStatus(StrEnum):
    AVAILABLE = "available"
    BETA = "beta"
    COMING_SOON = "coming_soon"
    RETIRED = "retired"


@dataclass(frozen=True, slots=True)
class Product:
    slug: str
    type: ProductType
    title: str
    description_md: str
    price_cents: int  # 0 for service-type products
    currency: str  # ISO 4217, e.g. "USD"
    duration_label: str  # human-readable, e.g. "1 year" or "40 hours"
    features: tuple[str, ...]
    category: str  # "Services" | "Training Material" | "Licenses"
    subcategory: str | None = None
    image_url: str = ""
    popular: bool = False
    status: ProductStatus = ProductStatus.AVAILABLE
    stripe_price_id: str | None = None  # required for training/license
    linked_learning_path_slug: str | None = None  # training products only

    def __post_init__(self) -> None:
        if self.type in (ProductType.TRAINING, ProductType.LICENSE) and not self.stripe_price_id:
            raise ValueError(f"product {self.slug}: {self.type.value} requires stripe_price_id")
        # Services route to lead capture — a non-zero price is allowed
        # because the UI shows it informationally, we just never charge.

    @property
    def is_purchasable(self) -> bool:
        """``service``-type products aren't purchasable — they route to
        an Ask. Everything else is purchasable only when AVAILABLE / BETA."""
        if self.type == ProductType.SERVICE:
            return False
        return self.status in (ProductStatus.AVAILABLE, ProductStatus.BETA)

    def assert_checkoutable(self) -> None:
        if self.type == ProductType.SERVICE:
            raise InvalidProductForCheckoutError(
                f"product {self.slug} is a service — use lead capture instead"
            )
        if not self.is_purchasable:
            raise InvalidProductForCheckoutError(
                f"product {self.slug} is not purchasable (status={self.status.value})"
            )


# ── Order ────────────────────────────────────────────────────────────


class OrderStatus(StrEnum):
    PENDING = "pending"
    PAID = "paid"
    REFUNDED = "refunded"
    FAILED = "failed"


_ALLOWED_ORDER_TRANSITIONS: dict[OrderStatus, frozenset[OrderStatus]] = {
    OrderStatus.PENDING: frozenset({OrderStatus.PAID, OrderStatus.FAILED}),
    OrderStatus.PAID: frozenset({OrderStatus.REFUNDED}),
    OrderStatus.REFUNDED: frozenset(),
    OrderStatus.FAILED: frozenset(),
}


@dataclass(slots=True)
class Order:
    id: UUID
    user_id: UUID
    product_slug: str
    amount_cents: int
    currency: str
    stripe_checkout_session_id: str
    stripe_payment_intent_id: str | None
    status: OrderStatus
    created_at: datetime
    paid_at: datetime | None = None

    def mark_paid(
        self,
        *,
        payment_intent_id: str,
        now: datetime | None = None,
    ) -> None:
        self._transition_to(OrderStatus.PAID)
        self.stripe_payment_intent_id = payment_intent_id
        self.paid_at = now or datetime.now(tz=UTC)

    def mark_failed(self) -> None:
        self._transition_to(OrderStatus.FAILED)

    def mark_refunded(self) -> None:
        self._transition_to(OrderStatus.REFUNDED)

    def _transition_to(self, target: OrderStatus) -> None:
        if target not in _ALLOWED_ORDER_TRANSITIONS[self.status]:
            raise OrderStateTransitionError(
                f"cannot transition order {self.id} from {self.status.value} to {target.value}"
            )
        self.status = target

    @property
    def is_paid(self) -> bool:
        return self.status is OrderStatus.PAID and self.paid_at is not None


def new_order(
    *,
    user_id: UUID,
    product: Product,
    stripe_checkout_session_id: str,
    now: datetime | None = None,
) -> Order:
    product.assert_checkoutable()
    return Order(
        id=uuid.uuid4(),
        user_id=user_id,
        product_slug=product.slug,
        amount_cents=product.price_cents,
        currency=product.currency,
        stripe_checkout_session_id=stripe_checkout_session_id,
        stripe_payment_intent_id=None,
        status=OrderStatus.PENDING,
        created_at=now or datetime.now(tz=UTC),
    )


# ── LicenseKey ───────────────────────────────────────────────────────


@dataclass(slots=True)
class LicenseKey:
    """The persisted form stores ``key_hash`` only; ``plaintext_key`` is
    set in-memory once on issuance and emailed/returned to the user,
    then dropped. Verification is done by hashing the user-supplied
    key + comparing to ``key_hash``."""

    id: UUID
    order_id: UUID
    user_id: UUID
    product_slug: str
    key_hash: str  # SHA-256 of the plaintext (we don't need bcrypt for this)
    issued_at: datetime
    expires_at: datetime | None = None
    revoked_at: datetime | None = None
    plaintext_key: str | None = None  # set once; cleared before persistence

    @property
    def is_active(self) -> bool:
        if self.revoked_at is not None:
            return False
        if self.expires_at is None:
            return True
        return self.expires_at > datetime.now(tz=UTC)

    def revoke(self, now: datetime | None = None) -> None:
        if self.revoked_at is not None:
            raise LicenseAlreadyRevokedError(f"license {self.id} already revoked")
        self.revoked_at = now or datetime.now(tz=UTC)


def new_license_key(
    *,
    order: Order,
    user_id: UUID,
    product_slug: str,
    plaintext: str,
    key_hash: str,
    expires_at: datetime | None = None,
    now: datetime | None = None,
) -> LicenseKey:
    return LicenseKey(
        id=uuid.uuid4(),
        order_id=order.id,
        user_id=user_id,
        product_slug=product_slug,
        key_hash=key_hash,
        issued_at=now or datetime.now(tz=UTC),
        expires_at=expires_at,
        plaintext_key=plaintext,
    )


# ── WebhookEvent (idempotency) ───────────────────────────────────────


@dataclass(frozen=True, slots=True)
class WebhookEvent:
    """Per-Stripe-event-id record. ``INSERT … ON CONFLICT DO NOTHING`` is
    the contract: if the row already exists, the webhook was already
    handled and we treat it as success."""

    stripe_event_id: str
    type: str  # e.g. "checkout.session.completed"
    payload: dict[str, object] = field(default_factory=dict)
    processed_at: datetime = field(default_factory=lambda: datetime.now(tz=UTC))


def new_webhook_event(
    *,
    stripe_event_id: str,
    type: str,
    payload: dict[str, object] | None = None,
    now: datetime | None = None,
) -> WebhookEvent:
    return WebhookEvent(
        stripe_event_id=stripe_event_id,
        type=type,
        payload=payload or {},
        processed_at=now or datetime.now(tz=UTC),
    )
