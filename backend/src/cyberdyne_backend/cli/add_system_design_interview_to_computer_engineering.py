"""Add the "System Design Interview Prep" course to the Computer Engineering
learning path via the admin API.

An operational, run-once helper, NOT app seed data (companion to
``add_fine_tuning_llms_to_computer_engineering`` and the ``create_*_path*``
helpers). The course itself is seeded by the academy seed
(``seed_system_design_interview``); this script

  1. creates the ``system-design-interview`` module bundling that course
     (409 -> already exists, skipped),
  2. appends the module to the ``computer-engineering`` path's
     ``moduleSlugs`` (skipped if already present), and
  3. upserts the module's pt-BR / es / fr translations (PUT - idempotent).

Safe to re-run.

    python -m cyberdyne_backend.cli.add_system_design_interview_to_computer_engineering

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
    "slug": "system-design-interview",
    "title": "System Design Interview Prep",
    "category": "Software Engineering",
    "level": "Intermediate",
    "duration": "3 hr",
    "icon": "🧩",
    "description": (
        "Reason through the system design interview: scalability, reliability "
        "and availability, load balancing, caching and CDNs, SQL vs NoSQL with "
        "replication and sharding, the CAP theorem, and message queues - then "
        "design a system end to end, with a full crash-course video."
    ),
    "topics": [
        "Scalability & availability",
        "Caching & load balancing",
        "Databases & CAP",
        "End-to-end design",
    ],
    "courseSlugs": ["system-design-interview"],
}

# Hand-authored translations for the MODULE card only (title/description).
# Course CONTENT is translated by the in-app job.
MODULE_TRANSLATIONS: dict[str, dict[str, str]] = {
    "pt-BR": {
        "title": "Preparacao para Entrevista de System Design",
        "description": (
            "Raciocine na entrevista de system design: escalabilidade, "
            "confiabilidade e disponibilidade, balanceamento de carga, cache e "
            "CDNs, SQL vs NoSQL com replicacao e sharding, o teorema CAP e filas "
            "de mensagens - e projete um sistema de ponta a ponta, com um video."
        ),
    },
    "es": {
        "title": "Preparacion para Entrevista de System Design",
        "description": (
            "Razona en la entrevista de system design: escalabilidad, "
            "confiabilidad y disponibilidad, balanceo de carga, cache y CDNs, "
            "SQL vs NoSQL con replicacion y sharding, el teorema CAP y colas de "
            "mensajes - y disena un sistema de extremo a extremo, con un video."
        ),
    },
    "fr": {
        "title": "Preparation a l'Entretien de System Design",
        "description": (
            "Raisonnez lors de l'entretien de system design : scalabilite, "
            "fiabilite et disponibilite, repartition de charge, cache et CDN, "
            "SQL vs NoSQL avec replication et sharding, le theoreme CAP et les "
            "files de messages - puis concevez un systeme de bout en bout, avec "
            "une video."
        ),
    },
}


def build_module_payload() -> dict[str, Any]:
    """Return the module payload. Pure - unit-tested. Guarantees the module
    bundles the course this feature ships (``seed_system_design_interview``)."""
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
        print(f"  path {PATH_SLUG}: not found - create the track first")
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

    print(f"Done - '{MODULE['title']}' is part of the {PATH_SLUG} path.")
    return 0


if __name__ == "__main__":  # pragma: no cover
    sys.exit(main())
