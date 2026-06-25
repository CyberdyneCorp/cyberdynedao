## ADDED Requirements

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
