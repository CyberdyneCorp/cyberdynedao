"""Add the "DevOps Fundamentals" course to the EXISTING ``ce-devops``
module (the DevOps stage of the Computer Engineering track), as its intro
course - in front of the tool-specific deep dives (Docker, Kubernetes,
Terraform, Ansible).

Unlike the other academy path helpers, this does NOT create a new module
or touch the track's ``moduleSlugs``. It reads the ``ce-devops`` module's
current ``courseSlugs`` and PATCHes them to prepend
``devops-fundamentals`` (skipping if already present). The course itself
is seeded by ``seed_devops_fundamentals``. Idempotent, safe to re-run.

    python -m cyberdyne_backend.cli.add_devops_fundamentals_to_ce_devops

Configuration via environment variables (same scheme as the other
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

MODULE_SLUG = "ce-devops"
COURSE_SLUG = "devops-fundamentals"


def prepended_course_slugs(existing: list[str], slug: str) -> list[str] | None:
    """New ``courseSlugs`` with ``slug`` prepended as the intro course, or
    ``None`` when it is already present. Pure - unit-tested."""
    if slug in existing:
        return None
    return [slug, *existing]


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


def main() -> int:
    api = os.environ.get("ACADEMY_API_BASE", DEFAULT_API_BASE)
    token = _token()

    st, modules = _call("GET", f"{api}/api/v1/admin/learning/modules", token)
    if st != 200:
        print(f"  list modules FAILED {st}")
        return 1
    module = next((m for m in modules if m["slug"] == MODULE_SLUG), None)
    if module is None:
        print(f"  module {MODULE_SLUG}: not found")
        return 1

    slugs = prepended_course_slugs(list(module.get("courseSlugs", [])), COURSE_SLUG)
    if slugs is None:
        print(f"  module {MODULE_SLUG}: course {COURSE_SLUG} already present")
        return 0

    st, body = _call(
        "PATCH",
        f"{api}/api/v1/admin/learning/modules/{MODULE_SLUG}",
        token,
        {"courseSlugs": slugs},
    )
    if st != 200:
        print(f"  module {MODULE_SLUG}: PATCH FAILED {st} {body}")
        return 1
    print(f"  module {MODULE_SLUG}: prepended {COURSE_SLUG} ({len(slugs)} courses)")
    print(f"Done - '{COURSE_SLUG}' is the intro course of the {MODULE_SLUG} stage.")
    return 0


if __name__ == "__main__":  # pragma: no cover
    sys.exit(main())
