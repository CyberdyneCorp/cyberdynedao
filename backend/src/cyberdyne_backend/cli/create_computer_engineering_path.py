"""Create the "Computer Engineering" learning path + its modules via the
admin API (GitHub issue #203, ask 1).

This is an operational, run-once helper — NOT app seed data. It proves the
point of the admin-CRUD feature: curriculum is authored through the API with
no source change or redeploy. It is idempotent: existing modules/paths
(409 Conflict) are skipped, so it is safe to re-run.

    python -m cyberdyne_backend.cli.create_computer_engineering_path

Configuration via environment variables (same scheme as ``academy_backup``):
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

# The curriculum from issue #203. Modules first, then the path referencing them.
MODULES: tuple[dict[str, Any], ...] = (
    {
        "slug": "programming-fundamentals",
        "title": "Programming Fundamentals",
        "category": "Foundations",
        "level": "Beginner",
        "duration": "1 hr",
        "icon": "💻",
        "description": "Variables, control flow, functions and recursion — writing your first correct programs.",
        "topics": ["Variables & Types", "Control Flow", "Functions", "Recursion"],
    },
    {
        "slug": "digital-logic",
        "title": "Digital Logic & Boolean Algebra",
        "category": "Hardware",
        "level": "Beginner",
        "duration": "50 min",
        "icon": "🔢",
        "description": "How gates become circuits: the bridge from boolean algebra to real hardware.",
        "topics": [
            "Boolean Algebra",
            "Logic Gates",
            "Combinational Circuits",
            "Sequential Circuits",
        ],
    },
    {
        "slug": "discrete-mathematics",
        "title": "Discrete Mathematics",
        "category": "Foundations",
        "level": "Beginner",
        "duration": "1 hr",
        "icon": "➗",
        "description": "The math of computing: sets, proofs, graphs and counting.",
        "topics": ["Sets & Relations", "Proof Techniques", "Graph Theory", "Combinatorics"],
    },
    {
        "slug": "data-structures-algorithms",
        "title": "Data Structures & Algorithms",
        "category": "CS Core",
        "level": "Intermediate",
        "duration": "2 hr",
        "icon": "🌳",
        "description": "Choosing the right structure and reasoning about cost.",
        "topics": [
            "Arrays & Lists",
            "Trees & Graphs",
            "Sorting & Searching",
            "Complexity Analysis",
        ],
    },
    {
        "slug": "computer-architecture",
        "title": "Computer Architecture & Organization",
        "category": "Hardware",
        "level": "Intermediate",
        "duration": "1.5 hr",
        "icon": "🖥️",
        "description": "From the instruction set down to pipelines and caches.",
        "topics": [
            "Instruction Set Architecture",
            "CPU Datapath & Pipelining",
            "Memory Hierarchy & Caches",
            "I/O Systems",
        ],
    },
    {
        "slug": "operating-systems",
        "title": "Operating Systems",
        "category": "Systems",
        "level": "Intermediate",
        "duration": "1.5 hr",
        "icon": "⚙️",
        "description": "How the OS shares the CPU, memory and devices safely.",
        "topics": [
            "Processes & Threads",
            "Scheduling",
            "Memory Management",
            "File Systems & Concurrency",
        ],
    },
    {
        "slug": "embedded-systems",
        "title": "Embedded Systems & Microcontrollers",
        "category": "Hardware",
        "level": "Advanced",
        "duration": "1.5 hr",
        "icon": "🔧",
        "description": "Programming close to the metal on resource-constrained devices.",
        "topics": ["Microcontrollers", "GPIO & Peripherals", "RTOS", "Firmware in C"],
    },
    {
        "slug": "computer-networks",
        "title": "Computer Networks",
        "category": "Systems",
        "level": "Intermediate",
        "duration": "1 hr",
        "icon": "🌐",
        "description": "How packets move from your NIC to the other side of the world.",
        "topics": [
            "OSI & TCP/IP",
            "Routing & Switching",
            "Transport Protocols",
            "Network Security",
        ],
    },
    {
        "slug": "databases",
        "title": "Databases & Data Management",
        "category": "CS Core",
        "level": "Intermediate",
        "duration": "1 hr",
        "icon": "🗄️",
        "description": "Modeling, querying and keeping data consistent.",
        "topics": ["Relational Model", "SQL", "Indexing & Transactions", "Normalization"],
    },
    {
        "slug": "signals-and-systems",
        "title": "Signals & Systems",
        "category": "Electrical",
        "level": "Advanced",
        "duration": "1.5 hr",
        "icon": "📶",
        "description": "The EE half of computer engineering: analyzing signals in time and frequency.",
        "topics": ["Time & Frequency Domain", "Fourier Analysis", "Sampling", "Filtering"],
    },
)

PATH: dict[str, Any] = {
    "slug": "computer-engineering",
    "title": "Computer Engineering",
    "description": (
        "From logic gates and C to operating systems and networks — the full "
        "hardware-software stack that defines computer engineering."
    ),
    "moduleSlugs": [m["slug"] for m in MODULES],
    "estimatedTime": "16-24 weeks",
    "icon": "🖥️",
}


def build_payloads() -> tuple[list[dict[str, Any]], dict[str, Any]]:
    """Return (module payloads, path payload). Pure — unit-tested. Guarantees
    the path only references modules that are created here."""
    module_slugs = {m["slug"] for m in MODULES}
    missing = [s for s in PATH["moduleSlugs"] if s not in module_slugs]
    if missing:  # pragma: no cover - guards against editing mistakes
        raise ValueError(f"path references modules not in MODULES: {missing}")
    return list(MODULES), dict(PATH)


def _ctx() -> ssl.SSLContext | None:
    if os.environ.get("ACADEMY_INSECURE_TLS") == "1":
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE
        return ctx
    return None


def _call(method: str, url: str, token: str, body: dict | None = None) -> tuple[int, Any]:
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
        return json.loads(r.read().decode())["access_token"]


def main() -> int:
    api = os.environ.get("ACADEMY_API_BASE", DEFAULT_API_BASE)
    token = _token()
    modules, path = build_payloads()

    for module in modules:
        st, _ = _call("POST", f"{api}/api/v1/admin/learning/modules", token, module)
        verb = "created" if st in (200, 201) else ("exists" if st == 409 else f"FAILED {st}")
        print(f"  module {module['slug']}: {verb}")

    st, body = _call("POST", f"{api}/api/v1/admin/learning/paths", token, path)
    if st in (200, 201):
        print(f"  path {path['slug']}: created")
    elif st == 409:
        print(f"  path {path['slug']}: exists")
    else:
        print(f"  path {path['slug']}: FAILED {st} {body}")
        return 1
    print("Done — 'Computer Engineering' path is live and enrollable.")
    return 0


if __name__ == "__main__":  # pragma: no cover
    sys.exit(main())
