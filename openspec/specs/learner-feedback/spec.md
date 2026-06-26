# learner-feedback Specification

## Purpose

A general feedback channel for signed-in learners to report problems and
request features, with an admin triage queue. Distinct from per-quiz feedback
and from the course/topic demand registry (which captures wanted courses).
(src: adapters/inbound/api/feedback/router.py, domain/feedback)

## Requirements

### Requirement: Submit feedback

The system SHALL let any authenticated learner submit feedback
(`POST /api/v1/feedback`) with a `kind` (`problem`/`feature`), a non-empty
`message` (≤4000 chars), and optional in-context references (`courseId`,
`lessonId`, `appVersion`, `platform`). It SHALL persist the item with
`status` `new` and return the created item (`201`). The channel SHALL be open
to all signed-in learners (free and Pro); it SHALL NOT be gated. An unknown
`kind` SHALL return `422`.

#### Scenario: Problem report is captured

- GIVEN an authenticated learner
- WHEN they POST `{kind: "problem", message: "Quiz 4 has no correct answer"}`
- THEN the system SHALL respond `201` with `kind: "problem"` and `status: "new"`

#### Scenario: Unknown kind rejected

- GIVEN an authenticated learner
- WHEN they POST a feedback item with `kind: "complaint"`
- THEN the system SHALL respond `422`

### Requirement: Admin triage queue

The system SHALL let an admin/editor list submitted feedback
(`GET /api/v1/admin/feedback`), newest first, filterable by `kind` and/or
`status` (`new`/`triaged`/`closed`). Non-admins SHALL be refused (`401`/`403`).

#### Scenario: Filter the queue by kind

- GIVEN a problem and a feature have been submitted
- WHEN an admin GETs `/api/v1/admin/feedback?kind=problem`
- THEN only the problem item is returned

#### Scenario: Non-admin refused

- GIVEN an unauthenticated caller
- WHEN they GET `/api/v1/admin/feedback`
- THEN the system SHALL respond `401` or `403`
