## Context

Mirror the courses i18n design for the learning catalogue. Courses use `course_translations`/`lesson_translations` (FK + `language` + `title`/`description`), a `resolve_locale` FastAPI dependency, per-field English fallback in the repo, and `SUPPORTED_LANGUAGES = ("en","pt-BR","es","fr")` (in `application/academy`). Learning modules/paths are keyed by **slug** (string PK), not UUID, so translation FKs reference the slug.

## Goals / Non-Goals

**Goals:** translatable module/path title+description with English fallback; locale-aware public reads; editor CRUD for translations; reuse the academy `SUPPORTED_LANGUAGES` + `resolve_locale`; zero change to existing English rows/seed.

**Non-Goals:** LLM auto-generation (provided-translation upsert — content is short prose); translating `topics`/`icon`/course content; frontend (no learner path view yet); a re-translate-on-change `source_hash` (admin/script-driven, not seeded).

## Decisions

- **Storage**: `learning_module_translations(slug FK→learning_modules.slug ON DELETE CASCADE, language, title TEXT, description TEXT, PK or unique (slug,language))` and `learning_path_translations` likewise. Slug FK (not UUID) since that's the PK. No `source_hash` (unlike courses) — these aren't seeded.
- **Read merge**: a pure domain helper `apply_translation(module/path, tr|None)` returns a copy with translated `title`/`description` substituted per-field when non-empty, else English. The repo loads translations for the requested locale in one batched query (`slug IN (...) AND language=?`) and merges — same shape as `_course_translations`. `en`/empty locale short-circuits (no join).
- **Port + use-cases**: `LearningRepository` read methods (`list_modules`, `list_paths`, `get_path`, `get_module`) gain `locale: str = "en"`; add translation writes (`upsert_module_translation`, `list_module_translations`, `delete_module_translation`, + path variants). New app use-cases `UpsertModuleTranslation`/`ListModuleTranslations`/`DeleteModuleTranslation` (+ path) and `locale` threaded into `ListModules`/`ListPaths` (and `get_path`/`get_module` callers). Gating/eligibility operate on slugs, so they don't need locale.
- **Language validation** in the use-case: must be in `SUPPORTED_LANGUAGES` and `!= "en"` → else `LearningContentValidationError` (→ 422). Reuse the academy constant (or re-export) rather than redefining.
- **API**: `resolve_locale` dependency on the two public catalogue GETs (passes `locale` to the use-case). Admin routes on the existing `admin_router` under `…/modules/{slug}/translations[/{language}]` and `…/paths/{slug}/translations[/{language}]`, editor-guarded, mapping domain errors to 404/422. New camelCase request/response schemas (`TranslationUpsertRequest{title,description}`, `TranslationResponse{language,title,description}`).
- **Wiring**: new dep providers in `main.py` mirroring the existing learning ones; the SqlAlchemy translation reader/writer over the new tables.

## Risks / Trade-offs

- **Cross-context constant reuse**: importing `SUPPORTED_LANGUAGES` from `application/academy` into the learning layer is a small coupling; acceptable (it's the canonical language set) and keeps the supported set single-sourced.
- **No `source_hash`**: editing a module's English title won't flag its translations as stale (courses do, for the seeder). Acceptable — learning translations are managed explicitly by an editor/script, not regenerated on reseed; staleness is the editor's call.
- **Provided vs generated**: not auto-translating means an editor (or the apply script) supplies the strings. Fine for short titles/descriptions and avoids wiring an LLM into the learning context.
