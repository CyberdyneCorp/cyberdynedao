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
