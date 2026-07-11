"""Wire schemas for the websearch endpoint."""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_camel


class _CamelModel(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)


class SearchResultResponse(_CamelModel):
    position: int
    title: str
    url: str
    snippet: str = ""
    source: str = ""


class SearchResponse(_CamelModel):
    query: str
    answer: str | None = None
    results: list[SearchResultResponse]
