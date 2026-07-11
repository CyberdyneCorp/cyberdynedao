---
name: create-learning-track
description: Create a whole Cyberdyne Academy learning track (path) from context — design a curriculum of courses grouped into modules, author each course, then create the path (if it doesn't exist) with its ordered modules and translations. Use when the user asks to "create a learning track/path on X", "build a curriculum from this YouTube playlist / these videos / this syllabus", or "make a full learning path" (not just one course).
---

# Create a Learning Track

Builds an entire **learning track** end to end: turn context (a topic, a YouTube playlist, videos, a syllabus, notes) into a curriculum of **courses** grouped into **modules** forming a **path**, author every course, then create the path (if it doesn't exist) with its ordered modules and translations.

This skill **orchestrates** two lower-level ones — do not duplicate their rules, invoke them:
- **create-academy-course** — authors ONE course (the house lesson pattern, YouTube transcript/video handling, the hard production rules, seed registration + tests, per-course translation). Every course in the track is produced by following it.
- **list-learning-tracks** / **reorder-learning-track** — inspect and reorder the result.

A single course? Use **create-academy-course** directly. A whole track (several courses + a path)? This skill.

## Step 1 — Gather context, design the curriculum

From whatever the user gives you (topic, playlist URL, video URLs, a syllabus, docs), decide the **shape** before authoring anything:

1. **Enumerate source material.** For a playlist, list its videos (`youtube-playlist` skill → `youtube_playlist.py`); for loose videos, note each; for a topic/syllabus, outline the subject areas. This is the work-list.
2. **Design the courses.** Group the material into **courses** — each a coherent unit that fits the house pattern (welcome + ~6-9 content lessons + quizzes + final). A long playlist may become one video-course (like `startups-in-the-age-of-ai`, 29 talks) or several themed courses; a broad topic becomes a set of text courses (like the CE degree tracks). Pick stable kebab-case slugs.
3. **Design the modules (stages).** A **module** is a track stage that bundles one or more courses via `courseSlugs`. Group related courses into modules in a **logical learning progression** (foundations → core → advanced → capstone) — the same reasoning as reorder-learning-track. A module can bundle one course or a basics/intermediate/advanced trio.
4. **Design the path.** Title, description, stable slug, `estimatedTime`, icon, and the ordered `moduleSlugs`.

Sketch this as a short plan (courses → modules → path order) and confirm scope with the user before authoring — a track is many courses, so agree on the size first.

## Step 2 — Author every course

For **each** course in the plan, follow **create-academy-course** Steps 1-2: write `seed_<slug>.py`, register it in `seed.py`, and update the course-seed tests. Scale the authoring with subagents (create-academy-course's "Scaling content authoring") — one agent per course or per lesson-batch, each writing an isolated fragment; assemble and validate deterministically yourself. Keep the whole set in **one branch/PR** so the catalogue count and slug-set test bump once.

Video-sourced courses: fetch transcripts with the `youtube-playlist` skill and follow the video-lesson anatomy (Summary / Main ideas / Mindmap body below the player). Context/topic courses: text lessons with a mermaid diagram + examples each.

## Step 3 — Path-creation CLI

Copy `templates/create_path_template.py` to `backend/src/cyberdyne_backend/cli/create_<track>_path.py` (companion to `create_computer_engineering_path.py`). Fill in `MODULES` (each bundling its `courseSlugs`), `PATH` (ordered `moduleSlugs`), and the pt-BR/es/fr **module + path** translations. It is a run-once, idempotent admin-API helper that:

1. creates each module (`POST /admin/learning/modules`; 409 → exists, skip),
2. creates the path (`POST /admin/learning/paths`; 409 → exists) **or**, when the path already exists, PATCHes its `moduleSlugs` to include the new modules (so re-running or extending an existing track is safe),
3. PUTs the module and path translations (pt-BR/es/fr).

Add a `build_payloads()` purity test in `tests/unit/test_learning_admin_crud.py` (mirror `test_computer_engineering_payloads_are_valid`): every module level is valid, the path references only modules built here, and every bundled `courseSlug` is a real seeded course in `ACADEMY_COURSES`.

## Step 4 — Quality gate + ship

Per create-academy-course Step 4: `ruff format` + `ruff check`, `lint-imports`, `pytest -q --cov` (≥90%). Branch → commit → PR → wait for the Quality gate → squash-merge → auto-deploy seeds and publishes every course.

## Step 5 — Live apply (needs admin auth)

After the deploy provisions the courses:

```bash
# 1. create the path + modules + module/path translations
ACADEMY_EMAIL=... ACADEMY_PASSWORD=... ACADEMY_INSECURE_TLS=1 \
  uv run python -m cyberdyne_backend.cli.create_<track>_path

# 2. translate each course's CONTENT (one job per course per language)
for slug in <course-1> <course-2> ...; do
  for lang in pt-BR es fr; do
    curl -sk -X POST ".../api/v1/admin/courses/$slug/translations/$lang" -H "Authorization: Bearer $TOKEN"
  done
done
# poll .../admin/courses/<slug>/translations until each is done
```

Auth + hosts: see **create-academy-course** (Hosts & auth reference) and the `academy-admin-live-apply-auth` memory.

## Step 6 — Verify live

Use **list-learning-tracks**: `python3 .claude/skills/list-learning-tracks/list_tracks.py --track <slug>` shows the new path with its ordered modules → courses. Confirm ordering with **reorder-learning-track** if you want to fine-tune the progression. Spot-check a course (`GET /courses/<slug>`) and a translated read (`?lang=pt-BR`) keep the `##` sections and ` ```mermaid ` blocks.

## Extending an existing track

If the path already exists, don't recreate it — the CLI PATCHes `moduleSlugs` to append the new modules. To slot a course into an **existing module** instead (like adding a fundamentals course to a tool stage), PATCH that module's `courseSlugs` (see the `add_devops_fundamentals_to_ce_devops` CLI) rather than adding a new module.

## Guardrails

- **Confirm scope first** — a track is many courses and a large PR; agree on the course/module list before authoring.
- Every hard rule from create-academy-course still applies to each course (one-correct-option quizzes, stable titles, RUF001 typography, constrained mermaid).
- Keep all the track's courses in one PR so the catalogue-count and slug-set tests bump once and stay green.
