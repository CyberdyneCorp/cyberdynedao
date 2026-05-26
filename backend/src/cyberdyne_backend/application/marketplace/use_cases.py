"""Marketplace use cases.

The Stripe webhook dispatcher is the centerpiece — it has to be
idempotent, fail-loud on signature mismatch, and never double-fulfill.
The fulfillment side then bridges to other contexts (Learning for
training enrollment auto-grant; LicenseEmailNotifier for license keys).
"""

from __future__ import annotations

import logging
import secrets
from dataclasses import dataclass
from datetime import UTC, datetime, timedelta
from hashlib import sha256
from typing import cast
from uuid import UUID

from cyberdyne_backend.domain.learning import LearningRepository, new_enrollment
from cyberdyne_backend.domain.marketplace import (
    CheckoutSession,
    DuplicateWebhookError,
    LicenseEmailNotifierPort,
    LicenseKey,
    MarketplaceRepository,
    Order,
    Product,
    ProductType,
    StripeCheckoutPort,
    StripeWebhookEvent,
    new_license_key,
    new_order,
    new_webhook_event,
)

logger = logging.getLogger("cyberdyne_backend.marketplace")


@dataclass(slots=True)
class ListProducts:
    repo: MarketplaceRepository

    async def execute(
        self, *, category: str | None = None, product_type: str | None = None
    ) -> list[Product]:
        return await self.repo.list_products(category=category, product_type=product_type)


@dataclass(slots=True)
class GetProduct:
    repo: MarketplaceRepository

    async def execute(self, slug: str) -> Product:
        return await self.repo.get_product(slug)


@dataclass(slots=True)
class CreateCheckoutSession:
    repo: MarketplaceRepository
    checkout: StripeCheckoutPort
    success_url: str
    cancel_url: str

    async def execute(self, *, user_id: UUID, product_slug: str) -> CheckoutSession:
        product = await self.repo.get_product(product_slug)
        product.assert_checkoutable()
        session = await self.checkout.create_checkout_session(
            product=product,
            user_id=user_id,
            success_url=self.success_url,
            cancel_url=self.cancel_url,
            client_reference_id=str(user_id),
        )
        # Persist a pending order keyed by the session id so the webhook
        # can find it by session_id when checkout.session.completed fires.
        order = new_order(
            user_id=user_id,
            product=product,
            stripe_checkout_session_id=session.session_id,
        )
        await self.repo.save_order(order)
        return session


@dataclass(slots=True)
class ListMyOrders:
    repo: MarketplaceRepository

    async def execute(self, user_id: UUID) -> list[Order]:
        return await self.repo.list_orders_for_user(user_id)


@dataclass(slots=True)
class ListMyLicenses:
    repo: MarketplaceRepository

    async def execute(self, user_id: UUID) -> list[LicenseKey]:
        return await self.repo.list_licenses_for_user(user_id)


@dataclass(slots=True)
class RevokeLicense:
    repo: MarketplaceRepository

    async def execute(self, license_id: UUID) -> LicenseKey:
        lic = await self.repo.get_license(license_id)
        lic.revoke()
        await self.repo.save_license(lic)
        return lic


# ── Webhook dispatcher ──────────────────────────────────────────────


def _gen_license_plaintext() -> str:
    """A 5-group dash-separated 25-char string. Same shape as the
    market's typical license format — easy to type, no ambiguous chars."""
    alphabet = "ABCDEFGHJKLMNPQRSTUVWXYZ23456789"  # no O/0, I/1
    groups: list[str] = []
    for _ in range(5):
        groups.append("".join(secrets.choice(alphabet) for _ in range(5)))
    return "-".join(groups)


def _hash_license(plaintext: str) -> str:
    return sha256(plaintext.encode("utf-8")).hexdigest()


@dataclass(slots=True)
class HandleStripeWebhook:
    """Dispatches a verified Stripe webhook event.

    Idempotent on ``event.stripe_event_id`` — if the same event id is
    re-delivered (Stripe normal retry behaviour), we short-circuit and
    return without doing the side-effects twice.

    Bridges to other contexts:
    - ``checkout.session.completed`` on a training product →
      auto-enrolls the user via ``LearningRepository``.
    - ``checkout.session.completed`` on a license product → issues a
      ``LicenseKey`` and emails it.
    - ``charge.refunded`` → marks the order refunded and revokes any
      attached license.
    """

    marketplace: MarketplaceRepository
    learning: LearningRepository
    email_notifier: LicenseEmailNotifierPort
    license_validity_days: int = 365

    async def execute(self, event: StripeWebhookEvent) -> None:
        was_new = await self.marketplace.record_webhook_event(
            new_webhook_event(
                stripe_event_id=event.stripe_event_id,
                type=event.type,
                payload=event.payload,
            )
        )
        if not was_new:
            logger.info(
                "stripe webhook %s (%s) already processed — skipping",
                event.stripe_event_id,
                event.type,
            )
            raise DuplicateWebhookError(event.stripe_event_id)

        if event.type == "checkout.session.completed":
            await self._handle_checkout_completed(event.payload)
        elif event.type in ("charge.refunded", "checkout.session.async_payment_failed"):
            await self._handle_refund_or_failure(event.payload, event.type)
        else:
            logger.info("stripe webhook %s ignored (type=%s)", event.stripe_event_id, event.type)

    async def _handle_checkout_completed(self, payload: dict[str, object]) -> None:
        data = cast(dict[str, object], payload.get("data") or {})
        session = cast(dict[str, object], data.get("object") or {})
        session_id = cast(str | None, session.get("id"))
        payment_intent_id = cast(str | None, session.get("payment_intent"))
        if not session_id:
            logger.warning("checkout.session.completed missing session id; payload=%r", payload)
            return
        order = await self.marketplace.get_order_by_session_id(session_id)
        if order is None:
            logger.warning("checkout.session.completed for unknown session %s", session_id)
            return
        order.mark_paid(payment_intent_id=payment_intent_id or "")
        await self.marketplace.save_order(order)
        product = await self.marketplace.get_product(order.product_slug)
        await self._fulfill(order=order, product=product, session=session)

    async def _fulfill(
        self,
        *,
        order: Order,
        product: Product,
        session: dict[str, object],
    ) -> None:
        if product.type is ProductType.TRAINING:
            if product.linked_learning_path_slug is None:
                logger.warning(
                    "training product %s has no linked_learning_path_slug — skipping enrollment",
                    product.slug,
                )
                return
            enrollment = new_enrollment(
                user_id=order.user_id,
                path_slug=product.linked_learning_path_slug,
            )
            await self.learning.upsert_enrollment(enrollment)
            logger.info(
                "auto-enrolled user %s in path %s after order %s",
                order.user_id,
                product.linked_learning_path_slug,
                order.id,
            )
        elif product.type is ProductType.LICENSE:
            plaintext = _gen_license_plaintext()
            expires = datetime.now(tz=UTC) + timedelta(days=self.license_validity_days)
            lic = new_license_key(
                order=order,
                user_id=order.user_id,
                product_slug=product.slug,
                plaintext=plaintext,
                key_hash=_hash_license(plaintext),
                expires_at=expires,
            )
            await self.marketplace.save_license(lic)
            customer_email = cast(str | None, session.get("customer_email")) or cast(
                str | None,
                cast(dict[str, object], session.get("customer_details") or {}).get("email"),
            )
            if customer_email:
                await self.email_notifier.send_license_email(
                    to_email=customer_email,
                    product_title=product.title,
                    plaintext_key=plaintext,
                    expires_at_iso=expires.isoformat(),
                )
            else:
                logger.warning(
                    "license issued for order %s but no customer email in webhook payload",
                    order.id,
                )

    async def _handle_refund_or_failure(self, payload: dict[str, object], event_type: str) -> None:
        data = cast(dict[str, object], payload.get("data") or {})
        obj = cast(dict[str, object], data.get("object") or {})
        payment_intent_id = cast(str | None, obj.get("payment_intent") or obj.get("id"))
        if not payment_intent_id:
            return
        # Best-effort lookup: orders keyed by session_id; refunds give us
        # the payment_intent. We need a small detour through orders to find
        # the right one — the repository helper handles that lookup.
        order = await self.marketplace.get_order_by_payment_intent(payment_intent_id)
        if order is None:
            logger.warning("%s for unknown payment_intent %s", event_type, payment_intent_id)
            return
        if event_type == "charge.refunded":
            order.mark_refunded()
            # Revoke any license attached to the same order.
            for lic in await self.marketplace.list_licenses_for_user(order.user_id):
                if lic.order_id == order.id and lic.revoked_at is None:
                    lic.revoke()
                    await self.marketplace.save_license(lic)
        else:
            order.mark_failed()
        await self.marketplace.save_order(order)
