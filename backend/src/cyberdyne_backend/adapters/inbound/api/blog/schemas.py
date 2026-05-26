"""Pydantic schemas for blog endpoints."""

from __future__ import annotations

from datetime import datetime
from typing import Literal
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field
from pydantic.alias_generators import to_camel


class _CamelModel(BaseModel):
    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
    )


StatusLiteral = Literal["draft", "published"]


class BlogPostSummaryResponse(_CamelModel):
    id: UUID
    slug: str
    title: str
    excerpt: str
    category_slug: str | None = None
    tags: list[str]
    status: StatusLiteral
    created_at: datetime
    published_at: datetime | None = None


class BlogPostDetailResponse(BlogPostSummaryResponse):
    body_md: str


class BlogPostListResponse(_CamelModel):
    items: list[BlogPostSummaryResponse]
    total: int
    page: int
    page_size: int


class CreateBlogPostRequest(_CamelModel):
    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
        extra="forbid",
    )

    title: str = Field(min_length=1, max_length=256)
    body_md: str = Field(min_length=1)
    excerpt: str = ""
    slug: str | None = Field(default=None, max_length=128)
    category_slug: str | None = Field(default=None, max_length=64)
    tags: list[str] = Field(default_factory=list)
