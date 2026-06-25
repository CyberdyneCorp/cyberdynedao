# authentication Specification

## Purpose

Resolve a bearer token into a `Principal` and gate routes by identity and
scope. Tokens are issued by the upstream CyberdyneAuth service; this
backend holds no passwords. Access tokens are **RS256 JWTs verified
locally against CyberdyneAuth's JWKS** (looked up by the token's `kid`),
not via RFC 7662 introspection — the introspection endpoint now requires
the caller to authenticate, and local verification needs no client
credentials and no per-request upstream round-trip. Baseline documents
behavior of `domain/auth_identity` + `adapters/inbound/middleware/auth.py`
+ `adapters/outbound/auth/*`.

## Requirements

### Requirement: Token-to-principal resolution

The system SHALL resolve a request's bearer token into a `Principal` by
verifying it as an RS256 JWT against CyberdyneAuth's JWKS, distinguishing
a `UserPrincipal` (human, carries `user_id` from `sub`) from a
`ServicePrincipal` (machine, carries `client_id`). The token SHALL be read
from the `Authorization: Bearer …` header, falling back to the
`access_token` cookie. (src: adapters/inbound/middleware/auth.py,
adapters/outbound/auth/jwks_verifier.py)

#### Scenario: Valid user token

- GIVEN a request with a valid CyberdyneAuth RS256 access token for a user
- WHEN the auth middleware processes the request
- THEN the token signature verifies against the JWKS key matching its `kid`
- AND the `iss` claim is one of the accepted issuers and the token is unexpired
- AND `request.state.principal` is set to a `UserPrincipal` with `user_id`, `scopes`, and `is_admin`

#### Scenario: Key rotation

- GIVEN an access token signed with a key whose `kid` is not in the cached JWKS
- WHEN the auth middleware processes the request
- THEN the system SHALL re-fetch the JWKS once (rate-limited) and retry the lookup
- AND the token verifies if the rotated key is now present

#### Scenario: Anonymous request

- GIVEN a request with no token
- WHEN the auth middleware processes the request
- THEN `request.state.principal` is left as `None`
- AND the request proceeds (anonymous endpoints still work)

#### Scenario: Invalid or expired token

- GIVEN a request whose token fails verification (bad signature, expired,
  untrusted issuer, malformed, or unknown `kid`)
- WHEN the auth middleware processes the request
- THEN `request.state.principal` is left as `None` and the request proceeds
- AND a public route still serves its response (the stale token is ignored)
- AND a `require_principal`/`require_editor` route responds `401`/`403`

#### Scenario: Auth service unavailable

- GIVEN the JWKS endpoint is unreachable (or returns non-200) AND no usable
  key is cached
- WHEN the auth middleware processes a request carrying a token
- THEN the system SHALL respond `503` with `{"detail": "auth service unavailable"}`

### Requirement: Principal-gated dependencies

The system SHALL provide `require_principal` (any authenticated principal)
and `require_editor` (editor authority) FastAPI dependencies. A user token
SHALL be required for user-scoped routes; service tokens SHALL be rejected
where a user is required. (src: adapters/inbound/middleware/auth.py)

#### Scenario: Missing principal on a protected route

- GIVEN an anonymous request to a `require_principal` route
- WHEN the dependency resolves
- THEN the system SHALL respond `401`

#### Scenario: Non-editor on an editor route

- GIVEN a `UserPrincipal` lacking the `editor` scope and not flagged admin
- WHEN a `require_editor` route is called
- THEN the system SHALL respond `403`

### Requirement: Editor authority via scope or admin flag

The system SHALL grant editor authority when the principal carries the
`editor` scope OR is flagged admin. The admin flag SHALL be read from the
verified token claims first (`is_superuser`/`is_admin`/`is_staff`, in
precedence order), then best-effort from the `/users/me` profile (cached
~60s). A profile fetch failure SHALL NOT raise — it degrades to "not
admin". (src: adapters/outbound/auth/profile_client.py)

#### Scenario: Admin flag from token claims

- GIVEN a user token whose verified claims include `is_admin=true`
- WHEN a `require_editor` route is called
- THEN editor authority is granted without fetching the profile

#### Scenario: Profile lookup degrades gracefully

- GIVEN a user token without an admin flag in introspection
- AND the `/users/me` profile endpoint is unavailable
- WHEN a `require_editor` route is called
- THEN the lookup does not raise
- AND editor authority is denied (`403`)
