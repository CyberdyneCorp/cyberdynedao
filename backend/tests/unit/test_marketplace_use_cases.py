"""Tests for marketplace use cases — checkout + webhook idempotency +
training auto-enrollment + license issuance + refund."""

from __future__ import annotations

import json
import uuid
from datetime import UTC, datetime, timedelta
from uuid import UUID

import pytest

from cyberdyne_backend.adapters.outbound.stripe.webhook_verifier import (
    DEFAULT_TOLERANCE_SECONDS,
    MockStripeWebhookVerifier,
    StripeWebhookVerifier,
)
from cyberdyne_backend.application.marketplace import (
    CreateCheckoutSession,
    HandleStripeWebhook,
    ListMyOrders,
    RevokeLicense,
)
from cyberdyne_backend.domain.learning import Enrollment, LearningModule, LearningPath
from cyberdyne_backend.domain.marketplace import (
    CheckoutSession,
    DuplicateWebhookError,
    InvalidProductForCheckoutError,
    LicenseKey,
    Order,
    OrderStatus,
    Product,
    ProductNotFoundError,
    ProductType,
    StripeSignatureError,
    StripeWebhookEvent,
    WebhookEvent,
    new_order,
)

# ── Fakes ────────────────────────────────────────────────────────────


class _FakeMarketplaceRepo:
    def __init__(self) -> None:
        self.products: dict[str, Product] = {}
        self.orders: dict[UUID, Order] = {}
        self.licenses: dict[UUID, LicenseKey] = {}
        self.events: dict[str, WebhookEvent] = {}

    async def list_products(self, *, category=None, product_type=None):
        return list(self.products.values())

    async def get_product(self, slug: str) -> Product:
        if slug not in self.products:
            raise ProductNotFoundError(slug)
        return self.products[slug]

    async def save_order(self, order: Order) -> None:
        self.orders[order.id] = order

    async def get_order(self, order_id: UUID) -> Order:
        return self.orders[order_id]

    async def get_order_by_session_id(self, session_id: str) -> Order | None:
        for o in self.orders.values():
            if o.stripe_checkout_session_id == session_id:
                return o
        return None

    async def get_order_by_payment_intent(self, payment_intent_id: str) -> Order | None:
        for o in self.orders.values():
            if o.stripe_payment_intent_id == payment_intent_id:
                return o
        return None

    async def list_orders_for_user(self, user_id: UUID) -> list[Order]:
        return [o for o in self.orders.values() if o.user_id == user_id]

    async def save_license(self, lic: LicenseKey) -> None:
        self.licenses[lic.id] = lic

    async def get_license(self, license_id: UUID) -> LicenseKey:
        return self.licenses[license_id]

    async def list_licenses_for_user(self, user_id: UUID) -> list[LicenseKey]:
        return [lic for lic in self.licenses.values() if lic.user_id == user_id]

    async def record_webhook_event(self, event: WebhookEvent) -> bool:
        if event.stripe_event_id in self.events:
            return False
        self.events[event.stripe_event_id] = event
        return True


class _FakeLearningRepo:
    def __init__(self) -> None:
        self.enrollments: list[Enrollment] = []

    async def list_modules(self) -> list[LearningModule]:
        return []

    async def list_paths(self) -> list[LearningPath]:
        return []

    async def get_path(self, slug: str) -> LearningPath:
        raise NotImplementedError

    async def upsert_enrollment(self, enrollment: Enrollment) -> Enrollment:
        self.enrollments.append(enrollment)
        return enrollment

    async def list_enrollments_for_user(self, user_id):
        return []

    async def upsert_progress(self, progress):
        return progress

    async def get_progress_map_for_user(self, user_id):
        return {}

    async def save_certificate(self, certificate):
        pass

    async def get_certificate_for_user_and_path(self, user_id, path_slug):
        return None


class _RecordingNotifier:
    def __init__(self) -> None:
        self.sent: list[dict[str, object]] = []

    async def send_license_email(
        self, *, to_email: str, product_title: str, plaintext_key: str, expires_at_iso: str | None
    ) -> None:
        self.sent.append(
            {
                "to": to_email,
                "product": product_title,
                "key": plaintext_key,
                "expires": expires_at_iso,
            }
        )


class _FakeCheckout:
    def __init__(self) -> None:
        self.calls: list[Product] = []

    async def create_checkout_session(
        self, *, product, user_id, success_url, cancel_url, client_reference_id=None
    ):
        self.calls.append(product)
        return CheckoutSession(
            session_id=f"cs_test_{product.slug}",
            url=f"https://stripe.test/{product.slug}",
        )


def _training(stripe_price_id: str = "price_x") -> Product:
    return Product(
        slug="train",
        type=ProductType.TRAINING,
        title="Course",
        description_md="",
        price_cents=29900,
        currency="USD",
        duration_label="40h",
        features=(),
        category="Training Material",
        stripe_price_id=stripe_price_id,
        linked_learning_path_slug="blockchain-developer",
    )


def _license_product() -> Product:
    return Product(
        slug="lic",
        type=ProductType.LICENSE,
        title="License",
        description_md="",
        price_cents=249900,
        currency="USD",
        duration_label="1 year",
        features=(),
        category="Licenses",
        stripe_price_id="price_y",
    )


def _service_product() -> Product:
    return Product(
        slug="svc",
        type=ProductType.SERVICE,
        title="Service",
        description_md="",
        price_cents=0,
        currency="USD",
        duration_label="",
        features=(),
        category="Services",
    )


# ── CreateCheckoutSession ────────────────────────────────────────────


class TestCreateCheckoutSession:
    async def test_creates_session_and_pending_order(self) -> None:
        repo = _FakeMarketplaceRepo()
        repo.products["train"] = _training()
        checkout = _FakeCheckout()
        uc = CreateCheckoutSession(repo=repo, checkout=checkout, success_url="s", cancel_url="c")
        user_id = uuid.uuid4()
        session = await uc.execute(user_id=user_id, product_slug="train")
        assert session.session_id.startswith("cs_test_")
        # Pending order persisted with that session id.
        assert len(repo.orders) == 1
        order = next(iter(repo.orders.values()))
        assert order.status is OrderStatus.PENDING
        assert order.user_id == user_id

    async def test_rejects_service_product(self) -> None:
        repo = _FakeMarketplaceRepo()
        repo.products["svc"] = _service_product()
        uc = CreateCheckoutSession(
            repo=repo, checkout=_FakeCheckout(), success_url="s", cancel_url="c"
        )
        with pytest.raises(InvalidProductForCheckoutError):
            await uc.execute(user_id=uuid.uuid4(), product_slug="svc")

    async def test_missing_product_raises(self) -> None:
        repo = _FakeMarketplaceRepo()
        uc = CreateCheckoutSession(
            repo=repo, checkout=_FakeCheckout(), success_url="s", cancel_url="c"
        )
        with pytest.raises(ProductNotFoundError):
            await uc.execute(user_id=uuid.uuid4(), product_slug="nope")


# ── HandleStripeWebhook ──────────────────────────────────────────────


def _checkout_completed_event(
    *, event_id: str, session_id: str, payment_intent: str = "pi_x", customer_email: str = "u@x.io"
) -> StripeWebhookEvent:
    return StripeWebhookEvent(
        stripe_event_id=event_id,
        type="checkout.session.completed",
        payload={
            "id": event_id,
            "type": "checkout.session.completed",
            "data": {
                "object": {
                    "id": session_id,
                    "payment_intent": payment_intent,
                    "customer_email": customer_email,
                }
            },
        },
    )


def _refund_event(*, event_id: str, payment_intent: str) -> StripeWebhookEvent:
    return StripeWebhookEvent(
        stripe_event_id=event_id,
        type="charge.refunded",
        payload={
            "id": event_id,
            "type": "charge.refunded",
            "data": {"object": {"payment_intent": payment_intent}},
        },
    )


class TestHandleStripeWebhook:
    async def test_training_purchase_auto_enrolls(self) -> None:
        market = _FakeMarketplaceRepo()
        learning = _FakeLearningRepo()
        notifier = _RecordingNotifier()
        market.products["train"] = _training()
        user_id = uuid.uuid4()
        order = new_order(
            user_id=user_id,
            product=market.products["train"],
            stripe_checkout_session_id="cs_train_1",
        )
        market.orders[order.id] = order

        uc = HandleStripeWebhook(marketplace=market, learning=learning, email_notifier=notifier)
        await uc.execute(_checkout_completed_event(event_id="evt_1", session_id="cs_train_1"))
        assert order.status is OrderStatus.PAID
        assert len(learning.enrollments) == 1
        assert learning.enrollments[0].path_slug == "blockchain-developer"
        # No license email for training products.
        assert notifier.sent == []

    async def test_license_purchase_issues_and_emails(self) -> None:
        market = _FakeMarketplaceRepo()
        learning = _FakeLearningRepo()
        notifier = _RecordingNotifier()
        market.products["lic"] = _license_product()
        user_id = uuid.uuid4()
        order = new_order(
            user_id=user_id,
            product=market.products["lic"],
            stripe_checkout_session_id="cs_lic_1",
        )
        market.orders[order.id] = order

        uc = HandleStripeWebhook(marketplace=market, learning=learning, email_notifier=notifier)
        await uc.execute(
            _checkout_completed_event(
                event_id="evt_lic_1", session_id="cs_lic_1", customer_email="alice@x.io"
            )
        )
        assert order.status is OrderStatus.PAID
        assert len(market.licenses) == 1
        sent = notifier.sent[0]
        assert sent["to"] == "alice@x.io"
        assert sent["product"] == "License"

    async def test_idempotent_on_duplicate_event_id(self) -> None:
        market = _FakeMarketplaceRepo()
        learning = _FakeLearningRepo()
        notifier = _RecordingNotifier()
        market.products["lic"] = _license_product()
        order = new_order(
            user_id=uuid.uuid4(),
            product=market.products["lic"],
            stripe_checkout_session_id="cs_idem",
        )
        market.orders[order.id] = order

        uc = HandleStripeWebhook(marketplace=market, learning=learning, email_notifier=notifier)
        evt = _checkout_completed_event(
            event_id="evt_idem", session_id="cs_idem", customer_email="bob@x.io"
        )
        await uc.execute(evt)
        # Second delivery raises DuplicateWebhookError and is a no-op.
        with pytest.raises(DuplicateWebhookError):
            await uc.execute(evt)
        assert len(market.licenses) == 1
        assert len(notifier.sent) == 1

    async def test_refund_marks_order_and_revokes_license(self) -> None:
        market = _FakeMarketplaceRepo()
        learning = _FakeLearningRepo()
        notifier = _RecordingNotifier()
        market.products["lic"] = _license_product()
        order = new_order(
            user_id=uuid.uuid4(),
            product=market.products["lic"],
            stripe_checkout_session_id="cs_refund",
        )
        market.orders[order.id] = order
        uc = HandleStripeWebhook(marketplace=market, learning=learning, email_notifier=notifier)
        await uc.execute(
            _checkout_completed_event(
                event_id="evt_pay", session_id="cs_refund", payment_intent="pi_ref"
            )
        )
        # Now refund.
        await uc.execute(_refund_event(event_id="evt_refund", payment_intent="pi_ref"))
        assert order.status is OrderStatus.REFUNDED
        lic = next(iter(market.licenses.values()))
        assert lic.revoked_at is not None

    async def test_unknown_session_logged_and_no_op(self) -> None:
        market = _FakeMarketplaceRepo()
        uc = HandleStripeWebhook(
            marketplace=market,
            learning=_FakeLearningRepo(),
            email_notifier=_RecordingNotifier(),
        )
        # No matching order → no crash, no side-effects.
        await uc.execute(_checkout_completed_event(event_id="evt_orphan", session_id="cs_orphan"))
        assert market.orders == {}


# ── RevokeLicense + ListMyOrders ─────────────────────────────────────


class TestAdminAndUserReads:
    async def test_revoke_marks_license_revoked(self) -> None:
        market = _FakeMarketplaceRepo()
        market.products["lic"] = _license_product()
        order = new_order(
            user_id=uuid.uuid4(),
            product=market.products["lic"],
            stripe_checkout_session_id="cs_l",
        )
        market.orders[order.id] = order
        from cyberdyne_backend.domain.marketplace import new_license_key

        lic = new_license_key(
            order=order,
            user_id=order.user_id,
            product_slug="lic",
            plaintext="X",
            key_hash="h",
        )
        market.licenses[lic.id] = lic
        revoked = await RevokeLicense(repo=market).execute(lic.id)
        assert revoked.revoked_at is not None

    async def test_list_my_orders_filters_by_user(self) -> None:
        market = _FakeMarketplaceRepo()
        market.products["lic"] = _license_product()
        user_id = uuid.uuid4()
        order_mine = new_order(
            user_id=user_id,
            product=market.products["lic"],
            stripe_checkout_session_id="cs_a",
        )
        order_other = new_order(
            user_id=uuid.uuid4(),
            product=market.products["lic"],
            stripe_checkout_session_id="cs_b",
        )
        market.orders[order_mine.id] = order_mine
        market.orders[order_other.id] = order_other
        results = await ListMyOrders(repo=market).execute(user_id)
        assert [o.id for o in results] == [order_mine.id]


# ── StripeWebhookVerifier ────────────────────────────────────────────


class TestWebhookVerifier:
    def _sign(self, *, secret: str, ts: int, body: bytes) -> str:
        import hashlib
        import hmac

        payload = f"{ts}.".encode() + body
        sig = hmac.new(secret.encode(), payload, hashlib.sha256).hexdigest()
        return f"t={ts},v1={sig}"

    def test_verifies_well_formed_event(self) -> None:
        secret = "whsec_test"
        now_ts = 1_700_000_000
        body = json.dumps({"id": "evt_1", "type": "checkout.session.completed"}).encode()
        header = self._sign(secret=secret, ts=now_ts, body=body)
        v = StripeWebhookVerifier(signing_secret=secret, now=float(now_ts))
        event = v.verify(raw_body=body, signature_header=header)
        assert event.stripe_event_id == "evt_1"
        assert event.type == "checkout.session.completed"

    def test_rejects_bad_signature(self) -> None:
        v = StripeWebhookVerifier(signing_secret="whsec_test", now=1_700_000_000.0)
        body = b'{"id":"e","type":"t"}'
        with pytest.raises(StripeSignatureError):
            v.verify(raw_body=body, signature_header="t=1700000000,v1=00")

    def test_rejects_old_timestamp(self) -> None:
        secret = "whsec_test"
        ts = 1_700_000_000
        body = b'{"id":"e","type":"t"}'
        header = self._sign(secret=secret, ts=ts, body=body)
        v = StripeWebhookVerifier(
            signing_secret=secret,
            now=float(ts + DEFAULT_TOLERANCE_SECONDS + 10),
        )
        with pytest.raises(StripeSignatureError):
            v.verify(raw_body=body, signature_header=header)

    def test_malformed_header_rejected(self) -> None:
        v = StripeWebhookVerifier(signing_secret="whsec_test", now=1_700_000_000.0)
        with pytest.raises(StripeSignatureError):
            v.verify(raw_body=b"{}", signature_header="")

    def test_missing_id_or_type_rejected(self) -> None:
        secret = "whsec_test"
        ts = 1_700_000_000
        body = b"{}"
        header = self._sign(secret=secret, ts=ts, body=body)
        v = StripeWebhookVerifier(signing_secret=secret, now=float(ts))
        with pytest.raises(StripeSignatureError):
            v.verify(raw_body=body, signature_header=header)

    def test_mock_verifier_trusts_everything(self) -> None:
        v = MockStripeWebhookVerifier()
        body = json.dumps({"id": "evt_m", "type": "checkout.session.completed"}).encode()
        evt = v.verify(raw_body=body, signature_header="ignored")
        assert evt.stripe_event_id == "evt_m"


# Suppress unused-import warning — timedelta kept for future
# expiry-pinned tests in the same module.
_ = timedelta(days=1)
_ = datetime.now(tz=UTC)
