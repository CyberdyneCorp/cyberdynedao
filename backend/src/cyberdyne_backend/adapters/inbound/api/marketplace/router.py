"""Marketplace endpoints — public catalogue + auth'd checkout + Stripe
webhook receiver + user-scoped orders/licenses."""

from __future__ import annotations

import logging
from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, Header, HTTPException, Request, status

from cyberdyne_backend.adapters.inbound.api.marketplace.schemas import (
    CheckoutRequest,
    CheckoutResponse,
    LicenseKeyResponse,
    OrderResponse,
    ProductResponse,
)
from cyberdyne_backend.adapters.inbound.middleware.auth import (
    require_editor,
    require_principal,
)
from cyberdyne_backend.application.marketplace import (
    CreateCheckoutSession,
    HandleStripeWebhook,
    ListMyLicenses,
    ListMyOrders,
    ListProducts,
    RevokeLicense,
)
from cyberdyne_backend.domain.auth_identity import UserPrincipal
from cyberdyne_backend.domain.marketplace import (
    DuplicateWebhookError,
    InvalidProductForCheckoutError,
    LicenseAlreadyRevokedError,
    LicenseKey,
    Order,
    Product,
    ProductNotFoundError,
    StripeSignatureError,
    StripeWebhookVerifierPort,
)

logger = logging.getLogger("cyberdyne_backend.marketplace.router")

public_router = APIRouter(prefix="/api/v1/marketplace", tags=["marketplace"])
me_router = APIRouter(prefix="/api/v1/me", tags=["me"])
webhook_router = APIRouter(prefix="/api/v1", tags=["stripe-webhook"])
admin_router = APIRouter(prefix="/api/v1/admin/marketplace", tags=["marketplace-admin"])


# ── Dependency stubs (overridden in main.py) ─────────────────────────


async def get_list_products_uc() -> ListProducts:  # pragma: no cover
    raise NotImplementedError


async def get_create_checkout_uc() -> CreateCheckoutSession:  # pragma: no cover
    raise NotImplementedError


async def get_handle_webhook_uc() -> HandleStripeWebhook:  # pragma: no cover
    raise NotImplementedError


async def get_my_orders_uc() -> ListMyOrders:  # pragma: no cover
    raise NotImplementedError


async def get_my_licenses_uc() -> ListMyLicenses:  # pragma: no cover
    raise NotImplementedError


async def get_revoke_license_uc() -> RevokeLicense:  # pragma: no cover
    raise NotImplementedError


def get_webhook_verifier() -> StripeWebhookVerifierPort:  # pragma: no cover
    raise NotImplementedError


# ── Response builders ────────────────────────────────────────────────


def _product_response(p: Product) -> ProductResponse:
    return ProductResponse(
        slug=p.slug,
        type=p.type.value,
        title=p.title,
        description_md=p.description_md,
        price_cents=p.price_cents,
        currency=p.currency,
        duration_label=p.duration_label,
        features=list(p.features),
        category=p.category,
        subcategory=p.subcategory,
        image_url=p.image_url,
        popular=p.popular,
        status=p.status.value,
        is_purchasable=p.is_purchasable,
    )


def _order_response(o: Order) -> OrderResponse:
    return OrderResponse(
        id=o.id,
        product_slug=o.product_slug,
        amount_cents=o.amount_cents,
        currency=o.currency,
        status=o.status.value,
        created_at=o.created_at,
        paid_at=o.paid_at,
    )


def _license_response(lic: LicenseKey, *, include_plaintext: bool = False) -> LicenseKeyResponse:
    return LicenseKeyResponse(
        id=lic.id,
        product_slug=lic.product_slug,
        issued_at=lic.issued_at,
        expires_at=lic.expires_at,
        revoked_at=lic.revoked_at,
        is_active=lic.is_active,
        plaintext_key=lic.plaintext_key if include_plaintext else None,
    )


# ── Public catalogue ─────────────────────────────────────────────────


@public_router.get(
    "/products",
    response_model=list[ProductResponse],
    response_model_by_alias=True,
)
async def list_products(
    use_case: Annotated[ListProducts, Depends(get_list_products_uc)],
    category: str | None = None,
    type_: str | None = None,
) -> list[ProductResponse]:
    products = await use_case.execute(category=category, product_type=type_)
    return [_product_response(p) for p in products]


# ── Auth'd checkout ──────────────────────────────────────────────────


@public_router.post(
    "/checkout",
    response_model=CheckoutResponse,
    response_model_by_alias=True,
    status_code=201,
)
async def create_checkout_session(
    body: CheckoutRequest,
    use_case: Annotated[CreateCheckoutSession, Depends(get_create_checkout_uc)],
    principal: Annotated[UserPrincipal, Depends(require_principal)],
) -> CheckoutResponse:
    if not isinstance(principal, UserPrincipal):
        raise HTTPException(status_code=403, detail="user token required")
    try:
        session = await use_case.execute(user_id=principal.user_id, product_slug=body.product_slug)
    except ProductNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except InvalidProductForCheckoutError as exc:
        raise HTTPException(status_code=409, detail=str(exc)) from exc
    return CheckoutResponse(session_id=session.session_id, url=session.url)


# ── Stripe webhook receiver ──────────────────────────────────────────


@webhook_router.post("/stripe/webhook", status_code=200)
async def stripe_webhook(
    request: Request,
    use_case: Annotated[HandleStripeWebhook, Depends(get_handle_webhook_uc)],
    verifier: Annotated[StripeWebhookVerifierPort, Depends(get_webhook_verifier)],
    stripe_signature: Annotated[str | None, Header(alias="Stripe-Signature")] = None,
) -> dict[str, str]:
    raw_body = await request.body()
    if not stripe_signature:
        raise HTTPException(status_code=400, detail="missing Stripe-Signature header")
    try:
        event = verifier.verify(raw_body=raw_body, signature_header=stripe_signature)
    except StripeSignatureError as exc:
        logger.warning("stripe webhook rejected: %s", exc)
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    try:
        await use_case.execute(event)
    except DuplicateWebhookError:
        # Stripe retries are normal — return 200 so they stop retrying.
        return {"status": "duplicate"}
    return {"status": "ok"}


# ── User-scoped reads ────────────────────────────────────────────────


@me_router.get(
    "/orders",
    response_model=list[OrderResponse],
    response_model_by_alias=True,
)
async def list_my_orders(
    use_case: Annotated[ListMyOrders, Depends(get_my_orders_uc)],
    principal: Annotated[UserPrincipal, Depends(require_principal)],
) -> list[OrderResponse]:
    if not isinstance(principal, UserPrincipal):
        raise HTTPException(status_code=403, detail="user token required")
    orders = await use_case.execute(principal.user_id)
    return [_order_response(o) for o in orders]


@me_router.get(
    "/licenses",
    response_model=list[LicenseKeyResponse],
    response_model_by_alias=True,
)
async def list_my_licenses(
    use_case: Annotated[ListMyLicenses, Depends(get_my_licenses_uc)],
    principal: Annotated[UserPrincipal, Depends(require_principal)],
) -> list[LicenseKeyResponse]:
    if not isinstance(principal, UserPrincipal):
        raise HTTPException(status_code=403, detail="user token required")
    licenses = await use_case.execute(principal.user_id)
    return [_license_response(lic) for lic in licenses]


# ── Admin ────────────────────────────────────────────────────────────


@admin_router.post(
    "/licenses/{license_id}/revoke",
    response_model=LicenseKeyResponse,
    response_model_by_alias=True,
)
async def revoke_license(
    license_id: UUID,
    use_case: Annotated[RevokeLicense, Depends(get_revoke_license_uc)],
    _principal: Annotated[UserPrincipal, Depends(require_editor)],
) -> LicenseKeyResponse:
    try:
        lic = await use_case.execute(license_id)
    except LicenseAlreadyRevokedError as exc:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(exc)) from exc
    return _license_response(lic)


__all__ = [
    "admin_router",
    "get_create_checkout_uc",
    "get_handle_webhook_uc",
    "get_list_products_uc",
    "get_my_licenses_uc",
    "get_my_orders_uc",
    "get_revoke_license_uc",
    "get_webhook_verifier",
    "me_router",
    "public_router",
    "webhook_router",
]
