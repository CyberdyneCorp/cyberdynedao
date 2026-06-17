# notebook Specification

## Purpose

The learner's per-user "living memory": saved notes (concepts, executed
code + run results/plots, summaries, theory, problems), flashcards, a
spaced-review schedule, and LLM-assisted generation. All routes are scoped
to the authenticated user. (src: adapters/inbound/api/notebook,
application/notebook, domain/notebook — issues #161, #187)

## Requirements

### Requirement: Notes CRUD

The system SHALL let an authenticated user create, list/search, fetch,
update, and delete notes under `/api/v1/notebook/notes`, scoped to that
user. A note carries a title, type (`lesson`/`lab`/`code`/`simulation`/
`theory`/`problem`), markdown body, optional `courseSlug`/`lessonId`, a
saved-from-the-Lab payload (`code` + `language` + `runResult` + `plotRefs`),
and `tags`. List is newest-first, keyset-paged, filterable by `type` and a
`q` title/body substring; an unknown `type` SHALL return `422`, a missing or
other-user note `404`.

#### Scenario: Create then fetch is user-scoped

- GIVEN a user creates a note with code + run result
- WHEN another user fetches it by id
- THEN the system SHALL respond `404`

### Requirement: Flashcards

The system SHALL let the user add, list, and delete flashcards on a note
they own (`/api/v1/notebook/notes/{id}/flashcards`). Each flashcard
operation SHALL first verify note ownership (`404` otherwise); question and
answer are 1..2000 chars (`422` otherwise).

#### Scenario: Add and list a flashcard

- GIVEN a user's note
- WHEN they add a `{question, answer}` card
- THEN it appears in that note's flashcard list

### Requirement: Spaced review

The system SHALL track a per-note review schedule (`reviewedAt`,
`nextReviewAt`, `reviewIntervalDays`). `POST /notes/{id}/review` with a
`rating` (`again`/`hard`/`good`/`easy`) SHALL advance the interval
(`again` resets to 1 day; otherwise it grows by a rating factor, capped at
365 days) and set `nextReviewAt = now + interval`. `GET /notes?due=true`
SHALL return only notes due now (`nextReviewAt <= now`).

#### Scenario: Review reschedules the note

- GIVEN a note never reviewed
- WHEN the user reviews it with rating `good`
- THEN `reviewIntervalDays` becomes 2 and `nextReviewAt` is set in the future

#### Scenario: Due filter excludes future reviews

- GIVEN a note just reviewed (next review in the future)
- WHEN the user lists notes with `due=true`
- THEN the note is excluded

### Requirement: LLM generation

The system SHALL generate flashcards and a summary for a note via the chat
LLM, scoped to the owning user. `POST /notes/{id}/flashcards/generate` SHALL
persist the model's flashcards (so they flow into the flashcard list and the
review queue) and return them; when the model yields no parseable cards
(e.g. the offline fallback with no API key), it SHALL return an empty list
rather than failing. `POST /notes/{id}/summary` SHALL persist an `aiSummary`
onto the note and return the updated note. A missing/other-user note SHALL
return `404`.

#### Scenario: Generate flashcards persists them

- GIVEN a user's note and a model that returns flashcards
- WHEN the user calls generate
- THEN the cards are persisted and appear in the note's flashcard list

#### Scenario: Offline generation yields no cards

- GIVEN no LLM is configured (offline fallback)
- WHEN the user calls generate
- THEN the system SHALL respond `201` with an empty list

#### Scenario: Summary is persisted on the note

- GIVEN a user's note
- WHEN the user requests a summary
- THEN `aiSummary` is set and visible on a later fetch of the note
