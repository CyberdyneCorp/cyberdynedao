"""List all Cyberdyne Academy learning tracks and the courses in each.

Read-only. Uses the PUBLIC learning API (no auth): joins
``/api/v1/learning/paths`` (the tracks + their ordered module slugs) with
``/api/v1/learning/modules`` (each module's bundled, resolved courses).

    python3 list_tracks.py                 # all tracks -> modules -> courses
    python3 list_tracks.py --track computer-engineering
    python3 list_tracks.py --lang pt-BR    # localized titles
    python3 list_tracks.py --json          # machine-readable
    python3 list_tracks.py --orphans       # also show courses in NO track

Config via env (same scheme as the academy helpers):
  ACADEMY_API_BASE   default https://dao.backend.coolify.cyberdynecorp.ai
  ACADEMY_INSECURE_TLS=1   disable TLS verification (self-signed hosts)
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


def _ctx() -> ssl.SSLContext | None:
    if os.environ.get("ACADEMY_INSECURE_TLS") == "1":
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE
        return ctx
    return None


def _get(url: str, *, retries: int = 3) -> Any:
    """GET + parse JSON, retrying transient failures (transport errors and
    5xx - Coolify cold pods blip). Raises SystemExit with a clean message on
    a persistent failure instead of an opaque traceback."""
    last = ""
    for attempt in range(1, retries + 1):
        try:
            with urllib.request.urlopen(url, context=_ctx()) as r:
                return json.loads(r.read().decode())
        except urllib.error.HTTPError as e:
            transient = e.code >= 500
            last = f"HTTP {e.code}: {e.read().decode()[:200]}"
        except (urllib.error.URLError, TimeoutError, ConnectionError, json.JSONDecodeError) as e:
            transient = True
            last = f"transport error: {getattr(e, 'reason', e)}"
        if not transient or attempt == retries:
            raise SystemExit(f"GET {url} failed ({last})")
        time.sleep(0.6 * attempt)
    raise SystemExit(f"GET {url} failed after {retries} tries ({last})")


def build(api: str, lang: str | None) -> tuple[list[dict[str, Any]], dict[str, dict[str, Any]]]:
    """Return (paths, modules-by-slug). Locale applied to both when given."""
    suffix = f"?lang={lang}" if lang else ""
    paths = _get(f"{api}/api/v1/learning/paths{suffix}")
    modules = _get(f"{api}/api/v1/learning/modules{suffix}")
    return paths, {m["slug"]: m for m in modules}


def _tracks_view(
    paths: list[dict[str, Any]], by_slug: dict[str, dict[str, Any]]
) -> list[dict[str, Any]]:
    out = []
    for p in paths:
        modules = []
        for ms in p.get("moduleSlugs", []):
            m = by_slug.get(ms)
            if m is None:
                modules.append({"slug": ms, "title": "(missing module)", "courses": []})
                continue
            modules.append(
                {
                    "slug": m["slug"],
                    "title": m["title"],
                    "level": m.get("level"),
                    "courses": [
                        {"slug": c["slug"], "title": c["title"], "level": c.get("level")}
                        for c in m.get("courses", [])
                    ],
                    "courseSlugs": m.get("courseSlugs", []),
                }
            )
        out.append(
            {
                "slug": p["slug"],
                "title": p["title"],
                "estimatedTime": p.get("estimatedTime"),
                "moduleCount": len(p.get("moduleSlugs", [])),
                "modules": modules,
            }
        )
    return out


def _print_tree(tracks: list[dict[str, Any]]) -> None:
    for t in tracks:
        est = f" [{t['estimatedTime']}]" if t.get("estimatedTime") else ""
        print(f"\n# {t['title']}  ({t['slug']}){est} - {t['moduleCount']} modules")
        for i, m in enumerate(t["modules"], 1):
            lvl = f" [{m['level']}]" if m.get("level") else ""
            print(f"  {i:>2}. {m['title']}  ({m['slug']}){lvl}")
            for c in m["courses"]:
                clvl = f" - {c['level']}" if c.get("level") else ""
                print(f"        - {c['title']}  ({c['slug']}){clvl}")
            if not m["courses"] and m.get("courseSlugs"):
                print(f"        (bundles {m['courseSlugs']} - not resolved)")


def main() -> int:
    ap = argparse.ArgumentParser(description="List learning tracks and their courses.")
    ap.add_argument("--track", help="only this track slug")
    ap.add_argument("--lang", help="locale for titles (pt-BR, es, fr)")
    ap.add_argument("--json", action="store_true", help="machine-readable output")
    ap.add_argument(
        "--orphans", action="store_true", help="also list courses that are in no track"
    )
    args = ap.parse_args()
    api = os.environ.get("ACADEMY_API_BASE", DEFAULT_API_BASE)

    paths, by_slug = build(api, args.lang)
    if args.track:
        paths = [p for p in paths if p["slug"] == args.track]
        if not paths:
            print(f"no track with slug {args.track!r}", file=sys.stderr)
            return 1
    tracks = _tracks_view(paths, by_slug)

    orphans: list[str] = []
    if args.orphans:
        # A course is "orphaned" if no module in the catalogue bundles it.
        bundled = {cs for m in by_slug.values() for cs in m.get("courseSlugs", [])}
        catalogue = _get(f"{api}/api/v1/courses?limit=200")
        orphans = sorted({c["slug"] for c in catalogue} - bundled)

    if args.json:
        payload: dict[str, Any] = {"tracks": tracks}
        if args.orphans:
            payload["coursesInNoTrack"] = orphans
        print(json.dumps(payload, indent=2, ensure_ascii=False))
        return 0

    _print_tree(tracks)
    if args.orphans:
        print(f"\n# Courses in NO track ({len(orphans)}):")
        for s in orphans:
            print(f"  - {s}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
