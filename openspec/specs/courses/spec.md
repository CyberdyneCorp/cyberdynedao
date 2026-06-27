# courses Specification

## Purpose

The Academy course catalogue: courses + ordered lessons + categories, learner
progress with per-course completion, course-level deadlines, completion
certificates, and i18n. Public read + editor authoring. (src:
adapters/inbound/api/courses/router.py, domain/courses, persistence/courses)

## Requirements

### Requirement: Public catalogue with draft gating

The system SHALL expose `GET /api/v1/courses` (filterable by `level`) and
`GET /api/v1/courses/{slug}`. A course SHALL be public iff `status ==
"published"`; drafts SHALL be hidden from non-editors and a draft/missing
slug SHALL return `404`. For an unauthenticated viewer of a published course,
the full lesson syllabus SHALL be returned but only the first lesson's body;
lessons 2+ SHALL have their body/content stripped. Authenticated viewers SHALL
receive all lesson bodies.

`GET /api/v1/courses` SHALL accept optional `limit` (1..200) and `offset`
(>=0) query params that page the catalogue, applied to the courses before
their lessons are loaded. Omitting `limit` SHALL return the full catalogue and
the response SHALL remain a bare array ordered by `(level, sort_order, title)`
either way, so existing clients are unaffected.

#### Scenario: Guest sees syllabus but only first lesson body

- GIVEN a published course with 3 lessons
- WHEN an anonymous user GETs the course
- THEN all 3 lesson titles are present but only lesson 1 has a body

#### Scenario: Paged catalogue

- GIVEN three published courses
- WHEN a client GETs `/api/v1/courses?limit=2&offset=2`
- THEN only the third course is returned, as a bare array, and an out-of-range
  `limit`/`offset` returns `422`

#### Scenario: Draft hidden from public

- GIVEN a draft course
- WHEN an anonymous user lists courses
- THEN the draft does not appear

### Requirement: Editor authoring

The system SHALL allow an `editor` to create/update/publish/unpublish/delete
courses, add/update/delete/reorder lessons, and manage categories, under
`/api/v1/admin/...`. A course slug SHALL be auto-derived from the title when
omitted, be unique (duplicate → `409`), and be immutable; the level SHALL be
immutable after creation. Lesson content SHALL satisfy its type invariant
(e.g. `video` requires a `content_url`, `text` requires a `text_body`),
returning `422` otherwise.

#### Scenario: Create defaults to draft with derived slug

- GIVEN an editor creates a course titled "Solidity 101" with no slug
- WHEN the request succeeds
- THEN the course exists as a draft with slug `solidity-101`

#### Scenario: Lesson type invariant enforced

- GIVEN a `video` lesson submitted without a `content_url`
- WHEN an editor creates it
- THEN the system SHALL respond `422`

### Requirement: Category hierarchy

The system SHALL support one level of category nesting (a category may have a
top-level parent). A category SHALL NOT be its own parent, and a parent SHALL
itself be top-level (else `422`). Deleting a category SHALL set referencing
courses to uncategorized and promote child categories to top-level.

#### Scenario: Self-parenting rejected

- GIVEN a category
- WHEN an editor sets the category's parent to itself
- THEN the system SHALL respond `422`

### Requirement: Lesson progress and course completion

The system SHALL record per-lesson progress (`PUT
/api/v1/courses/{slug}/lessons/{id}/progress`, percent 0..100, else `422`) for
the authenticated learner, maintaining the invariant that `completed_at` is
set iff `percent == 100`. Course progress SHALL aggregate completed lessons /
total lessons; a course SHALL be `completed` iff it has lessons and all are at
100%. `GET /api/v1/courses/{slug}/progress` SHALL require a user (403 if
anonymous); `GET /api/v1/courses/me/progress` SHALL list only started courses.

#### Scenario: Partial progress does not complete

- GIVEN a course with 2 lessons
- WHEN a learner sets lesson 1 to 60%
- THEN course progress reports 0 completed lessons and 0% complete

#### Scenario: Completing the last lesson completes the course

- GIVEN a 2-lesson course with lesson 1 at 100%
- WHEN the learner sets lesson 2 to 100%
- THEN course progress reports `completed = true`

### Requirement: Course-level deadlines

The system SHALL let an editor set/clear a course `due_at` (`PUT
/api/v1/admin/courses/{slug}/deadline`, null clears). The course read SHALL
derive a `deadlineStatus` (`none`/`upcoming`/`urgent`/`overdue`) and
`daysRemaining` at read time from `due_at` vs now.

#### Scenario: Overdue derived at read time

- GIVEN a course whose `due_at` is in the past
- WHEN the course is read
- THEN `deadlineStatus` is `overdue` with a negative `daysRemaining`

### Requirement: Completion certificates

The system SHALL issue a course completion certificate
(`POST /api/v1/courses/{slug}/certificate`) only when every lesson is
complete (else `409`); issuance SHALL be idempotent. The certificate SHALL be
publicly verifiable by id (`GET /api/v1/courses/certificates/{id}/verify`,
returning `{valid, certificate}` and never `404`) and downloadable as a PDF
(`…/pdf`, `404` if missing).

#### Scenario: Issue requires full completion

- GIVEN a learner who has not completed every lesson
- WHEN they request a certificate
- THEN the system SHALL respond `409`

#### Scenario: Verify an unknown certificate id

- GIVEN a certificate id that does not exist
- WHEN it is verified
- THEN the system SHALL respond `200` with `{valid: false, certificate: null}`

### Requirement: Localized content

The system SHALL store course/lesson text in English with per-language
overrides, falling back to English when a translation is absent, and let an
editor enqueue an async translation job
(`POST /api/v1/admin/courses/{slug}/translations/{language}`) — rejecting an
unsupported/English language with `422` and an unconfigured LLM with `503`.

A language SHALL count as `available` (`GET /api/v1/admin/courses/{slug}/translations`)
only when the course title/description and every lesson and quiz question are
translated. To keep a never-completing language diagnosable, that endpoint
SHALL also surface the per-language translation-job state (`jobs[]` with
`status`/`attempts`/`error`), where `error` names the specific field(s) that
failed. A long, code-heavy lesson body SHALL be translated in bounded chunks
so the model does not truncate its output and drop protected spans; a field
that still fails SHALL be recorded (not silently skipped) and retried, and the
job SHALL settle as `failed` with a diagnosable error after the attempt cap
rather than reporting `done` while a field is missing.

#### Scenario: Fallback to English

- GIVEN a course with no French translation
- WHEN it is read with locale `fr`
- THEN the English title/description are returned

#### Scenario: Failing lesson is diagnosable, not silent

- GIVEN a course whose translation job keeps failing on one lesson body
- WHEN the editor reads `GET /api/v1/admin/courses/{slug}/translations`
- THEN the language is absent from `available` AND `jobs[]` reports that
  language as `failed` with an `error` naming the failing lesson
