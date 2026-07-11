# learning-paths Specification

## Purpose

The legacy learning catalogue: seeded modules + paths, idempotent enrollment,
module progress, prerequisite/level/sequential gating + eligibility,
enrollment deadlines, and signed path certificates. (src:
adapters/inbound/api/learning/router.py, domain/learning, application/learning)
## Requirements
### Requirement: Catalogue and idempotent enrollment

The system SHALL expose public `GET /api/v1/learning/modules` and `/paths`
(sorted by `(sort_order, slug)`), and let a user enroll in a path
(`POST /api/v1/learning/paths/{slug}/enroll`). Enrollment SHALL be idempotent
on `(user_id, path_slug)` — re-enrolling returns the existing enrollment. An
unknown path SHALL return `404`.

#### Scenario: Re-enroll returns the same enrollment

- GIVEN a user already enrolled in `p1`
- WHEN they enroll in `p1` again
- THEN the same enrollment id is returned

### Requirement: Module progress invariant

The system SHALL record module progress (`PATCH
/api/v1/learning/modules/{slug}/progress`, percent 0..100, else `422`) for the
user, keeping `completed_at` non-null iff `percent == 100`. Dropping below 100
SHALL clear `completed_at`.

#### Scenario: Reaching 100 marks complete

- GIVEN a module at 50%
- WHEN the user sets it to 100%
- THEN `completed_at` is set

#### Scenario: Reopening clears completion

- GIVEN a completed module
- WHEN the user sets it to 60%
- THEN `completed_at` is cleared

### Requirement: Prerequisite gating and eligibility

The system SHALL compute, for a path, each module's lock state
(`GET /api/v1/learning/paths/{slug}/gating`) combining level gating (a level
unlocks only after all lower-level modules are complete) and sequential gating
(within a level, in declared order); each gate SHALL report `unlocked`,
`completed`, `blocked_by`, and `reason` (`level`/`sequential`). Eligibility
(`…/eligibility`) SHALL report `next_module` or a `reason`. An unknown path
SHALL return `404`.

#### Scenario: Sequential lock within a level

- GIVEN a path `[b1, b2, i1]` with no progress
- WHEN gating is requested
- THEN `b1` is unlocked, `b2` is blocked_by `b1` (sequential), `i1` is blocked (level)

### Requirement: Enrollment deadlines

The system SHALL report a user's enrollment deadlines
(`GET /api/v1/learning/deadlines`) with a status derived from `due_at` vs now:
`none` (no deadline), `overdue` (`due_at <= now`), `urgent` (within 3 days),
`upcoming` (beyond 3 days), plus `days_remaining`. An editor SHALL set/clear a
deadline; a missing enrollment SHALL return `404`.

#### Scenario: Urgent within three days

- GIVEN a deadline two days out
- WHEN deadlines are read
- THEN the status is `urgent` with `days_remaining = 2`

### Requirement: Path certificates

The system SHALL let an editor issue a path certificate
(`POST /api/v1/admin/learning/paths/{slug}/certificate/issue/{user_id}`) only
when every module in the path is at 100% (else `409`); a missing path SHALL
return `404`. Certificates SHALL be publicly verifiable by id (returning
`{valid, certificate}`; unknown id → `valid:false`) and downloadable as PDF
(`404` if missing).

#### Scenario: Issue requires full completion

- GIVEN a user who has not completed every module
- WHEN an editor issues the certificate
- THEN the system SHALL respond `409`

### Requirement: Published verification key

The system SHALL expose the certificate verification key at public
`GET /api/v1/learning/certificates/signing-key`, returning the signing
`algorithm`. When the Ed25519 scheme is active it SHALL include the
base64url `publicKey` so external verifiers can check signatures without
the backend's secret; under HMAC the `publicKey` SHALL be null (a shared
secret is not publishable).

#### Scenario: Ed25519 public key is published

- GIVEN the backend signs certificates with Ed25519
- WHEN a client GETs the signing-key endpoint
- THEN it receives `algorithm: ed25519` and the base64url public key, which verifies a real signature

#### Scenario: HMAC publishes no key

- GIVEN the backend signs with HMAC
- WHEN a client GETs the signing-key endpoint
- THEN `publicKey` is null

### Requirement: Admin CRUD for learning modules

An editor SHALL manage learning modules through the admin API, so modules can be authored without source changes. The system SHALL expose, guarded by the editor role:

- `GET /api/v1/admin/learning/modules` — list all modules (sorted by `(sort_order, slug)`).
- `POST /api/v1/admin/learning/modules` — create a module `{ slug?, title, category, description, level, duration, icon, topics[] }`. When `slug` is omitted it SHALL be derived from `title`. Creating a module whose slug already exists SHALL return `409`.
- `PATCH /api/v1/admin/learning/modules/{slug}` — partially update a module's fields; an unknown slug SHALL return `404`.
- `DELETE /api/v1/admin/learning/modules/{slug}` — delete a module; an unknown slug SHALL return `404`.

`level` SHALL be one of `Beginner`, `Intermediate`, `Advanced` (else `422`). Created/updated modules SHALL appear in the public `GET /api/v1/learning/modules` with no redeploy. A non-editor SHALL receive `401`/`403`.

#### Scenario: Create a module appears in the public catalogue

- **GIVEN** an editor
- **WHEN** they `POST /api/v1/admin/learning/modules` with a valid module body
- **THEN** the response is `201` with the created module
- **AND** the module is returned by public `GET /api/v1/learning/modules`

#### Scenario: Duplicate module slug is rejected

- **GIVEN** a module `m1` already exists
- **WHEN** an editor creates another module with slug `m1`
- **THEN** the system SHALL respond `409`

#### Scenario: Invalid level is rejected

- **WHEN** an editor creates a module with `level` not in `{Beginner, Intermediate, Advanced}`
- **THEN** the system SHALL respond `422`

#### Scenario: Unknown module update returns 404

- **WHEN** an editor `PATCH`es a module slug that does not exist
- **THEN** the system SHALL respond `404`

### Requirement: Admin CRUD for learning paths

An editor SHALL manage learning paths through the admin API. The system SHALL expose, guarded by the editor role:

- `GET /api/v1/admin/learning/paths` — list all paths (sorted by `(sort_order, slug)`).
- `POST /api/v1/admin/learning/paths` — create a path `{ slug?, title, description, moduleSlugs[], estimatedTime, icon }`. When `slug` is omitted it SHALL be derived from `title`. A duplicate slug SHALL return `409`.
- `PATCH /api/v1/admin/learning/paths/{slug}` — partially update a path, including replacing/reordering `moduleSlugs`; an unknown slug SHALL return `404`.
- `DELETE /api/v1/admin/learning/paths/{slug}` — delete a path; an unknown slug SHALL return `404`.
- `POST /api/v1/admin/learning/paths/{slug}/modules/reorder` — set the ordered `moduleSlugs` for a path.

Every entry in a path's `moduleSlugs` SHALL reference an existing module; a path create/update/reorder referencing an unknown module slug SHALL be rejected with `422` and SHALL NOT persist. Created/updated paths SHALL appear in the public `GET /api/v1/learning/paths`, remain enrollable, and keep existing gating/eligibility working off the stored module order, with no redeploy.

#### Scenario: Create a path with valid modules

- **GIVEN** modules `m1` and `m2` exist
- **WHEN** an editor `POST`s a path with `moduleSlugs: [m1, m2]`
- **THEN** the response is `201`
- **AND** the path is returned by public `GET /api/v1/learning/paths` and is enrollable

#### Scenario: Path referencing an unknown module is rejected

- **GIVEN** module `m1` exists but `ghost` does not
- **WHEN** an editor creates a path with `moduleSlugs: [m1, ghost]`
- **THEN** the system SHALL respond `422`
- **AND** no path is persisted

#### Scenario: Reorder updates the stored module order

- **GIVEN** a path with `moduleSlugs: [m1, m2, m3]`
- **WHEN** an editor reorders it to `[m3, m1, m2]`
- **THEN** public `GET /api/v1/learning/paths` returns the new order
- **AND** gating is computed from the new order

#### Scenario: Delete removes the path

- **GIVEN** a path `p1`
- **WHEN** an editor deletes `p1`
- **THEN** `p1` no longer appears in public `GET /api/v1/learning/paths`

### Requirement: Seeded catalogue preserved under admin CRUD

Introducing admin CRUD SHALL NOT alter the existing seeded catalogue. The 5 paths and 12 modules seeded by the initial migration SHALL remain present and unchanged in the public read endpoints until an editor explicitly edits them.

#### Scenario: Seeded catalogue intact

- **GIVEN** a freshly migrated database
- **WHEN** the public `GET /api/v1/learning/paths` and `/modules` are read
- **THEN** the original 5 paths and 12 modules are returned unchanged

### Requirement: Course-backed modules (stages)

A learning module SHALL optionally bundle one or more courses via `courseSlugs`. A module with `courseSlugs` represents a **stage** in a path whose substance is those courses; its title/level/duration/icon/topics remain the stage's display metadata. The public module and path read endpoints SHALL include each module's `courseSlugs` plus a lightweight expansion (`slug`, `title`, `level`) of the linked courses for rendering. A module MAY have zero linked courses (a legacy descriptive milestone).

#### Scenario: Module exposes its linked courses

- **GIVEN** a module `foundations` with `courseSlugs: ["python-course", "computational-thinking-basics"]`
- **WHEN** the public catalogue is read
- **THEN** the module reports those `courseSlugs` and an expansion carrying each course's slug/title/level

### Requirement: Derived module completion from linked courses

For a module with one or more `courseSlugs`, the system SHALL derive the user's module completion from course progress: the module is complete (100%) **iff every linked course is complete** for that user, and its percent is derived from the linked courses' completion. A module with no `courseSlugs` SHALL retain the legacy self-reported percent (`PATCH /learning/modules/{slug}/progress`). Path gating, eligibility, and certificate eligibility SHALL use this derived completion.

#### Scenario: Stage completes when all its courses are done

- **GIVEN** a module linking courses `c1` and `c2`, with `c1` complete and `c2` at 40%
- **WHEN** the user's path state is computed
- **THEN** the module is not complete
- **AND** when `c2` reaches 100% the module becomes complete

#### Scenario: Course-less module still self-reports

- **GIVEN** a seeded module with no linked courses
- **WHEN** the user PATCHes its progress to 100
- **THEN** it is complete, exactly as before this change

### Requirement: Admin assigns courses to a module

An editor SHALL set a module's linked courses by supplying `courseSlugs` on create/update of a module. Every slug SHALL reference an existing course; an unknown course slug SHALL be rejected with `422` and SHALL NOT persist.

#### Scenario: Assigning a real course to a stage

- **GIVEN** course `python-course` exists
- **WHEN** an editor sets module `foundations` `courseSlugs` to `["python-course"]`
- **THEN** the module stores that linkage and the public catalogue reflects it

#### Scenario: Unknown course rejected

- **WHEN** an editor sets a module's `courseSlugs` to include a slug with no matching course
- **THEN** the system SHALL respond `422` and the module is unchanged

### Requirement: Learner can browse and progress a path of courses

The learner UI SHALL provide a Learning Paths view: list paths, enroll, and for an enrolled path show each stage (module) with its linked courses, the per-stage lock/unlock state (existing gating), the next course to take, and the path certificate once every stage is complete. Opening a course from a stage SHALL navigate to the existing course player; stage completion updates as the user completes those courses.

#### Scenario: Path view reflects course progress

- **GIVEN** a user enrolled in a path whose first stage links one course
- **WHEN** the user completes that course
- **THEN** the path view shows the first stage complete and unlocks the next stage per gating

### Requirement: Locale-aware learning catalogue reads

The public `GET /api/v1/learning/modules` and `GET /api/v1/learning/paths` SHALL resolve the request locale (explicit `?lang=` → `Accept-Language` → `en`, unknown tags falling back to `en`) and return each module's / path's translated `title` and `description` when a translation for that language exists, with **per-field English fallback** (a missing translated field uses the English base value). The English base rows are unchanged; ordering and all other fields are unaffected by locale.

#### Scenario: Spanish reader gets the Spanish title, English fallback per field

- **GIVEN** a path with an English title and a Spanish translation of its title only (no Spanish description)
- **WHEN** it is read with `?lang=es`
- **THEN** the response title is the Spanish one and the description falls back to English

#### Scenario: Unknown locale falls back to English

- **WHEN** the catalogue is read with `?lang=xx`
- **THEN** all titles/descriptions are the English base values

#### Scenario: Seeded catalogue unaffected

- **GIVEN** the seeded modules/paths (no translations)
- **WHEN** read with any locale
- **THEN** their English titles/descriptions are returned unchanged

### Requirement: Admin manages module and path translations

An editor SHALL manage per-language translations of a module's and a path's `title` and `description` through the admin API:

- `GET /api/v1/admin/learning/modules/{slug}/translations` — list translations (by language).
- `PUT /api/v1/admin/learning/modules/{slug}/translations/{language}` — upsert `{ title, description }` for `language`.
- `DELETE /api/v1/admin/learning/modules/{slug}/translations/{language}` — remove it.
- The same four under `…/paths/{slug}/translations`.

`language` MUST be a supported non-English tag (`pt-BR`, `es`, `fr`); `en` or an unsupported tag SHALL return `422`. An unknown module/path slug SHALL return `404`. All routes require the editor role.

#### Scenario: Set then read a translation

- **GIVEN** module `m1` exists
- **WHEN** an editor `PUT`s `{title, description}` for `es`
- **THEN** it is stored, listed by `GET …/translations`, and surfaced by the public read with `?lang=es`

#### Scenario: English or unsupported language rejected

- **WHEN** an editor `PUT`s a translation for `en` or `de`
- **THEN** the system SHALL respond `422`

#### Scenario: Deleting a module removes its translations

- **GIVEN** module `m1` with an `es` translation
- **WHEN** the module is deleted
- **THEN** its translations are removed too (cascade)

