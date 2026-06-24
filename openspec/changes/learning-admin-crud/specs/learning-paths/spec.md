## ADDED Requirements

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
