"""Tests for marketplace domain entities + state machines."""

from __future__ import annotations

import uuid
from datetime import UTC, datetime, timedelta

import pytest

from cyberdyne_backend.domain.marketplace import (
    InvalidProductForCheckoutError,
    LicenseAlreadyRevokedError,
    OrderStateTransitionError,
    OrderStatus,
    Product,
    ProductStatus,
    ProductType,
    new_license_key,
    new_order,
)


def _service(slug: str = "svc", status: ProductStatus = ProductStatus.AVAILABLE) -> Product:
    return Product(
        slug=slug,
        type=ProductType.SERVICE,
        title="Service",
        description_md="",
        price_cents=0,
        currency="USD",
        duration_label="",
        features=(),
        category="Services",
        status=status,
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


def _license() -> Product:
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


class TestProductInvariants:
    def test_training_requires_stripe_price_id(self) -> None:
        with pytest.raises(ValueError):
            Product(
                slug="bad",
                type=ProductType.TRAINING,
                title="T",
                description_md="",
                price_cents=100,
                currency="USD",
                duration_label="",
                features=(),
                category="Training Material",
            )

    def test_license_requires_stripe_price_id(self) -> None:
        with pytest.raises(ValueError):
            Product(
                slug="bad",
                type=ProductType.LICENSE,
                title="L",
                description_md="",
                price_cents=100,
                currency="USD",
                duration_label="",
                features=(),
                category="Licenses",
            )

    def test_service_does_not_require_stripe_price_id(self) -> None:
        # Should not raise.
        _service()

    def test_service_is_not_purchasable(self) -> None:
        assert not _service().is_purchasable

    def test_training_is_purchasable_when_available(self) -> None:
        assert _training().is_purchasable

    def test_coming_soon_not_purchasable(self) -> None:
        coming = Product(
            slug="cs",
            type=ProductType.LICENSE,
            title="L",
            description_md="",
            price_cents=100,
            currency="USD",
            duration_label="",
            features=(),
            category="Licenses",
            stripe_price_id="x",
            status=ProductStatus.COMING_SOON,
        )
        assert not coming.is_purchasable

    def test_assert_checkoutable_service_raises(self) -> None:
        with pytest.raises(InvalidProductForCheckoutError):
            _service().assert_checkoutable()

    def test_assert_checkoutable_unavailable_raises(self) -> None:
        retired = Product(
            slug="r",
            type=ProductType.LICENSE,
            title="L",
            description_md="",
            price_cents=100,
            currency="USD",
            duration_label="",
            features=(),
            category="Licenses",
            stripe_price_id="x",
            status=ProductStatus.RETIRED,
        )
        with pytest.raises(InvalidProductForCheckoutError):
            retired.assert_checkoutable()


class TestOrderStateMachine:
    def test_new_order_starts_pending(self) -> None:
        order = new_order(
            user_id=uuid.uuid4(),
            product=_training(),
            stripe_checkout_session_id="cs_test_1",
        )
        assert order.status is OrderStatus.PENDING
        assert order.paid_at is None

    def test_new_order_rejects_service_product(self) -> None:
        with pytest.raises(InvalidProductForCheckoutError):
            new_order(
                user_id=uuid.uuid4(),
                product=_service(),
                stripe_checkout_session_id="cs_x",
            )

    def test_pending_to_paid(self) -> None:
        order = new_order(
            user_id=uuid.uuid4(),
            product=_license(),
            stripe_checkout_session_id="cs_2",
        )
        order.mark_paid(payment_intent_id="pi_abc")
        assert order.status is OrderStatus.PAID
        assert order.is_paid
        assert order.stripe_payment_intent_id == "pi_abc"

    def test_paid_to_refunded(self) -> None:
        order = new_order(
            user_id=uuid.uuid4(),
            product=_license(),
            stripe_checkout_session_id="cs_3",
        )
        order.mark_paid(payment_intent_id="pi_abc")
        order.mark_refunded()
        assert order.status is OrderStatus.REFUNDED

    def test_pending_to_failed(self) -> None:
        order = new_order(
            user_id=uuid.uuid4(),
            product=_license(),
            stripe_checkout_session_id="cs_4",
        )
        order.mark_failed()
        assert order.status is OrderStatus.FAILED

    def test_cannot_refund_pending(self) -> None:
        order = new_order(
            user_id=uuid.uuid4(),
            product=_license(),
            stripe_checkout_session_id="cs_5",
        )
        with pytest.raises(OrderStateTransitionError):
            order.mark_refunded()

    def test_cannot_pay_twice(self) -> None:
        order = new_order(
            user_id=uuid.uuid4(),
            product=_license(),
            stripe_checkout_session_id="cs_6",
        )
        order.mark_paid(payment_intent_id="pi_abc")
        with pytest.raises(OrderStateTransitionError):
            order.mark_paid(payment_intent_id="pi_xyz")


class TestLicenseKey:
    def test_active_when_not_revoked_and_not_expired(self) -> None:
        order = new_order(
            user_id=uuid.uuid4(),
            product=_license(),
            stripe_checkout_session_id="cs_l1",
        )
        lic = new_license_key(
            order=order,
            user_id=order.user_id,
            product_slug="lic",
            plaintext="ABCDE-12345-FGHIJ-67890-KLMNO",
            key_hash="h",
            expires_at=datetime.now(tz=UTC) + timedelta(days=10),
        )
        assert lic.is_active

    def test_inactive_when_expired(self) -> None:
        order = new_order(
            user_id=uuid.uuid4(),
            product=_license(),
            stripe_checkout_session_id="cs_l2",
        )
        lic = new_license_key(
            order=order,
            user_id=order.user_id,
            product_slug="lic",
            plaintext="X",
            key_hash="h",
            expires_at=datetime.now(tz=UTC) - timedelta(days=1),
        )
        assert not lic.is_active

    def test_revoke_marks_inactive(self) -> None:
        order = new_order(
            user_id=uuid.uuid4(),
            product=_license(),
            stripe_checkout_session_id="cs_l3",
        )
        lic = new_license_key(
            order=order,
            user_id=order.user_id,
            product_slug="lic",
            plaintext="X",
            key_hash="h",
        )
        lic.revoke()
        assert not lic.is_active
        assert lic.revoked_at is not None

    def test_double_revoke_raises(self) -> None:
        order = new_order(
            user_id=uuid.uuid4(),
            product=_license(),
            stripe_checkout_session_id="cs_l4",
        )
        lic = new_license_key(
            order=order,
            user_id=order.user_id,
            product_slug="lic",
            plaintext="X",
            key_hash="h",
        )
        lic.revoke()
        with pytest.raises(LicenseAlreadyRevokedError):
            lic.revoke()
