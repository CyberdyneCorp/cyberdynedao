# concepts Specification

## Purpose

A standalone, searchable library of concept cards (the Concepts nav), each
linking back to the lessons/courses that teach it. Public browse + editor
authoring. (src: adapters/inbound/api/concepts/router.py, domain/concepts)

## Requirements

### Requirement: Public browse and read

The system SHALL expose unauthenticated `GET /api/v1/concepts`
(`q` title/summary substring, `domain` exact filter, keyset `cursor`, `limit`
1..100 default 20, ordered by slug) and `GET /api/v1/concepts/{slug}` (404 if
absent).

#### Scenario: Search by query

- GIVEN concepts in different domains
- WHEN a client GETs `/api/v1/concepts?q=fourier`
- THEN only concepts matching "fourier" in title/summary are returned

#### Scenario: Cursor pagination

- GIVEN three concepts and `limit=2`
- WHEN the first page is fetched then the `nextCursor` followed
- THEN the pages together cover all three with a null final cursor

### Requirement: Editor authoring

The system SHALL let an `editor` create, update, and delete concepts
(`POST /api/v1/admin/concepts`, `PUT`/`DELETE …/{slug}`). The slug SHALL be
kebab-case and unique (duplicate → `409`, invalid → `422`); title/domain/
summary are required. Update SHALL preserve `id` and `created_at` and set
`updated_at`; a missing slug on update/delete SHALL return `404`.

#### Scenario: Duplicate slug rejected

- GIVEN a concept with slug `kvl` exists
- WHEN an editor creates another with slug `kvl`
- THEN the system SHALL respond `409`

#### Scenario: Update preserves identity

- GIVEN an existing concept
- WHEN an editor updates its title
- THEN the `id` and `created_at` are unchanged and `updated_at` is set
