---
name: improve-academy-course
description: Update, improve, or complement an EXISTING Cyberdyne Academy course or a single lesson, given its title (or slug). Edits the version-controlled seed file in place, respecting the title-as-reconciliation-key rules, then ships it through PR -> auto-deploy and re-translates only what changed. Use when the user asks to "fix / rewrite / expand / add a lesson to / improve / update the <course or lesson> lesson/course", NOT when creating a brand-new course (use create-academy-course) or a whole track (use create-learning-track).
---

# Improve an Academy Course

Changes **content that already ships**: rewrite a lesson body, fix an error, add examples, add or remove lessons, tune quizzes - for one course or one lesson identified by its **title**. Courses are version-controlled seed files that reconcile **by lesson title** on every deploy, so most edits are safe and in-place; the sharp edges are renames and removals. Follow this in order.

This skill **composes** the others - do not duplicate their rules, invoke them:
- **list-learning-tracks** - locate the course and its slug/track from a title.
- **create-academy-course** - the house lesson pattern and every hard production rule; all of them still apply to edited/added lessons. Read its "Step 1" before editing.

Creating a NEW course? Use **create-academy-course**. A whole new track? **create-learning-track**. Reordering modules? **reorder-learning-track**.

## The reconciliation model (read this first - it defines what is safe)

On every deploy the boot seed reconciles each course **by lesson title**, non-destructively:

| Edit | Effect on deploy | Safe? |
| --- | --- | --- |
| Change a lesson **body** (same title) | Updated in place | Yes - the common case |
| **Add** a lesson (new title) | Inserted at its position | Yes |
| **Rename** a lesson title | Creates a NEW lesson; the old title stays as an orphan | No - avoid; treat as remove+add |
| **Remove** a lesson | Leaves the old lesson **live** (orphaned) | Needs manual cleanup (Step 5) |
| Reorder lessons within the course | Order follows the seed tuple | Yes |

So: **editing bodies and adding lessons is easy; renaming and removing require the post-deploy cleanup in Step 5.** Prefer editing a body over renaming a title.

## Step 1 — Locate the course/lesson and read the current content

1. From the title, find the course slug: `python3 .claude/skills/list-learning-tracks/list_tracks.py --json` (or `GET /api/v1/learning/paths`), or search the seed files: `grep -rl "title=\"<course title>\"" backend/src/cyberdyne_backend/application/courses/seed_*.py`.
2. The seed file is `backend/src/cyberdyne_backend/application/courses/seed_<slug-with-underscores>.py`. Read it in full - it is the source of truth.
3. Read the **live** current content to confirm what is deployed (auth token needed for full bodies): `GET /api/v1/courses/<slug>` (see create-academy-course "Hosts & auth reference"). Diff intent against what is actually live.
4. For a **single-lesson** request, find that exact lesson in the tuple by its title.

## Step 2 — Edit the seed file in place

Make the change directly in `seed_<slug>.py`. Every hard rule from **create-academy-course** Step 1 still holds for anything you touch:

- Every quiz question keeps **exactly one** `opt(correct=True)` and >= 2 options.
- **No en dashes or curly quotes** (RUF001); constrained mermaid grammar (quoted `graph` labels; strict `mindmap` for video companions).
- `text`/`code` lessons need a non-empty body; `video` needs `content_url`.
- Keep the house ordering: every content lesson **immediately followed by its `quiz_lesson("Quiz: <title>", ...)`**, and the final `"Check your knowledge"` quiz **last**.

Guidance per kind of change:
- **Improve a body**: keep the title identical (it is the key). Rewrite the markdown, keep/adjust the one mermaid diagram and the code/formula example.
- **Complement (add lessons)**: insert `_t(...)`/`video_lesson(...)` + its `quiz_lesson(...)` at the right spot, before the final quiz. For a video lesson, fetch the transcript with the `youtube-playlist` skill and follow the Summary / Main ideas / Mindmap anatomy.
- **Fix a quiz**: edit options/`correct=`/`explanation` in place; do not change the quiz lesson's title.
- **Remove a lesson**: delete its `_t/video_lesson` AND its paired `quiz_lesson` from the tuple - then do Step 5 cleanup after deploy.
- **Avoid renames.** If a title must change, treat it as remove-old + add-new and clean up the orphan in Step 5.

## Step 3 — Update the tests

- The catalogue count `assert len(summary) == N` in `test_courses_seed.py` counts **courses**, not lessons - it only changes if you add/remove a whole course (you are not), so leave it.
- If the course has a **shape test** (e.g. `test_<slug>_course_shape` asserting an exact `len(course.lessons) == K` and text/video counts), update those numbers when you add or remove lessons.
- If you added/removed **video mindmaps** covered by `test_ai_course_mindmaps_use_strict_mermaid_syntax` (or a per-course strict-mindmap check), bump its expected diagram count.
- If the course has no shape test and you changed its lesson count, add a minimal one (mirror an existing `test_*_course_shape`) so the new structure is guarded.
- The one-correct-option guard (`test_every_registry_quiz_question_has_exactly_one_correct_option`) already covers every edited quiz - keep it green.

## Step 4 — Quality gate + ship

Per create-academy-course Step 4, from `backend/`:

```bash
uv run ruff format <changed files> && uv run ruff check src tests
uv run lint-imports
uv run mypy src
uv run pytest --cov --cov-report= --cov-fail-under=90   # CI-exact
```

Branch (never commit on `main`) -> commit (no AI mentions) -> PR with a body that says what changed and why -> wait for the Quality gate -> squash-merge. Merging auto-deploys and the boot seed reconciles the edits.

## Step 5 — Post-deploy cleanup (only for removes/renames)

Deploys never delete lessons, so a removed or renamed title stays live as an orphan. After the deploy provisions the edit, delete each orphan by id (needs editor auth):

```bash
# find the live lesson id of the orphaned title
curl -sk "https://dao.backend.coolify.cyberdynecorp.ai/api/v1/courses/<slug>" -H "Authorization: Bearer $TOKEN" \
  | jq '.lessons[] | {id, title}'
# delete it
curl -sk -X DELETE "https://dao.backend.coolify.cyberdynecorp.ai/api/v1/admin/courses/<slug>/lessons/<lesson-id>" \
  -H "Authorization: Bearer $TOKEN"
```

Body-only edits and pure additions need **no** cleanup - skip this step.

## Step 6 — Re-translate what changed

The in-app translation job is **incremental (source-hash keyed)**: re-running only re-translates lessons whose source changed. Trigger it for each supported language so the edit reaches pt-BR/es/fr:

```bash
for lang in pt-BR es fr; do
  curl -sk -X POST ".../api/v1/admin/courses/<slug>/translations/$lang" -H "Authorization: Bearer $TOKEN"
done
# poll .../admin/courses/<slug>/translations until each job is done
```

## Step 7 — Verify live

```bash
# the edited body/structure is live (auth => full bodies)
curl -sk "https://dao.backend.coolify.cyberdynecorp.ai/api/v1/courses/<slug>" -H "Authorization: Bearer $TOKEN"
# translated read keeps the ## sections and ```mermaid blocks
curl -sk "https://dao.backend.coolify.cyberdynecorp.ai/api/v1/courses/<slug>?lang=pt-BR" -H "Authorization: Bearer $TOKEN"
```

Confirm: the intended lesson body changed, no duplicate titles appeared (rename slip), every content lesson is still followed by its quiz, the final quiz is last, and (for removes) the orphan is gone.

## Guardrails

- **Title is the key** - edit bodies freely, but a changed title is a new lesson. When in doubt, keep the title and change only the body.
- **Every fix needs its regression covered** - a quiz fix is covered by the one-correct-option guard; a structural change needs the shape-test numbers updated. Do not merge on red CI.
- **Scope to what was asked** - improving one lesson means touching one lesson; do not silently rewrite the whole course.
- Hosts, auth, and the test editor account: see **create-academy-course** and the `academy-admin-live-apply-auth` / `academy-live-apply-hosts` memories.
