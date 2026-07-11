## 1. Domain

- [ ] 1.1 Add domain errors `LearningContentNotFoundError` (already exists — confirm), `LearningContentConflictError`, `LearningContentValidationError` in `domain/learning/errors.py`
- [ ] 1.2 Add `new_module(...)` and `new_path(...)` factories in `domain/learning/entities.py` with `level` enum validation and slug derivation/normalization

## 2. Ports + Persistence

- [ ] 2.1 Extend `LearningRepository` port with `get_module`, `create_module`, `update_module`, `delete_module`, `create_path`, `update_path`, `delete_path`, `set_path_modules`
- [ ] 2.2 Implement the write methods in `SqlAlchemyLearningRepository` (explicit inserts → conflict on duplicate; partial updates; `sort_order = max+1` for new rows; raise not-found/conflict appropriately)

## 3. Application use-cases

- [ ] 3.1 Add `CreateModule`, `UpdateModule`, `DeleteModule` use-cases (slug/level validation, conflict/not-found mapping)
- [ ] 3.2 Add `CreatePath`, `UpdatePath`, `DeletePath`, `ReorderPathModules` use-cases with `moduleSlugs`-must-exist validation against `list_modules()`
- [ ] 3.3 Export the new use-cases from `application/learning/__init__.py`

## 4. API

- [ ] 4.1 Add admin request schemas (`CreateModuleRequest`, `UpdateModuleRequest`, `CreatePathRequest`, `UpdatePathRequest`, `ReorderPathModulesRequest`) in `adapters/inbound/api/learning/schemas.py`
- [ ] 4.2 Add override-target providers + admin routes (modules: GET/POST/PATCH/DELETE; paths: GET/POST/PATCH/DELETE + modules/reorder) on `admin_router`, mapping domain errors to 404/409/422
- [ ] 4.3 Wire the new use-case dependencies in `main.py` (`_*_dep` generators + `app.dependency_overrides`)

## 5. Tests

- [ ] 5.1 Unit tests for the new use-cases against a fake `LearningRepository` (create/update/delete, conflict, not-found, invalid level, unknown module ref)
- [ ] 5.2 API tests for the admin routes (auth guard, status codes, public read reflects writes, reorder changes gating order)
- [ ] 5.3 Regression test: seeded 5 paths + 12 modules intact; a multi-module "Computer Engineering" path is creatable via the API and enrollable

## 6. Verify + finalize

- [ ] 6.1 `ruff check` + `ruff format` + `lint-imports` + `pytest` all green; diff test results against main
- [ ] 6.2 Confirm OpenAPI exposes the 9 new admin routes
- [ ] 6.3 Provide a runnable script to create the Computer Engineering path live post-deploy
- [ ] 6.4 `openspec validate learning-admin-crud --strict`; open PR
