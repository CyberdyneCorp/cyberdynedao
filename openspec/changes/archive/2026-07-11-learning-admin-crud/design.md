## Context

Learning modules and paths are already DB-backed (`learning_modules`, `learning_paths` tables) and read through `SqlAlchemyLearningRepository.list_modules/list_paths/get_path`. They are seeded once by migration `202605270003` (12 modules + 5 paths) and have **no write API** — the `LearningRepository` port exposes only reads for the catalogue. Courses, lessons, and categories already follow a complete admin-CRUD pattern (use-case classes + override-target dependency providers in `main.py` + `require_editor`-guarded routes), which this change mirrors.

## Goals / Non-Goals

**Goals:**
- Editors create/update/delete modules and paths (and reorder a path's modules) via `/api/v1/admin/learning/...` with no source change or redeploy.
- `moduleSlugs` referential integrity enforced at the application layer.
- Public read/gating/enrollment/certificate behavior and the seeded catalogue stay byte-for-byte identical until explicitly edited.
- New endpoints documented in OpenAPI.

**Non-Goals:**
- Publish/unpublish flags (modules/paths remain always-visible catalogue rows).
- Admin UI, translations, or restructuring the public read contract.
- New storage migration — existing tables are reused.

## Decisions

- **Layering mirrors courses CRUD.** New use-cases (`CreateModule`, `UpdateModule`, `DeleteModule`, `CreatePath`, `UpdatePath`, `DeletePath`, `ReorderPathModules`) live in `application/learning/use_cases.py` and are exported from `application/learning/__init__.py`. Each gets an override-target provider (`get_*_uc`) in the learning router and an async-generator `_*_dep` in `main.py` wired via `app.dependency_overrides`.
- **Routes on the existing `admin_router`** (`prefix=/api/v1/admin/learning`, already guarded by `require_editor`), so auth is reused, not reinvented.
- **Validation in the use-case, not the route.** `level` enum, slug derivation (reuse the project's slugify helper), and `moduleSlugs`-must-exist are enforced in the use-case so they hold regardless of caller. `moduleSlugs` are validated against `repo.list_modules()` before any write — invalid → domain `LearningContentValidationError` → mapped to `422`; nothing persists.
- **Slug handling.** Optional `slug` derived from `title` when omitted; create raises a domain `LearningContentConflictError` (→ `409`) when the slug exists. The repository create methods are explicit inserts (not upserts) so duplicates surface as conflicts.
- **Repository write methods** added to the port + adapter: `get_module`, `create_module`, `update_module`, `delete_module`, `create_path`, `update_path`, `delete_path`, `set_path_modules`. Update methods take a partial set of fields (None = leave unchanged) and raise `LearningContentNotFoundError` (→ `404`) when the slug is absent. New rows get `sort_order = max(existing)+1` so they sort after the seeded ones.
- **Reorder** is a thin wrapper over `update_path(module_slugs=...)` exposed as a dedicated endpoint to match `courses/reorder` ergonomics; it shares the same `moduleSlugs` validation.
- **Computer Engineering path (issue ask 1)** is created via the new API post-deploy using a small script (same approach as the course apply script), not via a seed/source edit — that is the whole point of the feature. A test exercises the equivalent create-path-with-modules flow so the capability is covered in CI.

## Risks / Trade-offs

- **Deleting a module referenced by a path** could orphan a `moduleSlug`. Mitigation: deletion is allowed (matching how the catalogue already tolerates arbitrary `module_slugs`), but gating already treats unknown slugs defensively; a follow-up could add a guard. Documented, not enforced, to keep scope tight.
- **No publish flag** means a created path is immediately public. Acceptable: editors are trusted, and it matches today's always-visible catalogue. A draft state can be added later without breaking this contract.
- **Seeded-row edits are persistent** (no reseed clobber, since seeding is a one-time migration) — an intended property, but means an accidental edit to a seeded path isn't auto-reverted. Acceptable given editor-only access.
