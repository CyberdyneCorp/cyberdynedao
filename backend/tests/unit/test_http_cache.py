"""Conditional-request (ETag) caching for the public catalogue (issue #258).

Covers the ``http_cache`` helper directly (match / non-match branches) and an
end-to-end conditional GET against ``/api/v1/categories``: the first request
returns ``200`` with an ``ETag`` + ``Cache-Control``; a second request echoing
that ETag in ``If-None-Match`` returns an empty ``304``. No DB is needed — the
list use case is dependency-overridden with fixed data.
"""

from __future__ import annotations

import uuid

import pytest
from fastapi import FastAPI, Request
from fastapi.testclient import TestClient

from cyberdyne_backend.adapters.inbound.api.courses.router import get_list_categories_uc
from cyberdyne_backend.adapters.inbound.api.courses.schemas import CategoryResponse
from cyberdyne_backend.adapters.inbound.api.http_cache import conditional_json_list


def _request(headers: dict[str, str] | None = None) -> Request:
    raw = [(k.lower().encode(), v.encode()) for k, v in (headers or {}).items()]
    return Request({"type": "http", "method": "GET", "headers": raw})


def _model() -> CategoryResponse:
    return CategoryResponse(id=uuid.uuid4(), slug="prog", name="Programming")


# ── Helper unit tests ────────────────────────────────────────────────


def test_helper_200_carries_etag_and_cache_control() -> None:
    resp = conditional_json_list([_model()], _request())
    assert resp.status_code == 200
    assert resp.headers["ETag"].startswith('"')
    assert "max-age=" in resp.headers["Cache-Control"]
    assert "private" in resp.headers["Cache-Control"]


def test_helper_returns_304_on_matching_if_none_match() -> None:
    model = _model()
    first = conditional_json_list([model], _request())
    etag = first.headers["ETag"]

    second = conditional_json_list([model], _request({"If-None-Match": etag}))
    assert second.status_code == 304
    assert second.body == b""
    assert second.headers["ETag"] == etag


def test_helper_200_on_stale_if_none_match() -> None:
    resp = conditional_json_list([_model()], _request({"If-None-Match": '"stale"'}))
    assert resp.status_code == 200


# ── Endpoint conditional-request test ────────────────────────────────


class _Cat:
    # Stable identity across calls, so two requests serialize to the same body
    # (and thus the same ETag) — the whole point of the 304 revalidation test.
    def __init__(self) -> None:
        self.id = uuid.UUID("11111111-1111-1111-1111-111111111111")
        self.slug = "programming"
        self.name = "Programming"
        self.icon = "💻"
        self.sort_order = 0
        self.parent_id = None


class _FixedCategoriesUC:
    async def execute(self) -> list[_Cat]:
        return [_Cat()]


@pytest.fixture
def client_with_categories(app: FastAPI) -> TestClient:
    app.dependency_overrides[get_list_categories_uc] = lambda: _FixedCategoriesUC()
    return TestClient(app)


def test_categories_conditional_request_roundtrip(client_with_categories: TestClient) -> None:
    first = client_with_categories.get("/api/v1/categories")
    assert first.status_code == 200
    etag = first.headers["ETag"]
    assert etag
    assert "max-age=" in first.headers["Cache-Control"]
    assert first.json()[0]["slug"] == "programming"

    # Revalidate with the ETag → cheap 304, empty body, same ETag.
    second = client_with_categories.get("/api/v1/categories", headers={"If-None-Match": etag})
    assert second.status_code == 304
    assert second.content == b""
    assert second.headers["ETag"] == etag
