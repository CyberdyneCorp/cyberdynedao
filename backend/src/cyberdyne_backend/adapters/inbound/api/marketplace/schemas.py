"""Pydantic schemas for marketplace endpoints."""

from __future__ import annotations

from datetime import datetime
from typing import Literal
from uuid import UUID

from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_camel


class _CamelModel(BaseModel):
    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
    )


class ProductResponse(_CamelModel):
    slug: str
    type: Literal["service", "training", "license"]
    title: str
    description_md: str
    price_cents: int
    currency: str
    duration_label: str
    features: list[str]
    category: str
    subcategory: str | None = None
    image_url: str
    popular: bool
    status: Literal["available", "beta", "coming_soon", "retired"]
    is_purchasable: bool


class CheckoutRequest(_CamelModel):
    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
        extra="forbid",
    )

    product_slug: str


class CheckoutResponse(_CamelModel):
    session_id: str
    url: str


class OrderResponse(_CamelModel):
    id: UUID
    product_slug: str
    amount_cents: int
    currency: str
    status: Literal["pending", "paid", "refunded", "failed"]
    created_at: datetime
    paid_at: datetime | None = None


class LicenseKeyResponse(_CamelModel):
    """Full response includes the plaintext key — only used on the
    immediate issuance reply. Subsequent reads omit it."""

    id: UUID
    product_slug: str
    issued_at: datetime
    expires_at: datetime | None = None
    revoked_at: datetime | None = None
    is_active: bool
    # Plaintext is only set on the immediate issuance reply.
    plaintext_key: str | None = None
