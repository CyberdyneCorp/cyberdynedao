# lesson-notes Specification

## Purpose

Per-user, lesson-scoped annotations — an optional highlighted quote plus
the learner's note body — that the Learn client syncs from on-device
storage. A precise slice of the broader notebook capability, with a
client-supplied id so re-sync is idempotent. (src:
adapters/inbound/api/lesson_notes, application/lesson_notes,
domain/lesson_notes — issue #188)

## Requirements

### Requirement: Idempotent create/sync

The system SHALL create a lesson note via `POST /api/v1/lessons/{lesson_id}/notes`
(`{ courseSlug, body, quote?, id? }`), scoped to the authenticated user. A
client MAY supply the note `id`; if a note with that `(user, id)` already
exists it SHALL be updated in place (no duplicate) and the response status
SHALL be `200`, otherwise `201`. An empty body SHALL return `422`.

#### Scenario: Re-syncing a client id does not duplicate

- GIVEN a client created a note with id `X`
- WHEN it POSTs again with the same id `X` and a new body
- THEN the system SHALL respond `200`, update the note in place, and keep a single row

#### Scenario: First create

- GIVEN a client POSTs a note without an id (or with a new id)
- WHEN the request is valid
- THEN the system SHALL respond `201` with the created note

### Requirement: List by lesson and across a course

The system SHALL list the user's notes for one lesson
(`GET /api/v1/lessons/{lesson_id}/notes`) and across all/one course
(`GET /api/v1/notes?courseSlug=&cursor=`, keyset-paged for export/search),
newest-first, scoped to the user.

#### Scenario: List a lesson's notes

- GIVEN a user has notes on lesson `l1`
- WHEN they GET `/api/v1/lessons/l1/notes`
- THEN only their `l1` notes are returned, newest first

### Requirement: Update and delete

The system SHALL allow `PATCH /api/v1/notes/{id}` (change `body` and/or
`quote`) and `DELETE /api/v1/notes/{id}`, scoped to the owning user; a
missing/other-user note SHALL return `404`. A PATCH SHALL change only the
fields provided — an omitted `quote` is left untouched while an explicit
`quote: null` clears it.

#### Scenario: Explicit null clears the quote

- GIVEN a note with a quote
- WHEN the user PATCHes it with `quote: null`
- THEN the quote is cleared

#### Scenario: Cross-user access is denied

- GIVEN one user's note
- WHEN another user PATCHes or DELETEs it by id
- THEN the system SHALL respond `404`
