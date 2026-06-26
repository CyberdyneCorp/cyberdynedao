"""Regression tests for the OpenAI embedding client batching (issue #244).

OpenAI's ``/v1/embeddings`` caps ``input`` at 2048 elements per request. The
catalog grew past that, so embedding the whole catalog in one call 400'd and
every ``/api/v1/agent`` turn (and ``/learning/scan``) 502'd. The client now
batches under the cap; these tests pin that with a mock transport and an
oversized (> 2048) catalog index build — no network.
"""

from __future__ import annotations

import json

import httpx
import pytest

from cyberdyne_backend.adapters.outbound.llm.embedding_client import (
    OpenAIEmbeddingClient,
)
from cyberdyne_backend.application.course_finder import CatalogSearchIndex
from cyberdyne_backend.domain.ai_chat import ChatProviderError
from cyberdyne_backend.domain.course_finder import CatalogEntry

pytestmark = pytest.mark.unit

_OPENAI_INPUT_CAP = 2048


def _client(record: list[int], *, status: int = 200) -> OpenAIEmbeddingClient:
    """A client whose mock transport records each request's ``input`` size and
    echoes one embedding per input — ``[float(i)]`` parsed from a ``t{i}`` text
    so cross-batch ordering is verifiable."""

    def handler(request: httpx.Request) -> httpx.Response:
        body = json.loads(request.content)
        inputs = body["input"]
        record.append(len(inputs))
        if status >= 400:
            return httpx.Response(status, json={"error": {"message": "boom"}})
        data = [{"index": i, "embedding": [float(int(t[1:]))]} for i, t in enumerate(inputs)]
        return httpx.Response(200, json={"data": data})

    http = httpx.AsyncClient(transport=httpx.MockTransport(handler))
    return OpenAIEmbeddingClient(api_key="sk-test", http_client=http)


async def test_embed_batches_under_openai_input_cap() -> None:
    record: list[int] = []
    client = _client(record)
    texts = [f"t{i}" for i in range(2500)]

    vectors = await client.embed(texts)

    assert len(vectors) == 2500
    # Split into 1000 + 1000 + 500 — every request stays within the 2048 cap.
    assert record == [1000, 1000, 500]
    assert all(n <= _OPENAI_INPUT_CAP for n in record)
    # Order is preserved across batches.
    assert vectors[0] == [0.0]
    assert vectors[1000] == [1000.0]
    assert vectors[2499] == [2499.0]


async def test_embed_empty_makes_no_request() -> None:
    record: list[int] = []
    assert await _client(record).embed([]) == []
    assert record == []


async def test_embed_small_input_is_single_request() -> None:
    record: list[int] = []
    out = await _client(record).embed(["t1", "t2", "t3"])
    assert record == [3]
    assert out == [[1.0], [2.0], [3.0]]


async def test_embed_surfaces_api_error() -> None:
    with pytest.raises(ChatProviderError, match="embeddings error 400"):
        await _client([], status=400).embed(["t1"])


class _BigCatalogSource:
    """A catalog source with more entries than the OpenAI per-request cap."""

    def __init__(self, count: int) -> None:
        self._count = count

    async def entries(self) -> list[CatalogEntry]:
        return [
            CatalogEntry(course_slug=f"course-{i}", lesson_id=None, text=f"t{i}")
            for i in range(self._count)
        ]


async def test_catalog_index_build_over_cap_is_batched() -> None:
    record: list[int] = []
    index = CatalogSearchIndex(source=_BigCatalogSource(2500), embedder=_client(record))

    await index.build()  # must not raise — the regression was a 400 here

    assert sum(record) == 2500  # every entry embedded
    assert all(n <= _OPENAI_INPUT_CAP for n in record)
    assert len(record) >= 2  # actually batched, not one oversized request
