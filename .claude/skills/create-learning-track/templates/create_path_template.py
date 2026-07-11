"""Create the "<Track Title>" learning path + its modules via the admin
API (companion to ``create_computer_engineering_path``).

An operational, run-once helper, NOT app seed data. The courses are
seeded by the academy seed; this curates them into modules and a path.
Idempotent and extend-safe:
  * each module is POSTed (409 -> already exists, skipped);
  * the path is POSTed, OR - if it already exists - its ``moduleSlugs``
    are PATCHed to include any new modules (so re-running, or growing an
    existing track, is safe);
  * module + path translations (pt-BR/es/fr) are PUT (idempotent).

    python -m cyberdyne_backend.cli.create_<track>_path

Configuration via environment variables (same scheme as the other path
helpers):
  ACADEMY_API_BASE   default https://dao.backend.coolify.cyberdynecorp.ai
  ACADEMY_AUTH_BASE  default https://auth.backend.coolify.cyberdynecorp.ai
  ACADEMY_TOKEN      a bearer token (skips login), OR
  ACADEMY_EMAIL / ACADEMY_PASSWORD   to log in
  ACADEMY_INSECURE_TLS=1   disable TLS verification (self-signed hosts)
"""
# TEMPLATE - copy to backend/src/cyberdyne_backend/cli/create_<track>_path.py,
# fill MODULES / PATH / *_TRANSLATIONS, delete these comments, and add a
# build_payloads() purity test in tests/unit/test_learning_admin_crud.py.

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

# Each module is a track stage bundling one or more seeded courses via
# ``courseSlugs``. Order MODULES in the intended learning progression.
MODULES: tuple[dict[str, Any], ...] = (
    {
        "slug": "<module-1-slug>",
        "title": "<Module 1 Title>",
        "category": "<Category>",
        "level": "Beginner",  # Beginner | Intermediate | Advanced
        "duration": "<N hr>",
        "icon": "<emoji>",
        "description": "<One-sentence stage description.>",
        "topics": ["<Topic>", "<Topic>"],
        "courseSlugs": ["<course-slug>"],  # real seeded course slugs
    },
    # ... more modules ...
)

PATH: dict[str, Any] = {
    "slug": "<track-slug>",  # stable, kebab-case
    "title": "<Track Title>",
    "description": "<2-3 sentence description of the whole track.>",
    "moduleSlugs": [m["slug"] for m in MODULES],  # ordered
    "estimatedTime": "<N-M weeks>",
    "icon": "<emoji>",
}

# Hand-authored translations for the MODULE and PATH cards (title/description
# only). Course CONTENT is translated by the in-app job (skill Step 5).
MODULE_TRANSLATIONS: dict[str, dict[str, dict[str, str]]] = {
    # "<module-slug>": {"pt-BR": {"title": "...", "description": "..."}, "es": {...}, "fr": {...}},
}
PATH_TRANSLATIONS: dict[str, dict[str, str]] = {
    "pt-BR": {"title": "<Título>", "description": "<Descrição>"},
    "es": {"title": "<Título>", "description": "<Descripción>"},
    "fr": {"title": "<Titre>", "description": "<Description>"},
}


def build_payloads() -> tuple[list[dict[str, Any]], dict[str, Any]]:
    """Return (module payloads, path payload). Pure - unit-tested. Guarantees
    the path only references modules built here."""
    module_slugs = {m["slug"] for m in MODULES}
    missing = [s for s in PATH["moduleSlugs"] if s not in module_slugs]
    if missing:  # pragma: no cover - edit guard
        raise ValueError(f"path references modules not in MODULES: {missing}")
    return list(MODULES), dict(PATH)


def merged_module_slugs(existing: list[str], wanted: list[str]) -> list[str]:
    """Existing order preserved; any wanted slug not present is appended."""
    return existing + [s for s in wanted if s not in existing]


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
    email, password = os.environ.get("ACADEMY_EMAIL"), os.environ.get("ACADEMY_PASSWORD")
    if not (email and password):
        raise SystemExit("set ACADEMY_TOKEN, or ACADEMY_EMAIL + ACADEMY_PASSWORD")
    req = urllib.request.Request(
        f"{auth}/api/v1/auth/login",
        data=json.dumps({"email": email, "password": password}).encode(),
        method="POST",
    )
    req.add_header("Content-Type", "application/json")
    with urllib.request.urlopen(req, context=_ctx()) as r:
        return str(json.loads(r.read().decode())["access_token"])


def _upsert_translations(api: str, token: str, kind: str, slug: str, trs: dict[str, Any]) -> None:
    for language, tr in trs.items():
        st, _ = _call(
            "PUT",
            f"{api}/api/v1/admin/learning/{kind}/{slug}/translations/{language}",
            token,
            tr,
        )
        print(f"    {kind[:-1]} {slug} {language}: {'ok' if st == 200 else f'FAILED {st}'}")


def main() -> int:
    api = os.environ.get("ACADEMY_API_BASE", DEFAULT_API_BASE)
    token = _token()
    modules, path = build_payloads()

    for module in modules:
        st, _ = _call("POST", f"{api}/api/v1/admin/learning/modules", token, module)
        verb = "created" if st in (200, 201) else ("exists" if st == 409 else f"FAILED {st}")
        print(f"  module {module['slug']}: {verb}")
        if module["slug"] in MODULE_TRANSLATIONS:
            _upsert_translations(api, token, "modules", module["slug"], MODULE_TRANSLATIONS[module["slug"]])

    # Create the path, or extend an existing one's moduleSlugs.
    st, body = _call("POST", f"{api}/api/v1/admin/learning/paths", token, path)
    if st in (200, 201):
        print(f"  path {path['slug']}: created")
    elif st == 409:
        _, existing = _call("GET", f"{api}/api/v1/admin/learning/paths", token)
        current = next((p["moduleSlugs"] for p in existing if p["slug"] == path["slug"]), [])
        merged = merged_module_slugs(list(current), path["moduleSlugs"])
        if merged == current:
            print(f"  path {path['slug']}: exists (all modules already present)")
        else:
            st, body = _call(
                "PATCH",
                f"{api}/api/v1/admin/learning/paths/{path['slug']}",
                token,
                {"moduleSlugs": merged},
            )
            if st != 200:
                print(f"  path {path['slug']}: PATCH FAILED {st} {body}")
                return 1
            print(f"  path {path['slug']}: extended to {len(merged)} modules")
    else:
        print(f"  path {path['slug']}: FAILED {st} {body}")
        return 1
    _upsert_translations(api, token, "paths", path["slug"], PATH_TRANSLATIONS)

    print(f"Done - '{path['title']}' path is live and enrollable.")
    return 0


if __name__ == "__main__":  # pragma: no cover
    sys.exit(main())
