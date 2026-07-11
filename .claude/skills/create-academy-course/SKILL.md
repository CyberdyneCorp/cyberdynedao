---
name: create-academy-course
description: Author a new Cyberdyne Academy course end-to-end — version-controlled seed file following the house lesson pattern (direct explanation + mermaid diagram + checkpoint quiz per lesson, comprehensive final quiz), wire it into a learning track, ship it, and translate it to pt-BR / es / fr. Use when the user asks to "create a course", "add a course to a learning track/path", "author academy content", or "turn this video/playlist/topic into a course".
---

# Create an Academy Course

Creates a course as **version-controlled seed content** (the source of truth), registers it, ships it through PR → auto-deploy, wires it into a learning track, and translates it. Everything below reflects how the live system actually behaves — follow it in order.

## Architecture (30 seconds)

- **Courses** live as seed modules: `backend/src/cyberdyne_backend/application/courses/seed_<slug>.py`, registered in `seed.py`, applied idempotently on every deploy (`SEED_ACADEMY_ON_BOOT=true`) via title-matched, non-destructive reconciliation.
- **Learning tracks** (`learning_paths`) contain **modules**; a module bundles courses via `courseSlugs`. Tracks/modules are authored **live via the admin API** (never seed data) by run-once CLI helpers in `cli/`.
- **Translations** are DB rows produced by an in-app LLM job — never hand-written into seeds. Supported: `en` (source), `pt-BR`, `es`, `fr`.

## Step 1 — Author the seed file

Copy `templates/seed_course_template.py` (in this skill directory) to `backend/src/cyberdyne_backend/application/courses/seed_<slug>.py` and fill it in.

**The house course pattern** (enforced by tests):

1. `Welcome` text lesson → its checkpoint quiz
2. Optional part/section intro text lessons → each followed by its checkpoint quiz
3. Content lessons, each **immediately followed** by `quiz_lesson("Quiz: <lesson title>", …)`:
   - **text** lesson: easy, direct explanation in markdown — short paragraphs, bold key concepts, one ` ```mermaid ` diagram illustrating the lesson's structure or flow
   - **video** lesson: `video_lesson(title, url, duration=…, body=…)` — the body renders **below the player** and must carry `## Summary` (complete prose, grounded ONLY in the video content), `## Main ideas` (bold-keyed bullets), `## Mindmap` (mermaid mindmap). Get transcripts with the `youtube-playlist` skill (`youtube_cc.py`)
4. Final `quiz_lesson("Check your knowledge", …)` — 8–12 questions spanning the whole course. It must be the **last** lesson.

**Hard rules (violating these breaks production):**

- Every quiz question has **exactly one** `opt(..., correct=True)` and ≥2 options. A single bad question **aborts the entire real-DB seed run** for every course after it (unit tests pass, production fails — issue #227). The shape tests guard this; keep them passing.
- **Lesson titles are reconciliation keys.** Renaming a shipped title creates a duplicate lesson; removing one leaves an orphan live (delete it via `DELETE /api/v1/admin/courses/{slug}/lessons/{id}` after deploy). Pick titles once.
- **No en dashes (`–`) or curly quotes (`' ' " "`)** anywhere in content — ruff RUF001 fails CI. Use `-` and straight quotes; em dash `—` is fine.
- Mermaid must follow the constrained grammar or it renders as an error box:
  - `mindmap`: header line `mindmap`, then `  root((Short Title))`, branches at 4 spaces, leaves at 6; every node ≤5 words, ASCII letters/digits/spaces/hyphens ONLY (no punctuation)
  - `graph`/`flowchart`: always quote labels `A["Label"]`, no `<br/>`, no `()&%;#` inside labels, ASCII node IDs
- `text`/`code` lessons require a non-empty body; `video` requires `content_url` (body optional).
- Levels: `Beginner` | `Intermediate` | `Advanced`. Slug: kebab-case, stable forever.

## Step 2 — Register + update tests

1. `seed.py`: add the import (alphabetical) and append `*<NAME>_COURSES,` to `_RAW_COURSES`.
2. `backend/tests/unit/test_courses_seed.py`:
   - bump `assert len(summary) == N` by the number of courses added
   - add the slug(s) to the big expected-slug set in `test_curated_content_covers_all_courses`
   - add a shape test calling the shared `_assert_ai_course_pattern(course)` helper (video body anatomy, lesson→quiz ordering, final quiz last, one-correct-option guard) plus exact lesson count
   - if lessons carry mindmaps, bump the expected diagram count in `test_ai_course_mindmaps_use_strict_mermaid_syntax`

## Step 3 — Track wiring CLI

Copy `templates/add_course_to_track_template.py` to `backend/src/cyberdyne_backend/cli/add_<course>_to_<track>.py`. It is a run-once, idempotent admin-API helper that:

1. creates the module bundling the course (`409` → exists, skip)
2. GETs the track's current `moduleSlugs` and PATCHes with the module appended (skip if present) — never overwrite blindly, live tracks evolve
3. PUTs **hand-authored module translations for pt-BR, es and fr** (module title/description only — course content is translated by the job in Step 5)

Add a payload-validity test in `backend/tests/unit/test_learning_admin_crud.py` mirroring `test_startups_ai_module_payload_is_valid` (level valid, bundled slugs exist in `ACADEMY_COURSES`, append helper idempotent).

Existing track slugs: `computer-engineering`, `mechanical-foundations`, `mechatronics-robotics`, `generative-design-ai`, `life-sciences-foundations`, `bioinformatics-omics`, `drug-design-ai` (list live ones with `GET /api/v1/learning/paths`).

## Step 4 — Quality gate + ship

```bash
cd backend
uv run ruff format <changed files> && uv run ruff check src tests
uv run lint-imports
uv run pytest -q --cov          # must stay ≥90% coverage
```

Branch → commit → PR (descriptive body, no AI mentions) → wait for the Quality gate check → squash-merge. **Merging to main auto-deploys on Coolify** and the boot seed provisions + publishes the course. Watch the deploy: `GET $COOLIFY_CYBERDYNE_URL/api/v1/deployments` (see the `coolify-dao-deploy-api` memory; the coolify skill's `deploy` subcommand is stale — trigger manually with `GET /api/v1/deploy?uuid=<app-uuid>` if no auto-deploy appears).

## Step 5 — Live apply (needs admin auth)

Admin endpoints need a user token with editor/admin. No credentials are stored anywhere — ask the user (a test editor account may be noted in the `academy-admin-live-apply-auth` memory; try it first).

```bash
# 1. wire the track (module + path membership + module translations)
ACADEMY_EMAIL=... ACADEMY_PASSWORD=... ACADEMY_INSECURE_TLS=1 \
  uv run python -m cyberdyne_backend.cli.add_<course>_to_<track>

# 2. translate the course content (durable in-app job, one call per language)
for lang in pt-BR es fr; do
  curl -sk -X POST "https://dao.backend.coolify.cyberdynecorp.ai/api/v1/admin/courses/<slug>/translations/$lang" \
    -H "Authorization: Bearer $TOKEN"    # → 202 {"status":"started"}
done

# 3. poll until done (job statuses: running → done | failed)
curl -sk ".../api/v1/admin/courses/<slug>/translations" -H "Authorization: Bearer $TOKEN"
```

The translator is markdown-aware and preserves fenced code blocks, so mermaid diagrams survive translation intact. Jobs are incremental (source-hash keyed): re-running after content edits only translates what changed.

## Step 6 — Verify live

```bash
# course published with the right structure (auth => full bodies; anonymous only gets the first lesson)
curl -sk "https://dao.backend.coolify.cyberdynecorp.ai/api/v1/courses/<slug>" -H "Authorization: Bearer $TOKEN"
# track membership
curl -sk "https://dao.backend.coolify.cyberdynecorp.ai/api/v1/learning/paths" | jq '.[] | select(.slug=="<track>") | .moduleSlugs'
# translated titles
curl -sk "https://dao.backend.coolify.cyberdynecorp.ai/api/v1/courses/<slug>?lang=pt-BR" -H "Authorization: Bearer $TOKEN"
```

Check ordering (every content lesson followed by its quiz, final quiz last), video `contentUrl`s, and that translated bodies keep `##` sections and ` ```mermaid ` blocks.

## Hosts & auth reference

| What | Where |
| --- | --- |
| Courses/learning API | `https://dao.backend.coolify.cyberdynecorp.ai` (NOT `api.backend...`) |
| Auth login | `POST https://auth.backend.coolify.cyberdynecorp.ai/api/v1/auth/login` `{email,password}` → `access_token` |
| TLS | self-signed for some trust stores → `ACADEMY_INSECURE_TLS=1` / `curl -k` |
| CLI env | `ACADEMY_TOKEN` or `ACADEMY_EMAIL`+`ACADEMY_PASSWORD`; `ACADEMY_API_BASE`, `ACADEMY_AUTH_BASE` |

## Scaling content authoring

For large courses (10+ lessons from transcripts/sources), fan out subagents — one per batch of lessons — each writing an isolated JSON fragment to the scratchpad (`{"<key>": {"body_md": …, "questions": [...]}}`), then assemble the seed file deterministically yourself and validate every fragment (sections present, mermaid grammar regexes, exactly-one-correct-option) before generating. Never let agents touch shared files or the repo.
