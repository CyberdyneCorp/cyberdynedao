"""End-to-end tests for learning path/module i18n: admin sets translations,
public catalogue reads them per-locale with English fallback."""

from __future__ import annotations

import uuid
from datetime import UTC, datetime

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from cyberdyne_backend.adapters.inbound.middleware.auth import require_editor, require_principal
from cyberdyne_backend.domain.auth_identity import UserPrincipal

pytestmark = pytest.mark.integration

_NOW = datetime(2026, 6, 1, 12, 0, tzinfo=UTC)


def _editor() -> UserPrincipal:
    return UserPrincipal(
        user_id=uuid.uuid4(),
        username="e",
        scopes=frozenset({"editor"}),
        audience=None,
        expires_at=_NOW,
    )


def _learner() -> UserPrincipal:
    return UserPrincipal(
        user_id=uuid.uuid4(),
        username="l",
        scopes=frozenset(),
        audience=None,
        expires_at=_NOW,
    )


@pytest.fixture
def admin_client(app: FastAPI, _prepared_schema: None) -> TestClient:
    app.dependency_overrides[require_principal] = _learner
    app.dependency_overrides[require_editor] = _editor
    return TestClient(app)


_MODULE = {
    "title": "Digital Logic",
    "category": "Engineering",
    "description": "Gates and circuits.",
    "level": "Beginner",
    "duration": "3 courses",
    "icon": "🔢",
    "topics": [],
}


def _make_module(c: TestClient, slug: str) -> None:
    assert (
        c.post("/api/v1/admin/learning/modules", json={**_MODULE, "slug": slug}).status_code == 201
    )


def test_module_translation_read_with_locale_and_fallback(admin_client: TestClient) -> None:
    _make_module(admin_client, "digital-logic")
    # Spanish title only (description left empty → should fall back per field).
    r = admin_client.put(
        "/api/v1/admin/learning/modules/digital-logic/translations/es",
        json={"title": "Lógica Digital"},
    )
    assert r.status_code == 200, r.text
    assert r.json() == {"language": "es", "title": "Lógica Digital", "description": ""}

    es = {m["slug"]: m for m in admin_client.get("/api/v1/learning/modules?lang=es").json()}
    assert es["digital-logic"]["title"] == "Lógica Digital"
    assert es["digital-logic"]["description"] == "Gates and circuits."  # per-field English fallback

    en = {m["slug"]: m for m in admin_client.get("/api/v1/learning/modules").json()}
    assert en["digital-logic"]["title"] == "Digital Logic"

    # Listed by the admin translations endpoint.
    langs = [
        t["language"]
        for t in admin_client.get(
            "/api/v1/admin/learning/modules/digital-logic/translations"
        ).json()
    ]
    assert langs == ["es"]


def test_unsupported_and_english_language_rejected(admin_client: TestClient) -> None:
    _make_module(admin_client, "m1")
    assert (
        admin_client.put(
            "/api/v1/admin/learning/modules/m1/translations/en", json={"title": "x"}
        ).status_code
        == 422
    )
    assert (
        admin_client.put(
            "/api/v1/admin/learning/modules/m1/translations/de", json={"title": "x"}
        ).status_code
        == 422
    )


def test_translation_unknown_slug_404(admin_client: TestClient) -> None:
    assert (
        admin_client.put(
            "/api/v1/admin/learning/modules/ghost/translations/es", json={"title": "x"}
        ).status_code
        == 404
    )


def test_path_translation_set_read_delete(admin_client: TestClient) -> None:
    _make_module(admin_client, "m1")
    admin_client.post(
        "/api/v1/admin/learning/paths",
        json={
            "title": "Computer Engineering",
            "description": "The stack.",
            "moduleSlugs": ["m1"],
            "estimatedTime": "24 weeks",
            "icon": "🖥️",
        },
    )
    assert (
        admin_client.put(
            "/api/v1/admin/learning/paths/computer-engineering/translations/pt-BR",
            json={"title": "Engenharia de Computação", "description": "A pilha completa."},
        ).status_code
        == 200
    )

    pt = {p["slug"]: p for p in admin_client.get("/api/v1/learning/paths?lang=pt-BR").json()}
    assert pt["computer-engineering"]["title"] == "Engenharia de Computação"

    # Delete → public read falls back to English.
    assert (
        admin_client.delete(
            "/api/v1/admin/learning/paths/computer-engineering/translations/pt-BR"
        ).status_code
        == 204
    )
    pt2 = {p["slug"]: p for p in admin_client.get("/api/v1/learning/paths?lang=pt-BR").json()}
    assert pt2["computer-engineering"]["title"] == "Computer Engineering"
