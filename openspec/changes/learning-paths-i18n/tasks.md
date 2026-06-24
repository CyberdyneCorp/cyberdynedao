## 1. Storage + domain

- [ ] 1.1 Migration: create `learning_module_translations` + `learning_path_translations` (slug FK ON DELETE CASCADE, language, title TEXT, description TEXT, unique (slug, language))
- [ ] 1.2 ORM models for both tables
- [ ] 1.3 Domain helper `apply_translation(entity, tr|None)` — per-field English fallback; expose `SUPPORTED_LANGUAGES`/validation to the learning layer

## 2. Ports + persistence

- [ ] 2.1 `LearningRepository`: add `locale` to `list_modules`/`list_paths`/`get_path`/`get_module`; add `upsert_/list_/delete_` module & path translation methods
- [ ] 2.2 SqlAlchemy impl: batched translation load + merge on reads (en short-circuits); translation upsert/list/delete

## 3. Application

- [ ] 3.1 Thread `locale` through `ListModules`/`ListPaths` (+ get_path/get_module callers)
- [ ] 3.2 New use-cases: `UpsertModuleTranslation`/`ListModuleTranslations`/`DeleteModuleTranslation` (+ path), validating language ∈ supported non-en

## 4. API

- [ ] 4.1 `resolve_locale` on public `GET /learning/modules` + `/paths`
- [ ] 4.2 Admin translation routes (GET/PUT/DELETE) for modules and paths; schemas; error→404/422 mapping
- [ ] 4.3 Wire new use-case deps in `main.py`

## 5. Tests + verify

- [ ] 5.1 Unit: `apply_translation` fallback; translation use-case language validation
- [ ] 5.2 API: set translation → `?lang=` returns it (per-field fallback); unsupported/en → 422; unknown slug → 404; seeded catalogue still English
- [ ] 5.3 ruff + mypy + lint-imports + pytest green; OpenAPI shows new routes + `lang` param
- [ ] 5.4 `openspec validate learning-paths-i18n --strict`

## 6. Apply (post-deploy)

- [ ] 6.1 Translate the Computer Engineering + Electrical Engineering paths + stages to es/fr/pt-BR via the new admin endpoints
