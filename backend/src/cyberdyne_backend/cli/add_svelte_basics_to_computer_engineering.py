"""Add the "Svelte — Basics" course to the Computer Engineering learning
path via the admin API.

An operational, run-once helper, NOT app seed data (companion to
``add_startups_ai_to_computer_engineering`` and the ``create_*_path*``
helpers). The course itself is seeded by the academy seed
(``seed_svelte``); this script

  1. creates the ``svelte-basics`` module bundling that course
     (409 -> already exists, skipped),
  2. appends the module to the ``computer-engineering`` path's
     ``moduleSlugs`` (skipped if already present), and
  3. upserts the module's pt-BR / es / fr translations (PUT — idempotent).

Safe to re-run.

    python -m cyberdyne_backend.cli.add_svelte_basics_to_computer_engineering

Configuration via environment variables (same scheme as the other path
helpers):
  ACADEMY_API_BASE   default https://dao.backend.coolify.cyberdynecorp.ai
  ACADEMY_AUTH_BASE  default https://auth.backend.coolify.cyberdynecorp.ai
  ACADEMY_TOKEN      a bearer token (skips login), OR
  ACADEMY_EMAIL / ACADEMY_PASSWORD   to log in
  ACADEMY_INSECURE_TLS=1   disable TLS verification (self-signed hosts)
"""

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

PATH_SLUG = "computer-engineering"

MODULE: dict[str, Any] = {
    "slug": "svelte-basics",
    "title": "Svelte — Basics",
    "category": "Web Development",
    "level": "Beginner",
    "duration": "2 hr",
    "icon": "🔥",
    "description": (
        "User interfaces with modern Svelte (runes): single-file components, "
        "$state and $derived, props, events, two-way bindings, logic blocks, "
        "effects and composition — one diagram and one realistic example per "
        "lesson."
    ),
    "topics": [
        "Components & Runes",
        "Props & State",
        "Events & Bindings",
        "Logic Blocks & Effects",
    ],
    "courseSlugs": ["svelte-basics"],
}

# Hand-authored translations for the MODULE card only (title/description).
# Course CONTENT is translated by the in-app job.
MODULE_TRANSLATIONS: dict[str, dict[str, str]] = {
    "pt-BR": {
        "title": "Svelte — Fundamentos",
        "description": (
            "Interfaces de usuário com Svelte moderno (runes): componentes "
            "de arquivo único, $state e $derived, props, eventos, bindings "
            "bidirecionais, blocos de lógica, efeitos e composição — um "
            "diagrama e um exemplo realista por lição."
        ),
    },
    "es": {
        "title": "Svelte — Fundamentos",
        "description": (
            "Interfaces de usuario con Svelte moderno (runes): componentes "
            "de archivo único, $state y $derived, props, eventos, bindings "
            "bidireccionales, bloques de lógica, efectos y composición — un "
            "diagrama y un ejemplo realista por lección."
        ),
    },
    "fr": {
        "title": "Svelte — Les bases",
        "description": (
            "Interfaces utilisateur avec Svelte moderne (runes) : composants "
            "monofichiers, $state et $derived, props, événements, liaisons "
            "bidirectionnelles, blocs logiques, effets et composition — un "
            "diagramme et un exemple réaliste par leçon."
        ),
    },
}


def build_module_payload() -> dict[str, Any]:
    """Return the module payload. Pure — unit-tested. Guarantees the module
    bundles the course this feature ships (``seed_svelte``)."""
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
