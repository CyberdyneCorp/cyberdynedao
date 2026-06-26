# course-demand Specification

## Purpose

A demand registry capturing learner requests for courses/topics we don't yet
offer, from two entry points (a typed "Request a course/topic" and a
Scan-to-Learn photo that found no matching course) into one store. Requests are
clustered by a normalized topic key so the authoring backlog shows ranked
demand. Demand capture only — no authoring/publishing happens here.
(src: adapters/inbound/api/course_demand/router.py, domain/course_demand)

## Requirements

### Requirement: Capture course/topic requests

The system SHALL let any authenticated learner submit a course/topic request
(`POST /api/v1/learning/course-requests`) with a `topic`, a `source`
(`typed`/`scan`), and optional `subject`, `sourceQuestionText`, `courseId`,
`lessonId`. It SHALL persist the request and return an acknowledgement
(`201`). The channel SHALL be open to all signed-in learners (not gated). An
unknown `source` SHALL return `422`.

#### Scenario: Typed request captured

- GIVEN an authenticated learner
- WHEN they POST `{topic: "Eigenvalues", source: "typed"}`
- THEN the system SHALL respond `201` with the normalized `topicKey`

### Requirement: Clustered ranked demand

The system SHALL cluster requests by a normalized topic key (lower-cased,
punctuation removed, whitespace collapsed) so a typed request and a scan
no-match for the same topic land in one cluster. An admin/editor SHALL read the
clustered backlog (`GET /api/v1/admin/learning/course-requests`) ordered by
request count (most-wanted first). Non-admins SHALL be refused (`401`/`403`).

#### Scenario: Typed + scan for the same topic cluster together

- GIVEN a typed request for "Eigenvalues" and a scan no-match for "eigenvalues?"
- WHEN an admin reads the clustered backlog
- THEN both requests appear in a single cluster with `count` 2

#### Scenario: Backlog ranked by demand

- GIVEN topic A was requested 3 times and topic B once
- WHEN an admin reads the clustered backlog
- THEN topic A is ranked above topic B
