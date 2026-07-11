---
name: reorder-learning-track
description: Reorder the modules of a Cyberdyne Academy learning track, taking the existing courses into account. Shows the current order with each module's courses, validates the new order is a permutation of the existing modules, applies it via the admin reorder endpoint, and verifies live. Use when the user asks to "reorder/rearrange a learning track/path", "move a course/module up or down in a track", or "sort a track by level".
---

# Reorder a Learning Track

A track's order is the order of its **modules** (each module bundles one or more courses). This skill reorders those modules safely: it never adds or drops a module (the admin endpoint requires a **permutation** of the existing set), it shows you the current order with the courses so you can decide, and it verifies the result after writing.

## Step 1 — Look at the current order (no auth)

```bash
python3 .claude/skills/reorder-learning-track/reorder_track.py show computer-engineering
```

Prints each module in order with its level and the course slugs it bundles. (For the full track catalogue, use the **list-learning-tracks** skill.) List live track slugs with `GET /api/v1/learning/paths`.

## Step 2 — Apply a new order (needs editor/admin auth)

Three ways to express the new order — pick one:

```bash
# a) Move one module to a 1-based position; everything else keeps its order.
python3 .claude/skills/reorder-learning-track/reorder_track.py apply computer-engineering \
    --move gpu-programming-cuda-opencl --to 10

# b) Sort by module level (Beginner -> Intermediate -> Advanced), stable within a level.
python3 .claude/skills/reorder-learning-track/reorder_track.py apply computer-engineering \
    --sort-by-level

# c) Give the exact full order (comma-separated module slugs — must be every module).
python3 .claude/skills/reorder-learning-track/reorder_track.py apply computer-engineering \
    --order computing-foundations,technical-english,ce-foundations,...
```

Auth (same scheme as the academy CLIs — see [[academy-admin-live-apply-auth]]):

```bash
ACADEMY_EMAIL=... ACADEMY_PASSWORD=... ACADEMY_INSECURE_TLS=1 \
  python3 .claude/skills/reorder-learning-track/reorder_track.py apply <track> --move <slug> --to <n>
# or ACADEMY_TOKEN=<bearer>
```

`apply` prints the reorder plan (marking moved modules), asks to confirm (skip with `--yes`), POSTs to `/api/v1/admin/learning/paths/{slug}/modules/reorder`, then re-reads the track to confirm the live order matches.

## Safety / behavior

- **Permutation-guarded.** If the requested order isn't exactly the current module set, it refuses and shows what was dropped/unknown — before any write. This is also the endpoint's own rule (`422` otherwise).
- **No-op detected.** If the order already matches, it does nothing.
- **Reorder ≠ add/remove.** To add a course/module to the track use **create-academy-course** (Step 3); to remove one, PATCH the path's `moduleSlugs`. This skill only permutes.
- Reordering preserves ids/progress — it only changes `sort_order`.

## Config

`ACADEMY_API_BASE` (default `https://dao.backend.coolify.cyberdynecorp.ai`), `ACADEMY_AUTH_BASE`, `ACADEMY_INSECURE_TLS=1`.

## Related

Start with **list-learning-tracks** to see all tracks and their courses; use **create-academy-course** to add a course to a track.
