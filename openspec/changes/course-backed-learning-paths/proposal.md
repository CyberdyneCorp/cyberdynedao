## Why

Learning paths today are ordered lists of **modules**, but a module is a standalone "milestone card" (title/level/duration/topics) with **no link to a course** — its progress is self-reported (`PATCH /learning/modules/{slug}/progress`). So you cannot build an "Engineering" path out of the real courses (lessons, quizzes, certificates) in the catalogue, and the learner web UI doesn't surface paths at all. We want a path to be an ordered set of **stages**, where each stage bundles one or more real courses, and completion/certificate fall out of finishing those courses.

## What Changes

- **A module becomes a course-backed stage.** Add `courseSlugs: string[]` to a learning module. A module may bundle one or more courses (1:many); its display metadata (title, level, duration, icon, topics) stays as the stage label.
- **Module completion is derived, not self-reported.** For a module with `courseSlugs`, a user completes it when **every linked course is complete** (course progress 100% / all lessons done); module percent is derived from its courses' completion. Modules with **no** linked courses keep the legacy self-reported percent (backward compatible — the 12 seeded modules keep working unchanged).
- **Path gating, eligibility, and certificates** keep operating on modules, now reading derived completion, so an ordered path of stages gates and certifies off real course progress.
- **Admin**: assign/unassign courses to a module (set `courseSlugs` on create/update); each slug is validated against existing courses (422 on unknown). The admin UI gains a course multi-select per module.
- **Learner UI**: a new **Learning Paths** view in the Learn window — browse paths, enroll, see each stage and its courses with lock/unlock gating and a "next course", and claim the path certificate on completion.
- Public path/module responses expose `courseSlugs` (and a lightweight expansion of the linked courses' title/slug/level for rendering).

Non-goals: changing the course/lesson/quiz model itself; removing the legacy self-reported module behavior; reworking course categories.

## Capabilities

### New Capabilities
<!-- none -->

### Modified Capabilities
- `learning-paths`: a module gains an optional set of linked courses; module completion (and therefore path gating/eligibility/certificate) is derived from linked-course completion when present; editors assign courses to modules; learners browse and progress a path of real courses.

## Impact

- **Data**: migration adds `course_slugs` (JSON, default `[]`) to `learning_modules`. No change to courses.
- **Backend**: `domain/learning` (module entity + completion derivation), `application/learning` (state/gating/eligibility/certificate read derived completion; admin use-cases validate course slugs), persistence (new column + read/write), API schemas/routers (request + response `courseSlugs` + expanded courses). Cross-context read of course progress required (a learning→courses query port).
- **Frontend**: `adminApi`/`learningAdminViewModel`/`LearningPathsAdmin.svelte` (course multi-select per module); a new learner `LearningPathsView` + viewmodel + `coursesApi` path read functions; ViewRouter wiring.
- **Tests**: completion-derivation unit tests, admin course-validation tests, API tests (assign courses, derived gating, path certificate), learner viewmodel tests, and a regression that legacy course-less modules still self-report.
- Builds on the admin-CRUD foundation in PR #205 (paths/modules are already API-manageable).
