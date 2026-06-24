## 1. Storage + domain

- [ ] 1.1 Migration: add `course_slugs` (JSON, NOT NULL, default `[]`) to `learning_modules`
- [ ] 1.2 `LearningModule` gains `course_slugs: tuple[str, ...]`; `new_module` accepts/normalizes it
- [ ] 1.3 Completion source helper: `module_completion(module, completed_course_slugs, percent_by_course, self_reported)` → (percent, is_completed); derived when `course_slugs`, else self-reported

## 2. Cross-context read ports

- [ ] 2.1 Define a learning-owned port for course reads: `course_exists` / `list_course_slugs` (validation) and `completed_course_slugs(user_id)` / `percent_by_course(user_id)` (completion)
- [ ] 2.2 Implement the port over the existing courses + course-progress repositories (no change to the courses context; keep lint-imports green)

## 3. Application

- [ ] 3.1 Module create/update use-cases validate `course_slugs` against existing courses (422 on unknown), mirroring path moduleSlugs validation
- [ ] 3.2 `GetMyLearningState`, gating, eligibility, and certificate eligibility assemble module completion from the derived source (course-backed) or self-reported (legacy)

## 4. API

- [ ] 4.1 Admin module schemas accept `courseSlugs`; create/update plumb it through
- [ ] 4.2 Public module/path responses add `courseSlugs` + expanded `courses: [{slug,title,level}]`
- [ ] 4.3 Confirm OpenAPI documents the new fields

## 5. Admin UI

- [ ] 5.1 `adminApi` + `learningAdminViewModel`: carry `courseSlugs` on module create/edit
- [ ] 5.2 `LearningPathsAdmin.svelte`: per-module course multi-select (from existing courses); show a module's linked courses

## 6. Learner UI

- [ ] 6.1 `coursesApi`: `fetchLearningPaths`, `fetchPathGating`, `enrollInPath`, types
- [ ] 6.2 `learningPathsViewModel` + tests
- [ ] 6.3 `LearningPathsView.svelte`: list/enroll paths; per-stage courses with gating, next course, certificate; route to course player
- [ ] 6.4 Wire into ViewRouter / Learn window

## 7. Tests + verify

- [ ] 7.1 Domain/use-case: derived completion (all-courses-complete gate; partial = mean), legacy self-report unchanged, unknown-course 422
- [ ] 7.2 API tests: assign courses to a module; derived gating; path certificate on all-courses-complete
- [ ] 7.3 Frontend: learningPathsViewModel + admin course-assign tests; `npm run check` + `npm run test`
- [ ] 7.4 Backend gate: ruff + mypy + lint-imports + pytest (diff vs main); regression that seeded 5 paths + 12 modules still work
- [ ] 7.5 `openspec validate course-backed-learning-paths --strict`
