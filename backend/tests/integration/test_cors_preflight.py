"""Regression: CORS preflight must permit every method the API uses.

The learner "mark lesson complete" call is ``PUT
/courses/{slug}/lessons/{id}/progress`` (set-deadline and quiz-upsert are
also PUT). ``PUT`` was missing from the CORS ``allow_methods``, so the
browser's preflight (OPTIONS) was rejected (400) and the request was
blocked — even though the endpoint itself worked (curl bypasses CORS).
"""

from __future__ import annotations

import pytest
from fastapi.testclient import TestClient

pytestmark = pytest.mark.integration

# Default cors_origins in test settings.
ORIGIN = "http://localhost:5173"


@pytest.mark.parametrize("method", ["GET", "POST", "PUT", "PATCH", "DELETE"])
def test_cors_preflight_allows_api_methods(client: TestClient, method: str) -> None:
    resp = client.options(
        "/api/v1/courses/some-slug/lessons/00000000-0000-0000-0000-000000000000/progress",
        headers={
            "Origin": ORIGIN,
            "Access-Control-Request-Method": method,
            "Access-Control-Request-Headers": "authorization,content-type",
        },
    )
    assert resp.status_code == 200, resp.text
    allowed = resp.headers.get("access-control-allow-methods", "")
    assert method in allowed, f"{method} not in Access-Control-Allow-Methods: {allowed!r}"
    assert resp.headers.get("access-control-allow-origin") == ORIGIN
