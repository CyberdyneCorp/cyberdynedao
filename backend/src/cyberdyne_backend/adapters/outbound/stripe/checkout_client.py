"""Stripe Checkout client.

Talks to the Stripe REST API directly via ``httpx`` — no
``stripe-python`` dep. Two reasons:
1. ``stripe-python`` is sync-first and imposes a global ``stripe.api_key``
   side-effect. Our hexagonal contract wants the secret passed in.
2. We only need ``POST /v1/checkout/sessions`` here; the surface is small.

The mock variant returns a fake session URL — used in tests and in
local dev when ``STRIPE_SECRET_KEY`` isn't configured.
"""

from __future__ import annotations

import logging
from typing import cast
from uuid import UUID, uuid4

import httpx

from cyberdyne_backend.domain.marketplace import CheckoutSession, Product

logger = logging.getLogger("cyberdyne_backend.stripe")

_STRIPE_API_BASE = "https://api.stripe.com/v1"


class StripeCheckoutClient:
    """Real Stripe API caller. Active when ``STRIPE_SECRET_KEY`` is set."""

    def __init__(
        self,
        *,
        secret_key: str,
        http_client: httpx.AsyncClient,
        timeout_s: float = 10.0,
    ) -> None:
        if not secret_key:
            raise ValueError("STRIPE_SECRET_KEY is required")
        self._secret_key = secret_key
        self._http = http_client
        self._timeout_s = timeout_s

    async def create_checkout_session(
        self,
        *,
        product: Product,
        user_id: UUID,
        success_url: str,
        cancel_url: str,
        client_reference_id: str | None = None,
    ) -> CheckoutSession:
        if not product.stripe_price_id:
            raise ValueError(f"product {product.slug} has no stripe_price_id")
        # Stripe expects form-encoded bodies on the REST API.
        form = {
            "mode": "payment",
            "line_items[0][price]": product.stripe_price_id,
            "line_items[0][quantity]": "1",
            "success_url": success_url,
            "cancel_url": cancel_url,
            "client_reference_id": client_reference_id or str(user_id),
            "metadata[product_slug]": product.slug,
            "metadata[user_id]": str(user_id),
        }
        response = await self._http.post(
            f"{_STRIPE_API_BASE}/checkout/sessions",
            data=form,
            auth=(self._secret_key, ""),
            timeout=self._timeout_s,
        )
        if response.status_code >= 400:
            logger.error("stripe checkout error %s: %s", response.status_code, response.text)
            raise RuntimeError(f"stripe checkout failed: {response.status_code}")
        body = cast(dict[str, object], response.json())
        session_id = cast(str, body["id"])
        url = cast(str, body["url"])
        return CheckoutSession(session_id=session_id, url=url)


class MockStripeCheckoutClient:
    """No-op checkout for local dev. Returns a synthetic session whose
    ``url`` points at a marker URL the frontend can recognise."""

    def __init__(self, *, success_url_template: str = "/marketplace?mock_session={sid}") -> None:
        self._template = success_url_template

    async def create_checkout_session(
        self,
        *,
        product: Product,
        user_id: UUID,
        success_url: str,
        cancel_url: str,
        client_reference_id: str | None = None,
    ) -> CheckoutSession:
        sid = f"cs_mock_{uuid4().hex[:24]}"
        return CheckoutSession(
            session_id=sid,
            url=self._template.format(sid=sid),
        )
