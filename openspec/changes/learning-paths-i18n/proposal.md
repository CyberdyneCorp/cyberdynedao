## Why

Courses are fully internationalized (locale-aware reads + `*_translations` tables + `SUPPORTED_LANGUAGES = en/pt-BR/es/fr`), but learning **paths** and **modules** are not — their rows store English only and the public reads take no locale. So an es/fr/pt-BR learner sees translated course content inside a path but English stage/path titles. Issue #211.

## What Changes

- Add `learning_module_translations` and `learning_path_translations` tables (FK to the module/path slug `ON DELETE CASCADE`, `language`, `title`, `description`; unique `(slug, language)`). One migration.
- **Locale-aware public reads**: `GET /api/v1/learning/modules` and `/paths` accept the request locale (`resolve_locale`) and return the translated `title`/`description` when present, with **per-field English fallback** — same semantics as courses.
- **Admin translation CRUD**: `GET` / `PUT` / `DELETE /api/v1/admin/learning/modules/{slug}/translations/{language}` and the same for `paths` (editor-guarded; `language` must be a supported non-`en` tag). Provided-translation upsert (path/module content is short prose — no code/markdown to mask, so the course LLM auto-translate pipeline isn't warranted here).
- Languages reuse the academy `SUPPORTED_LANGUAGES` (`en` base + `pt-BR`, `es`, `fr`).

Non-goals: translating the *courses* (already done); LLM auto-generation of path translations; frontend (the learner path view doesn't exist yet — it will pass `?lang=` when built); translating `topics`/`icon`.

## Capabilities

### Modified Capabilities
- `learning-paths`: module/path titles & descriptions are translatable per language; public catalogue reads are locale-aware with English fallback; editors manage translations via the admin API.

## Impact

- **Data**: new migration adds the two translations tables. Existing modules/paths/seed unaffected (English base rows unchanged).
- **Backend**: `domain/learning` (translation port methods + a locale-merge helper), `persistence/learning` (models + repo locale reads/writes), `application/learning` (read use-cases gain `locale`; new translation upsert/list/delete use-cases), `api/learning` (resolve_locale on public reads; admin translation routes), `main.py` wiring.
- **Tests**: locale fallback unit tests + API tests (set translation → `?lang=` returns it, fallback to en; unsupported language → 422; seeded catalogue still English).
- After deploy: the Computer Engineering + Electrical Engineering paths and their stages get es/fr/pt-BR translations applied via the new endpoints.
