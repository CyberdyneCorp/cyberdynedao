## Context

After PR #205, learning modules and paths are admin-CRUD resources, but a module is course-unaware: it carries display metadata and a self-reported progress percent, and paths/gating/certificates run off that percent. Courses (lessons, quizzes, certificates, progress) are a separate bounded context. This change links the two so a path becomes an ordered set of course-backed stages.

## Goals / Non-Goals

**Goals:**
- A module can bundle ≥1 course (`courseSlugs`); completion derives from those courses.
- Reuse the existing path gating / eligibility / certificate machinery unchanged in shape — only the *source* of a module's completion changes.
- Backward compatible: course-less modules keep self-reported progress; the seeded 5 paths + 12 modules keep working.
- A learner-facing Learning Paths view.

**Non-Goals:**
- Changing courses/lessons/quizzes. No change to course categories. No removal of self-reported module progress.

## Decisions

- **Storage**: add `course_slugs JSON NOT NULL DEFAULT '[]'` to `learning_modules` (migration). The domain `LearningModule` gains `course_slugs: tuple[str, ...]`.
- **Completion source (the crux)**: a module's per-user completion becomes a function `module_percent(module, course_progress)`:
  - if `course_slugs` is non-empty → derived: `100` iff every linked course is complete for the user, else a derived partial (e.g. mean of linked-course percents); `is_completed` iff all linked courses complete.
  - else → the existing `ModuleProgress` self-reported percent.
  This keeps `compute_path_gates`, eligibility, and `certificate_eligible` intact — they consume a `{module_slug: completed?}`/percent view that is now assembled from the derived source. The assembly happens in the application layer (`GetMyLearningState`/gating/eligibility/certificate), not the domain gating function.
- **Cross-context read**: the learning application needs each course's completion for a user. Introduce a thin read port (e.g. `CourseProgressReader.completed_course_slugs(user_id) -> set[str]` / `percent_by_course`) implemented over the existing courses progress repository — learning depends on a port, not on the courses adapter (keeps hexagonal layers; lint-imports stays green).
- **Course-slug validation**: admin module create/update validates `course_slugs` against the course repository via a small reader port (`course_exists`/`list_course_slugs`), mirroring how path `moduleSlugs` are validated against modules. Unknown → `LearningContentValidationError` → 422.
- **API responses**: module/path responses add `courseSlugs` + an expansion list `courses: [{slug,title,level}]` (resolved from the course repo at read time, or joined). Keeps the iOS client and the new web view able to render without N extra calls.
- **Admin UI**: `LearningPathsAdmin` gains a course multi-select per module (checkbox list of existing courses, reusing the courses list already loaded by the admin). The viewmodel sends `courseSlugs` on create/edit.
- **Learner UI**: a new `LearningPathsView` + `learningPathsViewModel` + `coursesApi` read functions (`fetchLearningPaths`, `fetchPathGating`, `enrollInPath`). Stages render their courses; clicking a course routes to the existing course player; gating/eligibility/certificate come from existing endpoints. Surfaced as a new Learn sub-view (ViewRouter `content` value or a tab in the Learn window).

## Risks / Trade-offs

- **Derived partial percent** is a presentation choice; the load-bearing rule is the all-courses-complete gate. We'll define partial percent as the mean of linked-course percents (documented), avoiding a false "100%".
- **Cross-context coupling**: learning now reads course progress. Mitigated by a narrow port owned by the learning context; the courses context is untouched.
- **Mixed modules** (some course-backed, some legacy self-reported) coexist in one path — supported by the per-module branch in the completion source; documented so it's intentional, not surprising.
- **Performance**: resolving course expansions + per-user course completion for a path adds queries; batch by loading the user's completed-course set once per request.
