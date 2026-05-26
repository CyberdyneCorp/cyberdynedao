# Cyberdyne Backend

Hexagonal FastAPI service that backs the SvelteKit frontend (`../frontend`). Plan and rationale live in [`../docs/backend-roadmap.md`](../docs/backend-roadmap.md).

**Status:** Phase 1 scaffold. `/healthz` + `/readyz` only. Real endpoints land in Phase 1.5+.

---

## Stack

- Python 3.12 · FastAPI · `uv` · structlog · pydantic v2
- Quality gate: `ruff` (lint + format), `mypy --strict`, `import-linter` (hexagonal-layer enforcement), `pytest-cov` (≥90% on `domain` + `application`)
- Deploy: Coolify (multi-stage `uv` Dockerfile, runs as non-root)

## Layout

```
src/cyberdyne_backend/
├── domain/         # entities, value objects, ports — pure Python, no I/O
├── application/    # use cases, orchestration
├── adapters/
│   ├── inbound/    # FastAPI routers (right now: /healthz, /readyz)
│   └── outbound/   # external clients (CyberdyneAuth, Stripe, Web3 — Phase 1.5+)
├── infrastructure/ # settings, logging, container wiring
└── main.py         # ASGI app factory
```

`import-linter` blocks PRs that violate the layers.

## Quickstart

```bash
just install            # uv sync --all-extras
just dev                # uvicorn on :8000 with --reload
just check              # lint + fmt-check + typecheck + lint-imports + test
```

Run individual gates: `just lint`, `just fmt-check`, `just typecheck`, `just lint-imports`, `just test`.

## Environment

Phase 1 needs almost nothing — `LOG_LEVEL` (default `INFO`) and `ENVIRONMENT` (default `local`). Full env-var inventory in the roadmap doc, §9.

## Tests

- **Unit** (`tests/unit/`) — no I/O. Counted toward the 90% coverage gate.
- **Integration** (`tests/integration/`) — adapters that cross a process boundary. Excluded from the default run; opt in with `just test-integration`.

The coverage gate only counts `domain/` + `application/`. Adapter coverage is by integration test instead — same calibration as the rest of the Cyberdyne stack.

## Deploy

See [`../docs/backend-roadmap.md`](../docs/backend-roadmap.md) §9 for the Coolify recipe (build args, env vars grouped by `is_build` vs `is_runtime`, and the traps to plan around).
