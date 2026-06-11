"""Regression: the OpenAPI schema must advertise the bearer requirement.

Enforcement is per-route (``Depends(require_principal)`` /
``Depends(require_editor)``), so FastAPI only renders Swagger's "Authorize"
button and per-route padlocks if the guards declare an ``HTTPBearer`` security
scheme. Without it, protected endpoints *look* open in /docs even though a
tokenless call returns 401. This locks that contract in.
"""

from __future__ import annotations

from fastapi.testclient import TestClient


def _schema(client: TestClient) -> dict:
    response = client.get("/openapi.json")
    assert response.status_code == 200
    return response.json()


def test_openapi_declares_httpbearer_scheme(client: TestClient) -> None:
    schema = _schema(client)
    schemes = schema.get("components", {}).get("securitySchemes", {})
    assert schemes.get("HTTPBearer") == {"type": "http", "scheme": "bearer"}


def test_protected_operation_requires_httpbearer(client: TestClient) -> None:
    schema = _schema(client)
    # POST /api/v1/marketplace/checkout is guarded by require_principal.
    op = schema["paths"]["/api/v1/marketplace/checkout"]["post"]
    assert op.get("security") == [{"HTTPBearer": []}]


def test_open_paths_carry_no_security(client: TestClient) -> None:
    schema = _schema(client)
    paths = schema["paths"]
    for path in ("/healthz", "/readyz", "/openapi.json"):
        op = paths.get(path, {}).get("get")
        if op is not None:
            assert "security" not in op, f"{path} should be open"


def test_every_security_requirement_uses_httpbearer(client: TestClient) -> None:
    schema = _schema(client)
    protected = 0
    for methods in schema["paths"].values():
        for op in methods.values():
            if isinstance(op, dict) and op.get("security"):
                protected += 1
                assert op["security"] == [{"HTTPBearer": []}]
    # There are guarded routes (this would be 0 if the scheme stopped wiring).
    assert protected > 0
