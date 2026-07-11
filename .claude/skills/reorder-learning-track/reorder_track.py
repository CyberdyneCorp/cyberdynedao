"""Reorder the modules of a Cyberdyne Academy learning track.

Reordering operates on a track's **modules** (each bundling one or more
courses). This helper shows the current order with the resolved courses so
you can reason about it, validates that the desired order is a permutation
of the existing modules, applies it via the admin reorder endpoint, and
verifies the result.

    # 1. inspect the current order (read-only, no auth)
    python3 reorder_track.py show computer-engineering

    # 2a. apply an explicit full order (must be exactly the current set)
    python3 reorder_track.py apply computer-engineering \
        --order slugA,slugB,slugC,...          # every module, new order

    # 2b. or move one module to a position (1-based), others keep order
    python3 reorder_track.py apply computer-engineering \
        --move gpu-programming-cuda-opencl --to 10

    # 2c. or sort by module level then keep relative order (Beginner first)
    python3 reorder_track.py apply computer-engineering --sort-by-level

Applying needs editor/admin auth (same scheme as the academy CLIs):
  ACADEMY_TOKEN, or ACADEMY_EMAIL + ACADEMY_PASSWORD
  ACADEMY_API_BASE / ACADEMY_AUTH_BASE, ACADEMY_INSECURE_TLS=1
`show` needs no auth. `apply` prints the diff and (unless --yes) asks to
confirm before writing.
"""

from __future__ import annotations

import argparse
import json
import os
import ssl
import sys
import time
import urllib.error
import urllib.request
from typing import Any

DEFAULT_API_BASE = "https://dao.backend.coolify.cyberdynecorp.ai"
DEFAULT_AUTH_BASE = "https://auth.backend.coolify.cyberdynecorp.ai"
_LEVEL_ORDER = {"Beginner": 0, "Intermediate": 1, "Advanced": 2}


def _ctx() -> ssl.SSLContext | None:
    if os.environ.get("ACADEMY_INSECURE_TLS") == "1":
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE
        return ctx
    return None


def _call(method: str, url: str, token: str | None = None, body: Any = None) -> tuple[int, Any]:
    """Return (status, parsed_body). status 0 means a transport error (no
    HTTP response); body is then the error string. A non-JSON error body is
    returned as its raw string."""
    data = json.dumps(body).encode() if body is not None else None
    req = urllib.request.Request(url, data=data, method=method)
    req.add_header("Content-Type", "application/json")
    if token:
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
    except (urllib.error.URLError, TimeoutError, ConnectionError) as e:
        return 0, str(getattr(e, "reason", e))


def _get_list(api: str, path: str, *, retries: int = 3) -> list[Any]:
    """GET a JSON array with retry on transient failure (transport error or
    5xx - cold pods on Coolify blip). Raises SystemExit with a clear message
    on a persistent error or an unexpected response shape."""
    url = f"{api}{path}"
    last = ""
    for attempt in range(1, retries + 1):
        status, body = _call("GET", url)
        if status == 200 and isinstance(body, list):
            return body
        if status == 200:
            raise SystemExit(f"GET {path}: expected a JSON array, got {type(body).__name__}")
        transient = status == 0 or status >= 500
        detail = body if isinstance(body, str) else json.dumps(body)
        last = f"HTTP {status or 'transport error'}: {str(detail)[:200]}"
        if not transient or attempt == retries:
            raise SystemExit(f"GET {path} failed ({last})")
        time.sleep(0.6 * attempt)  # brief backoff; cold pod usually recovers
    raise SystemExit(f"GET {path} failed after {retries} tries ({last})")


def _token() -> str:
    token = os.environ.get("ACADEMY_TOKEN")
    if token:
        return token
    auth = os.environ.get("ACADEMY_AUTH_BASE", DEFAULT_AUTH_BASE)
    email, password = os.environ.get("ACADEMY_EMAIL"), os.environ.get("ACADEMY_PASSWORD")
    if not (email and password):
        raise SystemExit("set ACADEMY_TOKEN, or ACADEMY_EMAIL + ACADEMY_PASSWORD")
    status, body = _call(
        "POST", f"{auth}/api/v1/auth/login", body={"email": email, "password": password}
    )
    if status != 200 or not isinstance(body, dict) or "access_token" not in body:
        raise SystemExit(f"login failed (HTTP {status or 'transport error'}): {str(body)[:200]}")
    return str(body["access_token"])


def _load(api: str) -> tuple[dict[str, dict[str, Any]], dict[str, dict[str, Any]]]:
    paths = _get_list(api, "/api/v1/learning/paths")
    modules = _get_list(api, "/api/v1/learning/modules")
    return {p["slug"]: p for p in paths}, {m["slug"]: m for m in modules}


def _print_order(track: dict[str, Any], by_slug: dict[str, dict[str, Any]]) -> None:
    print(f"# {track['title']}  ({track['slug']}) - {len(track['moduleSlugs'])} modules")
    for i, ms in enumerate(track["moduleSlugs"], 1):
        m = by_slug.get(ms, {})
        lvl = f" [{m.get('level')}]" if m.get("level") else ""
        courses = ", ".join(c["slug"] for c in m.get("courses", [])) or "(no courses)"
        print(f"  {i:>2}. {m.get('title', ms)}  ({ms}){lvl}  -> {courses}")


def cmd_show(api: str, track_slug: str) -> int:
    paths, by_slug = _load(api)
    track = paths.get(track_slug)
    if track is None:
        print(f"no track {track_slug!r}. Available: {sorted(paths)}", file=sys.stderr)
        return 1
    _print_order(track, by_slug)
    return 0


def _compute_order(current: list[str], args: argparse.Namespace, by_slug: dict) -> list[str]:
    if args.order:
        return [s.strip() for s in args.order.split(",") if s.strip()]
    if args.move:
        if args.move not in current:
            raise SystemExit(f"module {args.move!r} is not in this track")
        rest = [s for s in current if s != args.move]
        pos = max(1, min(args.to or len(current), len(current))) - 1
        return rest[:pos] + [args.move] + rest[pos:]
    if args.sort_by_level:
        # Stable sort by module level (Beginner < Intermediate < Advanced),
        # preserving the current relative order within a level.
        return sorted(current, key=lambda s: _LEVEL_ORDER.get(by_slug.get(s, {}).get("level"), 1))
    raise SystemExit("choose one of --order / --move --to / --sort-by-level")


def cmd_apply(api: str, track_slug: str, args: argparse.Namespace) -> int:
    paths, by_slug = _load(api)
    track = paths.get(track_slug)
    if track is None:
        print(f"no track {track_slug!r}", file=sys.stderr)
        return 1
    current = list(track["moduleSlugs"])
    desired = _compute_order(current, args, by_slug)

    # The reorder endpoint requires a permutation of the existing modules.
    if sorted(desired) != sorted(current):
        missing = sorted(set(current) - set(desired))
        extra = sorted(set(desired) - set(current))
        print("ERROR: new order must be exactly the current module set.", file=sys.stderr)
        if missing:
            print(f"  dropped: {missing}", file=sys.stderr)
        if extra:
            print(f"  unknown/added: {extra}", file=sys.stderr)
        return 2
    if desired == current:
        print("No change - the order is already as requested.")
        return 0

    print("Reorder plan:")
    for i, (a, b) in enumerate(zip(current, desired, strict=True), 1):
        mark = "" if a == b else "  <-- moved"
        print(f"  {i:>2}. {by_slug.get(b, {}).get('title', b)}  ({b}){mark}")
    if not args.yes:
        if input("\nApply this order? [y/N] ").strip().lower() not in ("y", "yes"):
            print("aborted.")
            return 0

    token = _token()
    st, body = _call(
        "POST",
        f"{api}/api/v1/admin/learning/paths/{track_slug}/modules/reorder",
        token,
        {"moduleSlugs": desired},
    )
    if st != 200:
        print(f"FAILED {st}: {body}", file=sys.stderr)
        return 1
    # Verify live.
    verify = _get_list(api, "/api/v1/learning/paths")
    live = next(p["moduleSlugs"] for p in verify if p["slug"] == track_slug)
    ok = live == desired
    print(f"\nDone - reorder {'verified live' if ok else 'APPLIED but live order differs!'}.")
    return 0 if ok else 1


def main() -> int:
    ap = argparse.ArgumentParser(description="Reorder a learning track's modules.")
    sub = ap.add_subparsers(dest="cmd", required=True)
    ps = sub.add_parser("show", help="print the current module order (no auth)")
    ps.add_argument("track")
    pa = sub.add_parser("apply", help="apply a new module order (needs editor auth)")
    pa.add_argument("track")
    pa.add_argument("--order", help="comma-separated full new order of module slugs")
    pa.add_argument("--move", help="a module slug to move")
    pa.add_argument("--to", type=int, help="1-based target position for --move")
    pa.add_argument("--sort-by-level", action="store_true", help="Beginner->Advanced, stable")
    pa.add_argument("--yes", "-y", action="store_true", help="skip the confirmation prompt")
    args = ap.parse_args()

    api = os.environ.get("ACADEMY_API_BASE", DEFAULT_API_BASE)
    if args.cmd == "show":
        return cmd_show(api, args.track)
    return cmd_apply(api, args.track, args)


if __name__ == "__main__":
    raise SystemExit(main())
