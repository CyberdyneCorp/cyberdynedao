"""Pydantic schemas for the wallet access-tier endpoint."""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_camel


class _CamelModel(BaseModel):
    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
    )


class AccessTraitsResponse(_CamelModel):
    learning: bool
    frontend: bool
    backend: bool
    blog_creator: bool
    admin: bool
    marketplace: bool


class WalletAccessResponse(_CamelModel):
    address: str
    has_access_nft: bool
    token_count: int
    traits: AccessTraitsResponse
