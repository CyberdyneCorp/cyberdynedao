# Cyberdyne Backend

Hexagonal FastAPI service that backs the SvelteKit frontend (`../frontend`). Plan and rationale live in [`../docs/backend-roadmap.md`](../docs/backend-roadmap.md); **baseline behaviour specs** (the source of truth for what each capability does today) live in [`../openspec/specs/`](../openspec/specs/).

**Status:** Live in production on Coolify. The Academy platform is built out across ~19 bounded contexts — auth, content, blog, leads, marketplace, uploads, courses (lessons, categories, progress, certificates, i18n), quizzes, learning paths, analytics, recommendations, the AI Tutor chat agent + code interpreter, DAO treasury, and the redesigned-client surfaces (bookmarks, activity/streak, skill map, achievements, concepts). See `../openspec/specs/` for the per-capability contracts.

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
│   ├── inbound/    # FastAPI routers (one package per bounded context) + auth middleware
│   └── outbound/   # external clients (CyberdyneAuth, Stripe, Web3, LLM, MATLAB/Python) + persistence
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
