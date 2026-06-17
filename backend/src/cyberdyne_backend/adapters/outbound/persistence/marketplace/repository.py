"""SQLAlchemy adapter for ``MarketplaceRepository``."""

from __future__ import annotations

from uuid import UUID

from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert as pg_insert
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from cyberdyne_backend.adapters.outbound.persistence.marketplace.models import (
    LicenseKeyRow,
    OrderRow,
    ProductRow,
    StripeWebhookEventRow,
)
from cyberdyne_backend.adapters.outbound.persistence.marketplace.redaction import (
    redact_webhook_payload,
)
from cyberdyne_backend.domain.marketplace import (
    LicenseKey,
    Order,
    OrderNotFoundError,
    OrderStatus,
    Product,
    ProductNotFoundError,
    ProductStatus,
    ProductType,
    WebhookEvent,
)


def _row_to_product(row: ProductRow) -> Product:
    return Product(
        slug=row.slug,
        type=ProductType(row.type),
        title=row.title,
        description_md=row.description_md,
        price_cents=row.price_cents,
        currency=row.currency,
        duration_label=row.duration_label,
        features=tuple(row.features),
        category=row.category,
        subcategory=row.subcategory,
        image_url=row.image_url,
        popular=row.popular,
        status=ProductStatus(row.status),
        stripe_price_id=row.stripe_price_id,
        linked_learning_path_slug=row.linked_learning_path_slug,
    )


def _row_to_order(row: OrderRow) -> Order:
    return Order(
        id=row.id,
        user_id=row.user_id,
        product_slug=row.product_slug,
        amount_cents=row.amount_cents,
        currency=row.currency,
        stripe_checkout_session_id=row.stripe_checkout_session_id,
        stripe_payment_intent_id=row.stripe_payment_intent_id,
        status=OrderStatus(row.status),
        created_at=row.created_at,
        paid_at=row.paid_at,
    )


def _row_to_license(row: LicenseKeyRow) -> LicenseKey:
    return LicenseKey(
        id=row.id,
        order_id=row.order_id,
        user_id=row.user_id,
        product_slug=row.product_slug,
        key_hash=row.key_hash,
        issued_at=row.issued_at,
        expires_at=row.expires_at,
        revoked_at=row.revoked_at,
        plaintext_key=None,
    )


class SqlAlchemyMarketplaceRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    # ── Products ─────────────────────────────────────────────────────
    async def list_products(
        self,
        *,
        category: str | None = None,
        product_type: str | None = None,
    ) -> list[Product]:
        stmt = select(ProductRow)
        if category:
            stmt = stmt.where(ProductRow.category == category)
        if product_type:
            stmt = stmt.where(ProductRow.type == product_type)
        stmt = stmt.order_by(ProductRow.sort_order, ProductRow.slug)
        rows = (await self._session.execute(stmt)).scalars().all()
        return [_row_to_product(r) for r in rows]

    async def get_product(self, slug: str) -> Product:
        row = await self._session.get(ProductRow, slug)
        if row is None:
            raise ProductNotFoundError(f"no product with slug={slug!r}")
        return _row_to_product(row)

    # ── Orders ───────────────────────────────────────────────────────
    async def save_order(self, order: Order) -> None:
        existing = await self._session.get(OrderRow, order.id)
        if existing is None:
            self._session.add(
                OrderRow(
                    id=order.id,
                    user_id=order.user_id,
                    product_slug=order.product_slug,
                    amount_cents=order.amount_cents,
                    currency=order.currency,
                    stripe_checkout_session_id=order.stripe_checkout_session_id,
                    stripe_payment_intent_id=order.stripe_payment_intent_id,
                    status=order.status.value,
                    created_at=order.created_at,
                    paid_at=order.paid_at,
                )
            )
        else:
            existing.stripe_payment_intent_id = order.stripe_payment_intent_id
            existing.status = order.status.value
            existing.paid_at = order.paid_at
        await self._session.flush()

    async def get_order(self, order_id: UUID) -> Order:
        row = await self._session.get(OrderRow, order_id)
        if row is None:
            raise OrderNotFoundError(f"no order with id={order_id}")
        return _row_to_order(row)

    async def get_order_by_session_id(self, session_id: str) -> Order | None:
        row = (
            await self._session.execute(
                select(OrderRow).where(OrderRow.stripe_checkout_session_id == session_id)
            )
        ).scalar_one_or_none()
        return _row_to_order(row) if row else None

    async def get_order_by_payment_intent(self, payment_intent_id: str) -> Order | None:
        row = (
            await self._session.execute(
                select(OrderRow).where(OrderRow.stripe_payment_intent_id == payment_intent_id)
            )
        ).scalar_one_or_none()
        return _row_to_order(row) if row else None

    async def list_orders_for_user(self, user_id: UUID) -> list[Order]:
        rows = (
            (
                await self._session.execute(
                    select(OrderRow)
                    .where(OrderRow.user_id == user_id)
                    .order_by(OrderRow.created_at.desc())
                )
            )
            .scalars()
            .all()
        )
        return [_row_to_order(r) for r in rows]

    # ── Licenses ─────────────────────────────────────────────────────
    async def save_license(self, license_key: LicenseKey) -> None:
        existing = await self._session.get(LicenseKeyRow, license_key.id)
        if existing is None:
            self._session.add(
                LicenseKeyRow(
                    id=license_key.id,
                    order_id=license_key.order_id,
                    user_id=license_key.user_id,
                    product_slug=license_key.product_slug,
                    key_hash=license_key.key_hash,
                    issued_at=license_key.issued_at,
                    expires_at=license_key.expires_at,
                    revoked_at=license_key.revoked_at,
                )
            )
        else:
            existing.revoked_at = license_key.revoked_at
            existing.expires_at = license_key.expires_at
        await self._session.flush()

    async def get_license(self, license_id: UUID) -> LicenseKey:
        row = await self._session.get(LicenseKeyRow, license_id)
        if row is None:
            raise OrderNotFoundError(f"no license with id={license_id}")
        return _row_to_license(row)

    async def list_licenses_for_user(self, user_id: UUID) -> list[LicenseKey]:
        rows = (
            (
                await self._session.execute(
                    select(LicenseKeyRow)
                    .where(LicenseKeyRow.user_id == user_id)
                    .order_by(LicenseKeyRow.issued_at.desc())
                )
            )
            .scalars()
            .all()
        )
        return [_row_to_license(r) for r in rows]

    # ── Webhook idempotency ──────────────────────────────────────────
    async def record_webhook_event(self, event: WebhookEvent) -> bool:
        # On Postgres, ``ON CONFLICT DO NOTHING`` is the clean way. The
        # aiosqlite test backend doesn't support it via the pg-specific
        # construct, so we fall back to a try/insert/IntegrityError path.
        # The stored copy is audit/idempotency-only (fulfillment reads the
        # live verified event), so strip PII / card data before persisting.
        safe_payload = redact_webhook_payload(event.payload)
        dialect = self._session.bind.dialect.name if self._session.bind else ""
        if dialect == "postgresql":
            stmt = (
                pg_insert(StripeWebhookEventRow)
                .values(
                    stripe_event_id=event.stripe_event_id,
                    type=event.type,
                    payload=safe_payload,
                    processed_at=event.processed_at,
                )
                .on_conflict_do_nothing(index_elements=["stripe_event_id"])
            )
            result = await self._session.execute(stmt)
            # ``rowcount`` exists on the CursorResult of an INSERT — pg
            # driver populates it but the generic ``Result`` typing
            # doesn't expose it, hence the cast.
            return int(getattr(result, "rowcount", 0) or 0) == 1
        # Generic fallback (sqlite / others): probe then insert.
        existing = await self._session.get(StripeWebhookEventRow, event.stripe_event_id)
        if existing is not None:
            return False
        self._session.add(
            StripeWebhookEventRow(
                stripe_event_id=event.stripe_event_id,
                type=event.type,
                payload=safe_payload,
                processed_at=event.processed_at,
            )
        )
        try:
            await self._session.flush()
        except IntegrityError:
            await self._session.rollback()
            return False
        return True
