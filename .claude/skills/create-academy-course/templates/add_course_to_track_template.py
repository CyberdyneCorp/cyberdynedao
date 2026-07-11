"""Add the "<Course Title>" course to the <Track Title> learning path via
the admin API.

An operational, run-once helper, NOT app seed data (companion to
``add_startups_ai_to_computer_engineering`` and the ``create_*_path*``
helpers). The course itself is seeded by the academy seed
(``seed_<slug>``); this script

  1. creates the ``<module-slug>`` module bundling that course
     (409 -> already exists, skipped),
  2. appends the module to the ``<track-slug>`` path's ``moduleSlugs``
     (skipped if already present), and
  3. upserts the module's pt-BR / es / fr translations (PUT — idempotent).

Safe to re-run.

    python -m cyberdyne_backend.cli.add_<course>_to_<track>

Configuration via environment variables (same scheme as the other path
helpers):
  ACADEMY_API_BASE   default https://dao.backend.coolify.cyberdynecorp.ai
  ACADEMY_AUTH_BASE  default https://auth.backend.coolify.cyberdynecorp.ai
  ACADEMY_TOKEN      a bearer token (skips login), OR
  ACADEMY_EMAIL / ACADEMY_PASSWORD   to log in
  ACADEMY_INSECURE_TLS=1   disable TLS verification (self-signed hosts)
"""
# TEMPLATE — copy to backend/src/cyberdyne_backend/cli/add_<course>_to_<track>.py,
# fill MODULE / MODULE_TRANSLATIONS / PATH_SLUG, delete these comments, and
# add a payload test in tests/unit/test_learning_admin_crud.py.

from __future__ import annotations

import json
import os
import ssl
import sys
import urllib.error
import urllib.request
from typing import Any

DEFAULT_API_BASE = "https://dao.backend.coolify.cyberdynecorp.ai"
DEFAULT_AUTH_BASE = "https://auth.backend.coolify.cyberdynecorp.ai"

PATH_SLUG = "<track-slug>"  # e.g. computer-engineering

MODULE: dict[str, Any] = {
    "slug": "<module-slug>",  # usually the course slug
    "title": "<Course Title>",
    "category": "<Category>",  # e.g. Entrepreneurship, CS Core, Systems
    "level": "Beginner",  # Beginner | Intermediate | Advanced
    "duration": "<N hr>",  # sum of lesson durations, rounded
    "icon": "<one emoji>",
    "description": "<One-sentence module description for the track page.>",
    "topics": [
        "<Topic 1>",
        "<Topic 2>",
        "<Topic 3>",
        "<Topic 4>",
    ],
    "courseSlugs": ["<course-slug>"],
}

# Hand-authored translations for the MODULE card only (title/description).
# Course CONTENT is translated by the in-app job (see the skill, Step 5).
MODULE_TRANSLATIONS: dict[str, dict[str, str]] = {
    "pt-BR": {
        "title": "<Título em português>",
        "description": "<Descrição em português.>",
    },
    "es": {
        "title": "<Título en español>",
        "description": "<Descripción en español.>",
    },
    "fr": {
        "title": "<Titre en français>",
        "description": "<Description en français.>",
    },
}


def build_module_payload() -> dict[str, Any]:
    """Return the module payload. Pure — unit-tested. Guarantees the module
    bundles the course this feature ships."""
    if not MODULE["courseSlugs"]:  # pragma: no cover - edit guard
        raise ValueError("module must bundle at least one course")
    return dict(MODULE)


def appended_module_slugs(existing: list[str], slug: str) -> list[str] | None:
    """Module list for the path PATCH, or ``None`` when nothing to do."""
    if slug in existing:
        return None
    return [*existing, slug]


def _ctx() -> ssl.SSLContext | None:
    if os.environ.get("ACADEMY_INSECURE_TLS") == "1":
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE
        return ctx
    return None


def _call(method: str, url: str, token: str, body: dict[str, Any] | None = None) -> tuple[int, Any]:
    data = json.dumps(body).encode() if body is not None else None
    req = urllib.request.Request(url, data=data, method=method)
    req.add_header("Content-Type", "application/json")
    req.add_header("Authorization", f"Bearer {token}")
    try:
        with urllib.request.urlopen(req, context=_ctx()) as r:
            raw = r.read().decode()
            return r.status, (json.loads(raw) if raw else None)
    except urllib.error.HTTPError as e:
        raw = e.read().decode()
        try:
            return e.code, json.loads(raw)
        except json.JSONDecodeError:
            return e.code, raw


def _token() -> str:
    token = os.environ.get("ACADEMY_TOKEN")
    if token:
        return token
    auth = os.environ.get("ACADEMY_AUTH_BASE", DEFAULT_AUTH_BASE)
    email = os.environ.get("ACADEMY_EMAIL")
    password = os.environ.get("ACADEMY_PASSWORD")
    if not (email and password):
        raise SystemExit("set ACADEMY_TOKEN, or ACADEMY_EMAIL + ACADEMY_PASSWORD")
    req = urllib.request.Request(
        f"{auth}/api/v1/auth/login",
        data=json.dumps({"email": email, "password": password}).encode(),
        method="POST",
    )
    req.add_header("Content-Type", "application/json")
    with urllib.request.urlopen(req, context=_ctx()) as r:
        access_token: str = json.loads(r.read().decode())["access_token"]
    return access_token


def main() -> int:
    api = os.environ.get("ACADEMY_API_BASE", DEFAULT_API_BASE)
    token = _token()
    module = build_module_payload()

    st, _ = _call("POST", f"{api}/api/v1/admin/learning/modules", token, module)
    verb = "created" if st in (200, 201) else ("exists" if st == 409 else f"FAILED {st}")
    print(f"  module {module['slug']}: {verb}")
    if verb.startswith("FAILED"):
        return 1

    st, paths = _call("GET", f"{api}/api/v1/admin/learning/paths", token)
    if st != 200:
        print(f"  path {PATH_SLUG}: list FAILED {st}")
        return 1
    path = next((p for p in paths if p["slug"] == PATH_SLUG), None)
    if path is None:
        print(f"  path {PATH_SLUG}: not found — create the track first")
        return 1
    slugs = appended_module_slugs(list(path["moduleSlugs"]), module["slug"])
    if slugs is None:
        print(f"  path {PATH_SLUG}: module already present")
    else:
        st, body = _call(
            "PATCH",
            f"{api}/api/v1/admin/learning/paths/{PATH_SLUG}",
            token,
            {"moduleSlugs": slugs},
        )
        if st != 200:
            print(f"  path {PATH_SLUG}: PATCH FAILED {st} {body}")
            return 1
        print(f"  path {PATH_SLUG}: module appended ({len(slugs)} modules)")

    for language, tr in MODULE_TRANSLATIONS.items():
        st, body = _call(
            "PUT",
            f"{api}/api/v1/admin/learning/modules/{module['slug']}/translations/{language}",
            token,
            tr,
        )
        if st != 200:
            print(f"  translation {language}: FAILED {st} {body}")
            return 1
        print(f"  translation {language}: upserted")

    print(f"Done — '{MODULE['title']}' is part of the {PATH_SLUG} path.")
    return 0


if __name__ == "__main__":  # pragma: no cover
    sys.exit(main())
