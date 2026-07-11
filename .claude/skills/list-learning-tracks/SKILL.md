---
name: list-learning-tracks
description: List all Cyberdyne Academy learning tracks and the courses inside each (ordered modules → bundled courses). Read-only, no auth. Use when the user asks "what learning tracks/paths do we have", "what courses are in the Computer Engineering track", "show the track catalogue", or before reordering a track.
---

# List Learning Tracks

Prints every learning track (path) with its **ordered modules** and, under each module, the **courses it bundles** (title, slug, level). Read-only — it hits the **public** learning API, so no credentials are needed.

## Run it

```bash
python3 .claude/skills/list-learning-tracks/list_tracks.py            # all tracks
python3 .claude/skills/list-learning-tracks/list_tracks.py --track computer-engineering
python3 .claude/skills/list-learning-tracks/list_tracks.py --lang pt-BR   # localized titles
python3 .claude/skills/list-learning-tracks/list_tracks.py --json         # machine-readable
python3 .claude/skills/list-learning-tracks/list_tracks.py --orphans      # + courses in NO track
```

`--track <slug>` limits to one track. `--lang pt-BR|es|fr` returns localized module/path titles. `--json` emits `{tracks: [...], coursesInNoTrack?: [...]}`. `--orphans` also lists catalogue courses that no module bundles (useful before deciding what to add to a track).

## What it does

Joins two public endpoints (see [[create-academy-course]] for the API map):
- `GET /api/v1/learning/paths` — tracks with their ordered `moduleSlugs`.
- `GET /api/v1/learning/modules` — each module's `courseSlugs` **and** resolved `courses` cards (`slug`, `title`, `level`), locale-aware.

For each track it walks `moduleSlugs` in order, resolves each module, and lists its courses. A module slug with no matching module shows `(missing module)`; a module that bundles courses the catalogue didn't resolve shows the raw `courseSlugs`.

## Config

`ACADEMY_API_BASE` (default `https://dao.backend.coolify.cyberdynecorp.ai`) and `ACADEMY_INSECURE_TLS=1` for self-signed TLS — same scheme as the other academy helpers.

## Related

To change a track's module order, use the **reorder-learning-track** skill (it starts by showing this same view). To add a course to a track, see **create-academy-course** (Step 3).
