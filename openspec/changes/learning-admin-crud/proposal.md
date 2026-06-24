## Why

Adding a learning path or module today requires editing seed data in source and shipping a migration + redeploy — one PR per curriculum change. Courses, lessons, and categories are already authored entirely through the admin API; learning **paths** and **modules** are the last catalogue resources still stuck in code (issue #203). Promoting them to admin-CRUD resources lets curriculum (e.g. the requested "Computer Engineering" path) be authored via the API with no source changes or redeploys.

## What Changes

- Add admin write endpoints under the existing `/api/v1/admin/learning` router (guarded by `require_editor`):
  - **Modules**: `GET` (admin list), `POST` (create), `PATCH /{slug}` (update), `DELETE /{slug}`.
  - **Paths**: `GET` (admin list), `POST` (create), `PATCH /{slug}` (update, incl. reordering `moduleSlugs`), `DELETE /{slug}`, and `POST /{slug}/modules/reorder`.
- Extend the `LearningRepository` port + its SQLAlchemy adapter with create/update/delete/get for modules and paths (plus a path-module reorder).
- Add application use-cases mirroring the courses CRUD style, with validation: slug format + uniqueness, `level ∈ {Beginner, Intermediate, Advanced}`, and **every `moduleSlugs` entry must reference an existing module**.
- Public read endpoints (`GET /learning/modules`, `/paths`), gating, eligibility, enrollment, deadlines, and certificates are **unchanged**.
- The existing 5 paths + 12 modules (seeded by migration `202605270003`) are preserved; storage is unchanged (no new migration).
- OpenAPI (`/openapi.json`) documents the new admin endpoints automatically via FastAPI.

Non-goals (out of scope): publish/unpublish flags for paths/modules; an admin UI; restructuring the public read contract.

## Capabilities

### New Capabilities
<!-- none -->

### Modified Capabilities
- `learning-paths`: adds a requirement that an editor can create/update/delete learning **modules** and **paths** (and reorder a path's modules) via the admin API, with `moduleSlugs` referential validation — the catalogue is no longer read-only/seed-only.

## Impact

- **Code**: `domain/learning/entities.py` (module/path factories + validation), `domain/learning/errors.py` (new errors), `domain/learning/ports.py` (port methods), `adapters/outbound/persistence/learning/repository.py` (write methods), `application/learning/use_cases.py` + `application/learning/__init__.py` (new use-cases), `adapters/inbound/api/learning/schemas.py` + `router.py` (admin schemas + routes), `main.py` (dependency wiring).
- **API**: 9 new admin routes; OpenAPI updated. No change to public/auth read endpoints.
- **Data**: no schema migration — reuses `learning_modules` / `learning_paths`. Seeded rows untouched.
- **Tests**: new unit (use-cases) + API tests; regression that the seeded 5 paths + 12 modules remain intact and that a multi-module path (Computer Engineering) is creatable and enrollable via the API.
