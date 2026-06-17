# marketplace Specification

## Purpose

Sell training and license products via Stripe Checkout, fulfil on webhook
(grant enrollment / issue license key), and expose the buyer's orders and
licenses. (src: adapters/inbound/api/marketplace/router.py, domain/marketplace,
application/marketplace)

## Requirements

### Requirement: Product catalogue and checkout

The system SHALL list purchasable products (`GET /api/v1/marketplace/products`,
showing only `AVAILABLE`/`BETA` statuses) and create a Stripe Checkout
session for an authenticated buyer (`POST /api/v1/marketplace/checkout`). A
service-type product SHALL be rejected with `409` (routed to lead capture); a
non-purchasable product SHALL be rejected with `409`; a missing product SHALL
return `404`. Checkout SHALL create a `PENDING` order keyed by the Stripe
session id.

#### Scenario: Checkout a training product

- GIVEN an available training product
- WHEN an authenticated buyer POSTs `/api/v1/marketplace/checkout`
- THEN a `PENDING` order is created and a Stripe checkout URL is returned

#### Scenario: Service product is not checkout-able

- GIVEN a service-type product
- WHEN a buyer attempts checkout
- THEN the system SHALL respond `409`

### Requirement: Signed, idempotent webhook fulfilment

The system SHALL accept `POST /api/v1/stripe/webhook` only with a valid
`Stripe-Signature` (HMAC, 300s tolerance); an invalid signature SHALL return
`400`. Handling SHALL be idempotent on the Stripe event id (a duplicate
returns `200` and fulfils nothing twice). On `checkout.session.completed` the
order SHALL become `PAID` and fulfilment SHALL run (training → enrollment;
license → issue key + email). On `charge.refunded` the order SHALL become
`REFUNDED` and attached licenses revoked.

#### Scenario: Successful payment fulfils the order

- GIVEN a `PENDING` order for session `cs_123`
- WHEN a signed `checkout.session.completed` for `cs_123` arrives
- THEN the order becomes `PAID` and its product is fulfilled

#### Scenario: Duplicate webhook event

- GIVEN an event id already processed
- WHEN the same event is delivered again
- THEN the system SHALL respond `200` and fulfil nothing a second time

#### Scenario: Bad signature

- GIVEN a request with an invalid `Stripe-Signature`
- WHEN it reaches the webhook
- THEN the system SHALL respond `400`

#### Scenario: Oversized payload is capped

- GIVEN a request body larger than the webhook size cap (256 KiB)
- WHEN it reaches the webhook
- THEN the system SHALL respond `413` before the signature is verified

### Requirement: Stored webhook payloads are redacted

The system SHALL mask customer PII and card identifiers in the persisted
`stripe_webhook_events.payload` (kept for idempotency + audit). Fulfilment
reads the live verified event, never the stored row, so the row MUST NOT
accumulate regulated data. Structural fields (ids, type, amounts, status)
SHALL be preserved for debugging.

#### Scenario: Persisted payload masks PII

- GIVEN a `checkout.session.completed` event carrying a customer email + name
- WHEN it is recorded
- THEN the stored payload masks those values while keeping the session id and amount

### Requirement: Buyer orders and licenses

The system SHALL expose `GET /api/v1/me/orders` and `GET /api/v1/me/licenses`
for the authenticated buyer, and allow an `editor` to revoke a license
(`POST /api/v1/admin/marketplace/licenses/{id}/revoke`). A license plaintext
key SHALL be returned only at issuance (via email), never on subsequent
reads. Revoking an already-revoked license SHALL return `409`.

#### Scenario: List my licenses without plaintext

- GIVEN the buyer holds an issued license
- WHEN they GET `/api/v1/me/licenses`
- THEN the license is listed with no plaintext key
