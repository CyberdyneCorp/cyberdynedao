# bookmarks Specification

## Purpose

Per-user favorites and a recently-viewed history backing the client's
Saved/Recent surfaces. (src: adapters/inbound/api/bookmarks/router.py,
domain/bookmarks)

## Requirements

### Requirement: Favorites

The system SHALL let an authenticated user list, add, and remove favorites
(`GET`/`POST /api/v1/me/favorites`, `DELETE …/{id}`). A favorite has a `type`
(`course`/`lesson`/`note`) and `ref`; adding SHALL be idempotent on
`(user, type, ref)`. An unknown `type` SHALL return `422`; deleting a favorite
not owned by the user SHALL return `404`. All access SHALL be user-scoped.

#### Scenario: Idempotent favorite

- GIVEN a user favorites `course:quantum-101`
- WHEN they favorite the same item again
- THEN the same favorite id is returned and only one row exists

#### Scenario: Delete a missing favorite

- GIVEN a user
- WHEN they DELETE a favorite id they do not own
- THEN the system SHALL respond `404`

### Requirement: Recently-viewed history

The system SHALL record and list recently-viewed items
(`POST`/`GET /api/v1/me/recent`), keyed per user on `(type, ref)` — re-viewing
SHALL bump `viewed_at` rather than duplicating. The list SHALL be
most-recent-first with `limit` clamped to 1..100 (default 20).

#### Scenario: Re-view bumps instead of duplicating

- GIVEN a user has viewed `lesson:l1`
- WHEN they view it again
- THEN one row remains with an updated `viewed_at`
