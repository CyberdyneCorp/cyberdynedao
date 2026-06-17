# leads Specification

## Purpose

Capture inbound contact "asks" (public, captcha-protected, rate-limited) and
triage them through an admin lifecycle. (src: adapters/inbound/api/leads/router.py,
domain/leads, application/leads)

## Requirements

### Requirement: Public ask submission

The system SHALL accept `POST /api/v1/asks` from anonymous callers with a
captcha token. The captcha SHALL be verified before persistence; a rejected
captcha SHALL return `400` and persist nothing. Submissions SHALL be
rate-limited to 5 per 60 seconds per client IP; exceeding the limit SHALL
return `429`. A created ask SHALL start in status `NEW` and trigger a
notification.

#### Scenario: Valid submission

- GIVEN a valid captcha token
- WHEN a client POSTs `/api/v1/asks`
- THEN the ask is persisted with status `NEW` and a notification is sent

#### Scenario: Captcha rejected

- GIVEN a captcha token that fails verification
- WHEN a client POSTs `/api/v1/asks`
- THEN the system SHALL respond `400` and persist nothing

#### Scenario: Rate limit exceeded

- GIVEN 5 asks already submitted from an IP within 60 seconds
- WHEN a 6th ask is submitted from that IP
- THEN the system SHALL respond `429`

### Requirement: Admin triage lifecycle

The system SHALL allow an `editor` to list asks (`GET /api/v1/admin/asks`,
filterable by status/channel/free-text, paginated) and update one
(`PATCH /api/v1/admin/asks/{id}`) — applying a status transition, appended
note, and/or owner reassignment atomically, emitting an event per action. An
invalid status transition SHALL return `409`; an empty note SHALL return `409`.

#### Scenario: Valid transition

- GIVEN an ask in status `NEW`
- WHEN an editor transitions it to `TRIAGED`
- THEN the status changes and a `STATUS_CHANGED` event is emitted

#### Scenario: Forbidden transition

- GIVEN an ask in a state that disallows the target
- WHEN an editor requests that transition
- THEN the system SHALL respond `409`
