# quota Specification

## Purpose

Server-side free-tier quota and Pro fair-use enforcement for the
token/compute-heavy features DAO serves (AI tutor chat, code execution,
Scan-to-Learn). The client display is advisory; DAO enforces caps regardless of
client. The `pro` entitlement is owned by CyberdyneAuth — DAO only reads it off
the introspected/JWT principal. (src: adapters/inbound/api/quota,
application/quota, domain/quota)

## Requirements

### Requirement: Read the Pro entitlement

The system SHALL read the caller's subscription entitlements from the auth
principal (the `entitlements` array on introspection / the access token) and
treat a `pro` or `pro:<plan>` token as Pro. It SHALL NOT grant entitlements
itself.

#### Scenario: Pro token recognized

- GIVEN an access token whose `entitlements` include `pro:annual`
- WHEN the principal is built
- THEN the principal is Pro

### Requirement: Free-tier quotas

The system SHALL enforce per-user free-tier caps for non-Pro users:
**10 AI-tutor messages/month**, **20 code runs/day**, **5 photo scans/month**.
On exceeding a cap it SHALL respond **402** (payment required) so the client can
show the paywall, including the limit, the reset time, and remaining count via
`X-Quota-*` response headers. Counters reset on a fixed monthly/daily window.
A blocked request SHALL NOT consume quota. Anonymous callers are not subject to
per-user quota (the per-IP limiter guards them).

#### Scenario: Free tutor cap reached

- GIVEN a non-Pro learner who has sent 10 tutor messages this month
- WHEN they send another
- THEN the system SHALL respond `402` with `X-Quota-Limit: 10` and `X-Quota-Remaining: 0`

### Requirement: Pro fair-use soft caps

For Pro users the system SHALL apply fair-use soft caps (~500 tutor
messages/month, ~200 scans/month) and respond **429** (with `Retry-After`) when
exceeded — a throttle, not a hard cut. Code execution has no Pro soft cap.

#### Scenario: Pro passes the free cap

- GIVEN a Pro learner
- WHEN they send more than 10 tutor messages in a month
- THEN the requests succeed until the fair-use soft cap, after which they get `429`

### Requirement: Pro-only certificate issuance

Course-completion certificate issuance SHALL be Pro-only; a non-Pro learner
SHALL be refused with **402**.

#### Scenario: Free learner cannot issue a certificate

- GIVEN a non-Pro learner
- WHEN they POST `/api/v1/courses/{slug}/certificate`
- THEN the system SHALL respond `402`
