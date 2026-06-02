# Backend Roadmap

> **Status:** Draft v1 · 2026-05-25
> **Owner:** Leo
> **Repo:** new `cyberdynedao/backend/` sibling to `frontend/`
> **Audience:** Leo coming back cold in 3 weeks, plus contributors who already know the Cyberdyne stack (CyberdyneAuth, CyberRAG, OrgPilot)

> **Shipped beyond this v1 plan (2026-06-01).** Phases 1–6 below are live.
> The learning platform has since grown well past the original Phase-4
> sketch — all of the following are merged, tested, and deployed:
> **courses & lessons** (admin CRUD, levels, publish, reorder, typed
> lessons), **per-lesson progress + per-course auto-completion**
> (`PUT /api/v1/courses/{slug}/lessons/{id}/progress`,
> `GET /api/v1/courses/{slug}/progress` - course-scoped, complete iff
> every lesson is; passing a lesson's quiz auto-completes that lesson),
> **quizzes** (player + attempts + static feedback),
> **file uploads** (MIME routing, size caps, traversal guards, persistent
> volume), **prerequisite/level/sequential gating + enrollment
> eligibility**, **enrollment deadlines + course-level deadlines**
> (`PUT /api/v1/admin/courses/{slug}/deadline`; overdue/urgent/upcoming
> status derived at read time), **learner + admin analytics**
> (the learner dashboard now also reports completed + in-progress
> courses, derived from lesson progress), **certificate verify-by-id +
> PDF**, and a **learning-aware chat agent**
> (see [`agents_capabilities.md`](agents_capabilities.md)), and the
> **code-interpreter lesson type** (`code` lessons run on the MATLAB-LLVM
> engine via `POST /api/v1/lessons/{id}/code/run`), **AI contextual quiz
> feedback** (`POST /api/v1/lessons/{id}/quiz/feedback` - LLM-personalized
> "why it's wrong" per incorrect answer), and **LLM course
> recommendations** (`GET /api/v1/recommendations/me` - deterministic
> catalogue ranking against the learner's dashboard + an LLM narrative).
> All planned Academy AI phases are now delivered. Per-context detail
> lives in each bounded
> context under `backend/src/cyberdyne_backend/`.

This doc is the plan, not a spec. Anything declared here is the default; anything in **Open Questions** is unblocked work that needs a decision before Phase 2 starts.

---

## 1. Goals & Non-Goals

### Goals

1. Replace every static `src/lib/data/*.ts` file with a versioned, cache-friendly REST endpoint on a Python FastAPI service, hexagonal at its core, behind CyberdyneAuth.
2. Ship a learning platform (modules, paths, enrollment, progress, certificates) and a marketplace (Stripe-powered training + license keys + service inquiries) wired into the existing frontend views.
3. Stand up a single OpenAI-backed chat agent (tool calls + retrieval) grounded in Cyberdyne content (projects, blog, learning modules, services) so the terminal UI can answer "what does CyberSTAC do?" without hitting the static file.
4. Expose on-chain reality (NFT-tier access; full DAO treasury composition on Base: ERC-20 balances + **AAVE v3 positions** + **Uniswap v4 LP positions** for the DAO smart contract address) as cached read-models — not "another wallet flow". The wallet flow lives in CyberdyneAuth. Governance proposals and on-chain dividend mechanics are out of v1 — see Open Q 11.
5. Hit **≥90% unit-test coverage** on `domain/` and `application/` layers as a hard CI gate from day one (excluding integration-only adapters — same calibration the rest of the Cyberdyne stack uses). The gate is enforced by `pytest-cov` with `fail_under=90`; the only allowed escape hatch is a PR that lowers the threshold, never a per-line `# pragma: no cover`.
6. Standard Cyberdyne developer workflow: **`uv`** for dependency management (`uv.lock` committed, `uv sync --frozen` in Docker) and **`just`** as the task runner (`just install / dev / test / lint / typecheck / lint-imports / check`). Matches CyberdyneAuth / geo_dashboard / OrgPilot bone-for-bone so muscle memory transfers across services.
7. Be Coolify-deployable on first push using the same recipe as CyberdyneAuth / OrgPilot (multi-stage `uv` Dockerfile with `UV_LINK_MODE=copy`, `alembic upgrade head` on entrypoint, Traefik via `expose:`).

### Non-Goals

- **We are not re-implementing CyberdyneAuth.** Login, sessions, CSRF, wallet sign-in, OAuth — all of that is consumed from `auth.backend.coolify.cyberdynecorp.ai`. We verify its JWTs and read claims; we never mint them.
- **We are not building a CMS.** Blog content is authored in Markdown in this repo (or pushed via an admin endpoint), not in a WYSIWYG editor. No drafts UI in v1.
- **We are not re-implementing CyberRAG.** The chat agent's knowledge backend is CyberRAG via MCP (or HTTP fallback) — see §5.6 for why we are not rolling pgvector inline.
- **We are not running a smart-contract indexer.** Web3 reads are on-demand + short-TTL cached, not a Subgraph clone. If we ever need historical indexing, that's a separate service.
- **No write-side Web3 in v1.** Dividend distribution oracles, treasury rebalance triggers — design the seam, but don't ship the keystore yet.
- **No DAO governance contract chosen in v1.** Proposal aggregation, voting, and on-chain dividend windows wait until a Governor implementation lands (Open Q 11). The frontend's Proposals panel keeps rendering mock data; the `GovernorAdapter` port is defined so the swap is small once a contract is picked.
- **No Stripe Connect / multi-tenant payouts.** Single-tenant Stripe account, single payout destination. Marketplace sellers other than Cyberdyne itself is a v2 problem.

---

## 2. Stack Decision Table

| Concern | Choice | One-line rationale |
|---|---|---|
| Language | Python 3.12 | Matches CyberdyneAuth, CyberRAG, CyberDocExtractor — same toolchain, same lessons |
| Web framework | FastAPI 0.115+ | Same as every other Cyberdyne service; first-class async, OpenAPI, pydantic v2 |
| Package manager | `uv` | Proven Coolify recipe; `uv.lock` + `--frozen` build is reproducible |
| Task runner | `just` | Already conventional across the stack |
| ORM | SQLAlchemy 2.0 async + asyncpg | Same as CyberdyneAuth/OrgPilot; per-request Unit of Work |
| Migrations | Alembic | Run on container entrypoint; `alembic upgrade head && uvicorn …` |
| Primary store | PostgreSQL 17 | Single backup, single connection pool — Cyberdyne house rule |
| Vector / KG store | **None inline — delegate to CyberRAG** | See §5.6; one fewer pg extension to manage; same graph powers OrgPilot |
| Auth | CyberdyneAuth (RFC 7662 introspection + OAuth 2.0 client-credentials) | Verify via `/api/v1/auth/introspect`; never mint locally. This backend is itself an OAuth client for outbound service-to-service calls. |
| Payments | Stripe (single-account) | Test mode → live mode; webhook handler with idempotency keys |
| Web3 RPC | `web3.py` 6.x | Read-only path against Base mainnet; signer wiring deferred to Phase 5 |
| LLM | OpenAI (gpt-4o-mini default, gpt-4o for tool-heavy) | Tool-calling is mature; swap-by-port if needed |
| MCP client | FastMCP 3 client (streamable-http) | Talk to CyberRAG/MCP using the same transport CyberRAG already exposes |
| Arch enforcement | `import-linter` | Same contracts file shape as CyberdyneAuth — enforced on every PR |
| Coverage | `pytest-cov` with `fail_under = 90` on `domain` + `application` packages | Hard gate; integration adapters excluded |
| Observability | `structlog` + Sentry + Prometheus `/metrics` | Same trio as OrgPilot |
| Background work | FastAPI `BackgroundTasks` (v1) → arq + Redis (v2 if needed) | YAGNI Redis until Stripe webhook retries or chat-agent backfill demand it |
| Deploy | Coolify (Dockerfile, single app + sidecar Postgres) | Same as every other Cyberdyne service |

---

## 3. Architecture Overview

Hexagonal layout matches CyberdyneAuth bone-for-bone. Top-level layout:

```
backend/
├── pyproject.toml
├── uv.lock
├── justfile
├── alembic.ini
├── alembic/
├── Dockerfile.coolify
├── compose.coolify.yaml
├── importlinter.cfg
├── src/cyberdyne_backend/
│   ├── domain/            # entities, value objects, ports — pure Python, no I/O
│   ├── application/       # use cases, orchestration, UoW boundaries
│   ├── adapters/
│   │   ├── inbound/       # FastAPI routers, MCP server (later), schedulers
│   │   └── outbound/      # repos (SQLAlchemy), Stripe, Web3, OpenAI, CyberRAG, CyberdyneAuth
│   ├── infrastructure/    # session/engine factory, settings, logging, sentry, container
│   └── main.py            # ASGI app factory
└── tests/
    ├── unit/              # >=90% coverage of domain + application
    ├── integration/       # real Postgres (testcontainers), mocked external APIs
    └── e2e/               # against running stack; opt-in CI job, not gating
```

**Module slicing inside `domain/` and `application/`** mirrors the bounded contexts (one folder per context — no shared "models.py"):

```
domain/{auth_identity, content, learning, marketplace, leads, ai_chat, web3_read, dao_readmodel}/
application/{same names}/
adapters/outbound/{persistence, stripe, web3rpc, openai, cyberrag, cyberdyne_auth, email}/
```

`import-linter` contracts (one per layer + one per bounded context — same shape as CyberdyneAuth's):
- `domain` cannot import from `application`, `adapters`, `infrastructure`.
- `application` cannot import from `adapters` or `infrastructure`.
- `adapters/inbound` cannot import from `adapters/outbound`.
- Each bounded context can only import its own `domain` and `application` modules + the shared `domain/common` kernel.

### Core request flow

```mermaid
flowchart TB
    Client["SvelteKit frontend<br/>or AI agent"]
    Traefik["Traefik / Coolify"]

    subgraph App["cyberdyne-backend (FastAPI)"]
        Routers["Inbound adapters<br/>FastAPI routers"]
        AuthMW["AuthN middleware<br/>verifies CyberdyneAuth JWT"]
        UC["Application use cases"]
        Domain["Domain entities + ports"]
        UoW["Per-request UoW<br/>(async SQLAlchemy)"]
        OutPersist["SQLAlchemy repos"]
        OutStripe["Stripe adapter"]
        OutWeb3["Web3.py adapter"]
        OutOpenAI["OpenAI adapter"]
        OutRAG["CyberRAG client (MCP)"]
    end

    subgraph Ext["External"]
        Auth["CyberdyneAuth<br/>(introspect + /oauth2/token<br/>+ /users/me + /clients/me)"]
        PG[("PostgreSQL 17")]
        Stripe["Stripe API + webhooks"]
        Base["Base mainnet RPC<br/>(AccessNFT, Treasury, Marketplace)"]
        OpenAI["OpenAI API"]
        CyberRAG["CyberRAG REST + MCP"]
    end

    Client --> Traefik --> Routers --> AuthMW --> UC --> Domain
    AuthMW -. RFC 7662 introspect (cached) .-> Auth
    UC --> UoW --> OutPersist --> PG
    UC --> OutStripe --> Stripe
    UC --> OutWeb3 --> Base
    UC --> OutOpenAI --> OpenAI
    UC --> OutRAG --> CyberRAG
    Stripe -. webhook .-> Routers
```

**Where ports live:** each bounded context owns its ports in `domain/<context>/ports.py` (Protocols / abstract base classes). Outbound adapters in `adapters/outbound/` implement them. The DI container in `infrastructure/container.py` (a thin factory, not a magic framework — same as CyberdyneAuth) wires them per request.

---

## 4. Domain Model — The Spine

Only the entities that matter; no per-column ERDs.

**Identity (mirrored from CyberdyneAuth, read-only here)**

CyberdyneAuth issues two distinct token types as of [issue #2](https://github.com/CyberdyneCorp/CyberdyneAuth/issues/2): user tokens (from password/OAuth/wallet login) and service tokens (from `POST /api/v1/auth/oauth2/token` client-credentials). Both are introspected the same way (`POST /api/v1/auth/introspect`), so we model them as a discriminated union:

```python
@dataclass(frozen=True, slots=True)
class UserPrincipal:
    user_id: UUID
    username: str | None        # from introspect.username
    scopes: frozenset[str]      # from introspect.scope (space-separated)
    audience: str | None        # from introspect.aud
    expires_at: datetime         # from introspect.exp

@dataclass(frozen=True, slots=True)
class ServicePrincipal:
    client_id: str
    scopes: frozenset[str]
    audience: str | None
    expires_at: datetime

Principal = UserPrincipal | ServicePrincipal
```

Built from `IntrospectionResponse` (`active`, `sub`, `scope`, `aud`, `exp`, `iat`, `client_id`, `token_type`, `username`). Discriminator: presence of `client_id` (service) vs `username` (user). Both are value objects, never persisted — rebuilt per request from cached introspection.

**Full user profile** (email, `organization_id`, `is_active`, etc.) is *not* on `UserPrincipal`. Routes that need it use a `UserProfile` dependency that lazily fetches `GET /api/v1/users/me` (cached 60s by `user_id`). Same pattern for `ServiceProfile` via `GET /api/v1/clients/me`. Two caches, opt-in per route — see §5.1.

NFT tier, linked wallet, and on-chain data are *not* on any of these — they come from the Web3 reader (§5.7) and dedicated use cases.

**Content**
- `BlogPost` (slug, title, body_md, excerpt, category_id, author_id, published_at, tags[]) — primary aggregate.
- `BlogCategory` (slug, name, palette).
- `Project` (slug, name, palette, status, description, features[], extra_features[]) — backs `products.ts`.
- `Domain` / `Belief` / `RoadmapPhase` / `TokenomicsRow` — small reference tables backing `cyberdyne.ts`.
- `TeamMember` (id, name, title, bio, image_url, tags[], palette).
- `ServiceSection` (id, title, intro, bullets[]).

**Learning**
- `LearningModule` (slug, title, category, body_md, level, duration_minutes, topics[], icon).
- `LearningPath` (slug, title, description, module_slugs[], estimated_weeks).
- `Enrollment` (user_id, path_id, started_at, status).
- `ModuleProgress` (user_id, module_id, percent, completed_at). Invariant: `completed_at` non-null iff `percent == 100`.
- `Certificate` (user_id, path_id, issued_at, nft_token_id?, verification_hash). Invariant: only issued when all modules in path are `completed`.

**Marketplace**
- `Product` (slug, type ∈ {service, training, license}, title, description_md, price_cents, currency, duration_label, features[], stripe_price_id?, status). Invariant: `training` and `license` require `stripe_price_id`; `service` does not (it routes to lead capture).
- `Order` (id, user_id, product_id, amount_cents, stripe_payment_intent_id, stripe_checkout_session_id, status ∈ {pending, paid, refunded, failed}, created_at, paid_at?). Invariant: `paid_at` set iff `status == paid`.
- `LicenseKey` (id, order_id, product_id, key_value (encrypted at rest), expires_at, revoked_at?). Generated on Stripe `checkout.session.completed` for license products.
- `WebhookEvent` (stripe_event_id PK, type, payload_json, processed_at). Idempotency table — `INSERT … ON CONFLICT DO NOTHING` is the contract.

**Leads / Asks**
- `Ask` (id, channel ∈ {contact_form, marketplace_service_inquiry, chat_agent_handoff}, name, email, body, product_slug?, source_url, status ∈ {new, triaged, in_progress, closed}, owner_user_id?, created_at, notes_md).
- `AskEvent` (ask_id, kind ∈ {status_changed, note_added, owner_assigned}, by_user_id, payload, at).

**AI Chat**
- `ChatSession` (id, user_id?, created_at, last_message_at). Anonymous sessions allowed.
- `ChatMessage` (id, session_id, role ∈ {user, assistant, tool}, content_md, tool_name?, tool_args_json?, tool_result_json?, tokens_in, tokens_out, model, created_at).

**Web3 Read-Models**
- `TreasurySnapshot` (chain, taken_at, total_usd, erc20_balances_json, aave_summary_json, uniswap_v4_position_count). Cached every N minutes via scheduler — adapter, not domain.
- `AavePositionSnapshot` (chain, owner_address, reserve_address, supplied_underlying, borrowed_variable, borrowed_stable, fetched_at) — one row per (owner, reserve). The account-level summary (health factor, LTV, liquidation threshold, total collateral / debt / available borrows) lives in `TreasurySnapshot.aave_summary_json` so we don't recompute it per request.
- `UniswapV4PositionSnapshot` (chain, owner_address, position_id, pool_id, currency0, currency1, fee, tick_spacing, hooks_address, tick_lower, tick_upper, liquidity, fees_owed_token0, fees_owed_token1, fetched_at) — one row per LP position the DAO holds.
- `NftTierCache` (wallet_address, tier, fetched_at, expires_at). Same shape CyberdyneAuth uses; we cache because Base RPC isn't free.
- *Deferred:* `ProposalSnapshot` — not in v1; reintroduced when the Governor contract is chosen (Open Q 11).

Keys: every public ID is a slug (kebab-case) or a UUID v7. Stripe ids and on-chain addresses are stored as strings, never as enums.

---

## 5. Module-by-Module Breakdown

For each module: **purpose**, three representative endpoints, **key dependencies**, **testing approach**. Authoritative endpoint list lives in OpenAPI; this is just the spine.

### 5.1 Auth Integration (consume only)

**Purpose:** Verify CyberdyneAuth tokens (cookie or Bearer), expose `request.state.principal` (user or service) to every router, look up full profile data on demand, and act as a service client when this backend calls other CyberdyneAuth-trusted services (CyberRAG, NFT-tier lookup, etc.).

**Status:** CyberdyneAuth has shipped the full OAuth 2.0 client-credentials surface as of [CyberdyneAuth#2](https://github.com/CyberdyneCorp/CyberdyneAuth/issues/2). Open Q 9 is resolved. The verification model below uses **RFC 7662 token introspection** as the primary verifier — supersedes the older `/users/me`-only approach used by `geo_dashboard` and `orgpilot`, both of which were built before introspection existed.

**Verification model: RFC 7662 introspection.** CyberdyneAuth still does not expose a JWKS endpoint (tokens remain opaque), but `POST /api/v1/auth/introspect` now lets us validate any token (user OR service) in one call and learn its scope, audience, expiry, and whether the subject is a user (`token_type=Bearer`, `username` present) or a service (`token_type=Bearer`, `client_id` present).

The auth middleware:

1. Extracts the token from either the `access_token` cookie (browser) or the `Authorization: Bearer …` header (service).
2. Looks up `(sha256(token) → Principal)` in an in-process cache (TTL **30s**, matching geo_dashboard's reasoning — long enough to absorb polling loops, short enough to keep revocation latency bounded). **Keys are SHA-256 of the token**, never the raw token.
3. On cache miss, calls `POST ${CYBERDYNE_AUTH_BASE_URL}/api/v1/auth/introspect` with `token=<the token>`. The response's `active: bool` decides validity; `client_id` vs `username` decides whether the principal is a service or a user.
4. **Failures are not cached.** Errors and `active: false` results retry upstream next call. No stale-cache fallback.
5. **Request coalescing.** Multiple concurrent verifications of the same token are merged via an `asyncio.Future` leader pattern (5 simultaneous polls → 1 upstream call). Critical for dashboard polling.
6. Upstream client wrapped in resilience: retry-with-backoff (3 retries, 0.5–8s) on transport errors, circuit breaker (5 failures → open for 60s).
7. Stores the resolved `Principal` on `request.state.principal`. Anonymous endpoints still work — middleware doesn't reject missing tokens, it just leaves `principal = None`.

**Lazy full-profile loading.** Introspection returns enough for routing + authorization (scopes, audience, subject type, expiry). It does **not** return the full user profile (email, organization_id) or the full client profile (name, allowed_audiences). Routes that need those fields use a FastAPI dependency that lazily fetches:
- `GET /api/v1/users/me` for user tokens (caches `UserProfile` by `user_id` for 60s).
- `GET /api/v1/clients/me` for service tokens (caches `ServiceProfile` by `client_id` for 60s).

Two endpoints, two caches, but only paid when the route actually needs the data. The introspect call is universal; profile lookups are opt-in.

**Backend-as-service-client.** This backend itself is a CyberdyneAuth OAuth client. On startup:
1. Calls `POST /api/v1/auth/oauth2/token` with `grant_type=client_credentials` + `client_secret_basic` auth using `CYBERDYNE_AUTH_CLIENT_ID` + `CYBERDYNE_AUTH_CLIENT_SECRET`.
2. Caches the resulting `access_token` in memory along with the `expires_at`.
3. A background task refreshes at 90% of TTL (e.g. at 54 min for a 1h token).
4. The cached service token is the bearer for every outbound call this backend makes to CyberRAG, to CyberdyneAuth's admin endpoints (`/api/v1/admin/users/{id}/nft` for tier lookup), and to any other CyberdyneAuth-trusted service.

This replaces the user-impersonation refresh-token-rotation hack we'd have shipped pre-issue #2.

**Pattern still lifted from `geo_dashboard`** (caching shape, request coalescing, SHA-256 keys, resilience layer), but the call target moves from `/users/me` to `/auth/introspect`. The geo_dashboard files are still the right reference for everything *except* which endpoint to call:
- `geo_dashboard/backend/src/geosphere_backend/domain/ports/auth_port.py` — the port shape (rename `verify_bearer` → `introspect_token` to reflect the new contract).
- `geo_dashboard/backend/src/geosphere_backend/adapters/outbound/auth/caching_auth_port.py` — caching decorator structure (SHA-256 keys, leader pattern, only-cache-success).
- `orgpilot/backend/src/orgpilot/adapters/outbound/auth/amini_auth_client.py` — resilience wrapper.

Worth raising a follow-up with `geo_dashboard` and `orgpilot` maintainers: they can now migrate from `/users/me` to `/auth/introspect` for the same caching footprint with stronger semantics (proper `exp`, scopes, audience, token_type). Not blocking us.

**Remaining gaps from CyberdyneAuth (unchanged from pre-issue #2):**
- **No JWKS endpoint** — we still can't verify JWTs locally, so every cold-cache request is one introspect call. With 30s TTL and request coalescing, hit rate should be >95%. If high-RPS routes ever push this over budget, file the JWKS feature request.
- **Single `organization_id` per user** — multi-org isn't modeled. If we need richer tenancy, we maintain a local `tenant_membership` table (the geo_dashboard pattern).
- **No org name in `/users/me`** — only the UUID. Cache names locally if displayed.

**Domain shapes** — see §4 for `UserPrincipal`, `ServicePrincipal`, and the `Principal` discriminated union.

**Key endpoints (ours):**
- `GET /api/v1/me` — returns the merged user view (CyberdyneAuth profile + our local extras like enrolled paths, order summary, linked wallet from our DB). Only valid for user principals; service principals get a 403 ("use /api/v1/clients/me equivalent or the dedicated service routes").
- `POST /api/v1/me/link-wallet` — initiates wallet linking via CyberdyneAuth's EIP-191 challenge/verify pair (`POST /api/v1/auth/wallet/challenge` → frontend signs → `POST /api/v1/auth/wallet/verify`). Not SIWE / EIP-4361.
- Internal middleware: every request resolves `request.state.principal: Principal | None`.

**Key dependencies:** `httpx` async client (single instance, connection pool), our local resilience helpers (retry + circuit breaker, lift from OrgPilot). No JWT library — we don't decode tokens locally.

**Testing:**
- Unit: `FakeAuthClient` with canned introspect responses (active-user, active-service, inactive, 500, timeout); cache TTL eviction; request coalescing under concurrent load; resilience behaviour; service-token bootstrap + refresh-at-90%.
- Integration: `respx` mocks of `${BASE}/api/v1/auth/introspect`, `${BASE}/api/v1/users/me`, `${BASE}/api/v1/clients/me`, and `${BASE}/api/v1/auth/oauth2/token` covering the happy paths and 401/500/timeout for each.
- E2E (nightly): real client-credentials issuance against staging CyberdyneAuth + introspection of the issued token.
- Coverage: 100% on `domain/auth_identity` (tiny — value objects + Principal union).

### 5.2 Content & Blog

**Purpose:** Replace `products.ts`, `cyberdyne.ts`, `services.ts`, `team.ts` (static reference data) and add a real blog with categories, tags, drafts, slugs, and RSS.

**Representative endpoints:**
- `GET /api/v1/blog/posts?category=&tag=&page=&limit=` — paginated list, defaults to `published_at desc`, excludes drafts unless caller has `editor` claim.
- `GET /api/v1/blog/posts/{slug}` — full post by slug, 404 on draft for non-editors.
- `GET /api/v1/blog/rss.xml` — Atom-style feed, last 50 posts.
- `GET /api/v1/content/team` — team list (replaces `team.ts`).
- `GET /api/v1/content/projects` — replaces `products.ts`.
- `POST /api/v1/admin/blog/posts` — editor-only, body is markdown + frontmatter. Returns draft.
- `POST /api/v1/admin/blog/posts/{slug}/publish` — sets `published_at = now()`.

**Key dependencies:** SQLAlchemy repo, slug uniqueness constraint, markdown rendering on read (we store source `body_md`, never pre-rendered HTML — the frontend handles rendering).

**Testing:**
- Unit: slug normalization, draft visibility rule, RSS feed XML structure.
- Integration: real Postgres via `testcontainers`, end-to-end CRUD with idempotent slug collisions.

### 5.3 Learning Platform

**Purpose:** Back the `learn.ts` data plus user enrollment, progress, and (eventually) certificates with NFT verification hashes.

**Representative endpoints:**
- `GET /api/v1/learning/modules` and `GET /api/v1/learning/paths` — public catalog.
- `POST /api/v1/learning/paths/{slug}/enroll` — auth required, idempotent on `(user_id, path_id)`.
- `PATCH /api/v1/learning/modules/{slug}/progress` — body `{ percent: 0..100 }`. Sets `completed_at` automatically at 100.
- `GET /api/v1/learning/me` — current user's enrollments + per-module progress.
- `POST /api/v1/admin/learning/paths/{slug}/certificate/issue/{user_id}` — issues a certificate; in v1 it's just a signed JSON blob. Phase 6 mints the NFT.

**Key dependencies:** the `Content` module (a module's body markdown can be authored once and rendered identically to a blog post — same repo pattern).

**Testing:**
- Unit: progress invariant (100% ⇔ `completed_at`), enrollment idempotency, certificate eligibility predicate.
- Integration: enroll → progress → complete-all → certificate flow against real Postgres.

### 5.4 Marketplace + Stripe

**Purpose:** Productize `shop.ts` for real money. Three product types behave very differently:
- **Service** (`backend-api`, `frontend-dapp`, etc.) → routes to lead capture, no payment.
- **Training material** → one-time Stripe Checkout, on `paid` grants the user `enrollment` in a learning path linked to the product.
- **License** → one-time Stripe Checkout, on `paid` provisions a `LicenseKey` returned to the user (and emailed).

**Representative endpoints:**
- `GET /api/v1/marketplace/products?category=&type=` — public catalog.
- `POST /api/v1/marketplace/products/{slug}/checkout` — creates a Stripe Checkout Session, returns `{ url }`. For `service` type returns `{ redirect_to: "/contact?intent=…" }` instead.
- `POST /api/v1/stripe/webhook` — Stripe webhook receiver. Verifies signature with `stripe.Webhook.construct_event`, deduplicates via `WebhookEvent`, dispatches to a use case per event type.
- `GET /api/v1/me/orders` — user's orders.
- `GET /api/v1/me/licenses` — license keys for current user.

**Key dependencies:** `stripe-python`, `WebhookEvent` idempotency table, structured logging on every webhook (Stripe event id is the correlation ID).

**Testing:**
- Unit: webhook dispatcher (mocked Stripe events fixture — copy from Stripe CLI fixtures), license-key generator, redemption invariants.
- Integration: `stripe.Webhook.construct_event` with a known signing secret + canned payloads (no live Stripe calls in CI).
- Manual: Stripe CLI `stripe listen --forward-to localhost:8000/api/v1/stripe/webhook` is the dev loop, documented in README.

**Honest sizing:** this is the single biggest M of the roadmap. Webhook idempotency + license key delivery + refund handling + Coolify-friendly secret rotation is real work. Don't compress it.

### 5.5 Leads / Asks

**Purpose:** Back the Contact page (`/contact`) and the "marketplace service inquiry" path. Build a minimal CRM-ish queue (status + owner + notes). No SLA tracking in v1.

**Representative endpoints:**
- `POST /api/v1/asks` — public (with hCaptcha or Cloudflare Turnstile token; CyberdyneAuth doesn't gate this). Rate-limited per IP (5/min).
- `GET /api/v1/admin/asks?status=&channel=&q=` — editor-only paginated list.
- `PATCH /api/v1/admin/asks/{id}` — change status, assign owner, append note. Emits `AskEvent`.

**Key dependencies:** hCaptcha verifier (port + adapter), email notifier (port + adapter — `email-mock` in dev, SMTP in prod), `domain/leads` is otherwise self-contained.

**Testing:**
- Unit: status state machine (e.g. you can't reopen a closed ask without an explicit note), captcha verifier behaviour.
- Integration: full submit-then-list round-trip; rate limiter integration test with `slowapi` or hand-rolled token bucket.

### 5.6 AI Chat Agent

**Purpose:** Back the existing terminal-style chat surface with an OpenAI agent that can call tools to look up Cyberdyne content, project info, learning modules, and (optionally) on-chain user state. This is "the public face of the website knowing things about itself."

**Decision: knowledge backend.** Consume **CyberRAG** via MCP, do **not** roll inline pgvector. Three reasons:
1. CyberRAG already exists, has multi-tenant workspaces, hard-delete, graph-aware retrieval, and 95% test coverage. Reinventing it inline is weeks of work for a worse outcome.
2. The corpus is small (projects + blog + modules ≈ low thousands of chunks). CyberRAG handles this trivially in one workspace.
3. We want the same MCP tools that Claude Desktop / OrgPilot agents already use — alignment with the rest of the stack matters.

Cost of this choice: the backend depends on CyberRAG being up. Mitigated by (a) a cached `corpus_summary` blob refreshed every 15 min that the agent falls back to if CyberRAG is unreachable, (b) the agent's tools degrade — "lookup by slug" stays local because we own the canonical projects/blog tables. The agent only loses *semantic* search on outage.

**Representative endpoints:**
- `POST /api/v1/chat/sessions` — creates a session (anonymous OK), returns `{ session_id }`.
- `POST /api/v1/chat/sessions/{id}/messages` — body `{ content }`. Returns `text/event-stream` with the streamed assistant response and tool-call events.
- `GET /api/v1/chat/sessions/{id}` — history.

**Tool surface available to the LLM:**
- `lookup_project(slug)` → local DB.
- `list_projects(status?)` → local DB.
- `lookup_module(slug)` → local DB.
- `search_cyberdyne_knowledge(query, mode='hybrid')` → CyberRAG MCP `query_knowledge_graph`.
- `get_marketplace_product(slug)` → local DB.
- `create_ask_for_handoff(name, email, body, product_slug?)` → `Ask` row with channel `chat_agent_handoff`. Guarded — requires explicit user confirmation in the tool description.
- `get_user_tier()` → on-chain NFT tier read from the Web3 reader (§5.7), keyed by the user's linked wallet. Only callable when the request principal is a `UserPrincipal`; refuses for `ServicePrincipal` callers. The backend's *own* outbound call to CyberRAG uses its service token (not the user's), but the agent's *tools* are gated by the calling user's identity.

**Key dependencies:** `openai` 1.x async client, `fastmcp` client, SSE response (mind the Traefik buffering trap — see §9).

**Testing:**
- Unit: tool dispatcher (mocked OpenAI tool-call payloads), prompt assembly, redaction (no PII bleeding into logs).
- Integration: a fake OpenAI server returning canned tool-call sequences; CyberRAG mocked behind a port.
- Manual: a small `eval/` directory with 20 sample prompts and expected tool sequences — diffed in CI but not gating.

### 5.7 Web3 Reader

**Purpose:** Read-only on-chain access against **Base mainnet**. Backs the DAO view (treasury composition + DeFi positions), wallet investments panel, and the chat agent's `get_user_tier()` tool.

**Reads in v1:**
- `CyberdyneAccessNFT` balanceOf / tierOf for a wallet → backs NFT terminal + chat tier check.
- **Full DAO treasury composition for `TREASURY_ADDRESS`** (the DAO's smart contract address on Base):
  - **Plain ERC-20 balances** — USDC, WETH, and any other treasury assets held directly. Token list is admin-configured (env var `TREASURY_TOKEN_ADDRESSES`); no auto-discovery in v1.
  - **AAVE v3 positions** via the Aave Pool + Protocol Data Provider on Base:
    - Reserve list from `AaveProtocolDataProvider.getAllReservesTokens()`.
    - Per-reserve aToken balance (supplies), variableDebtToken balance, stableDebtToken balance for the DAO address.
    - Account summary via `Pool.getUserAccountData(TREASURY_ADDRESS)` → `totalCollateralBase`, `totalDebtBase`, `availableBorrowsBase`, `currentLiquidationThreshold`, `ltv`, `healthFactor`.
  - **Uniswap v4 positions** via the Position Manager + StateView on Base:
    - Enumerate ERC-721 positions owned by the DAO address from the v4 Position Manager.
    - For each position, decode the `PoolKey` (currency0, currency1, fee, tickSpacing, hooks), tick range, and liquidity.
    - Uncollected fees per token via StateView's position-info read (or `IPositionManager.getPositionInfo()` depending on the deployed interface — pin to the canonical Base mainnet addresses).
- `CyberdyneMarketplace` and `TrainingMaterials` contract reads where they overlap with off-chain products (e.g., is this license already minted on-chain?).

**DAO governance proposals: deferred.** We are *not* picking a Governor implementation yet (OpenZeppelin Governor + Timelock, Compound/Tally-style, Aragon, or custom). The frontend's "Recent Proposals" panel keeps rendering mock data from `daoData.ts` until that decision lands — see Open Q 11. The `GovernorAdapter` port is defined as a placeholder so the swap is small once a contract is chosen.

**Writes in v1: none.** The seam is defined (`OnchainSigner` port with one prod implementation that raises `NotImplementedError`) so we don't have to refactor in Phase 5. Dividend distribution / oracle updates ship later behind a feature flag, with the signer key in a KMS — not in env vars.

**Representative endpoints:**
- `GET /api/v1/dao/treasury` — top-level aggregate: total USD value, ERC-20 breakdown, AAVE account summary (health factor / LTV / total supply / total borrow), Uniswap v4 position count.
- `GET /api/v1/dao/positions/aave` — per-reserve AAVE positions (supplied + borrowed-variable + borrowed-stable, each with the underlying token symbol and USD value) plus the account summary.
- `GET /api/v1/dao/positions/uniswap-v4` — every Uniswap v4 LP position the DAO holds: pool key, tick range, liquidity, uncollected fees per token, and a computed pool price snapshot.
- `GET /api/v1/dao/dividends/next` — next distribution window. Off-chain admin-set schedule until the on-chain dividend mechanism ships (deferred with the Governor decision).
- `GET /api/v1/wallet/{address}/access-tier` — CyberdyneAccessNFT tier resolver, cached 5 min.

**Note:** `GET /api/v1/dao/proposals` is deliberately absent — see Open Q 11.

**Key dependencies:** `web3.py`, a multi-RPC adapter (primary RPC + backup — Base public RPC is rate-limited), a small ABI registry containing: AccessNFT (from `contracts/contracts/`), ERC-20 (standard), AAVE v3 Pool + ProtocolDataProvider + aToken + DebtToken (from `@aave/core-v3`), Uniswap v4 PoolManager + PositionManager + StateView (from `@uniswap/v4-core` and `@uniswap/v4-periphery` once the Base addresses are published). Caching is required: every call goes through a `TtlReadCache` port to avoid hammering RPC.

**Testing:**
- Unit: ABI decoding, cache TTL behaviour, multi-RPC fallback, AAVE health-factor / LTV math, Uniswap v4 position decoding.
- Integration: two flavors —
  - `anvil` with our own deployed mocks for AccessNFT / Marketplace / TrainingMaterials (the contracts we control).
  - **Mainnet-fork mode** (`anvil --fork-url <BASE_RPC>` against a pinned block) for AAVE v3 and Uniswap v4 reads. We don't redeploy AAVE or Uniswap in CI — that's days of work; we read from forked mainnet state.
  - Foundry binaries pulled in CI by a single `setup-foundry` step.
- Manual spot-check before sign-off: AAVE health factor + LTV match the AAVE UI for `TREASURY_ADDRESS`; Uniswap v4 positions + uncollected fees match the Uniswap UI for the same address.

### 5.8 DAO Read-Models

**Purpose:** Stitch Web3 reads + off-chain analytics into the shapes the frontend already consumes (`daoData.ts`: `TreasuryAsset[]`, `DaoProposal[]`, `DividendInfo`, `OperationalData`).

What's on-chain in v1: treasury composition (ERC-20s + AAVE positions + Uniswap v4 positions) — all sourced via §5.7. What's off-chain: operational data (monthly income / op costs / profit margin) — needs a dedicated `Treasury` aggregate in this backend, or pulled from OrgPilot's finance module via API (see Open Q 4). What's deferred entirely: proposals + on-chain dividend windows — those wait for the Governor decision (Open Q 11).

**Representative endpoints:** all under `GET /api/v1/dao/*` already listed in §5.7, plus `GET /api/v1/dao/operations` for the off-chain finance aggregate. The aggregator use case fans out to `web3_read` (on-chain) + `treasury_offchain` (Postgres tables fed by manual admin updates in v1, or OrgPilot pull if Open Q 4 lands that way).

**Testing:** mostly composition tests — the on-chain adapter is stubbed at the port boundary, off-chain aggregates are unit-tested over fixtures.

---

## 6. Frontend Integration Plan

Migration order is **cheapest first → most external-dep last**. Stripe sandbox bring-up is the long pole, so it goes last.

| Static file | New endpoint(s) | Migration order | Notes |
|---|---|---|---|
| `team.ts` | `GET /api/v1/content/team` | 1 (Phase 1) | Trivial, proves the deploy seam + CORS + cookie domain |
| `cyberdyne.ts` (beliefs, domains, tokenomics, roadmap) | `GET /api/v1/content/cyberdyne` (single bundle) | 1 (Phase 1) | Big read-only blob; one endpoint is fine |
| `services.ts` | `GET /api/v1/content/services` | 2 (Phase 2) | Same shape as content; trivial extension |
| `products.ts` | `GET /api/v1/content/projects` | 2 (Phase 2) | Reuse the project repo |
| `contact.ts` (channels) + `ContactView` POST | `GET /api/v1/content/contact-methods` + `POST /api/v1/asks` | 2 (Phase 2) | Asks API ships with this view; captcha required |
| `news.ts` | `GET /api/v1/blog/posts` + `GET /api/v1/blog/posts/{slug}` | 3 (Phase 3) | Drives the blog write-side too (admin endpoints) |
| `learn.ts` (modules, paths, resources) | `GET /api/v1/learning/{modules,paths}`, `GET /api/v1/content/resources` | 4 (Phase 4) | Adds enrollment/progress (auth-gated) |
| `daoData.ts` treasury + AAVE + Uniswap v4 positions | `GET /api/v1/dao/treasury`, `GET /api/v1/dao/positions/{aave,uniswap-v4}` | 5 (Phase 5) | Real on-chain reads against Base mainnet |
| `daoData.ts` operational data (income / costs / margin) | `GET /api/v1/dao/operations` | 5 (Phase 5) | Off-chain — admin uploads or pulled from OrgPilot (Open Q 4) |
| `daoData.ts` proposals + dividend countdown | (none yet) | **Deferred** | Stay static until a Governor contract is chosen (Open Q 11) |
| `investments.ts` (LP positions) | `GET /api/v1/me/wallet/positions` | 5 (Phase 5) | Wallet must be linked via CyberdyneAuth; reuses Uniswap v4 + AAVE adapters but for the *user's* address, not the DAO's |
| `shop.ts` + cart | `GET /api/v1/marketplace/products`, `POST .../{slug}/checkout` | 6 (Phase 6) | Last because Stripe + license fulfilment is the slowest external bring-up |

Frontend changes per phase: convert one or two static `*.ts` files into a `+page.server.ts` or `+layout.server.ts` `load()` that calls the new endpoint, with the static file kept around as a fallback for one PR for safety, then deleted.

---

## 7. Phased Roadmap

Six phases. Each phase is independently shippable — at the end of every phase the production frontend should still work, with strictly more endpoints behind it.

### Phase 1 — Skeleton + first endpoints (S, ~1 week)

**Goal:** prove the deploy seam end-to-end with the smallest possible surface.

**Scope:**
- Repo scaffold (`pyproject.toml`, `uv.lock`, `justfile`, `Dockerfile.coolify`, `compose.coolify.yaml`, `importlinter.cfg`, GitHub Actions CI with `pytest-cov fail_under=90` for `domain` + `application` packages — even though both are nearly empty).
- `infrastructure/` settings, logging, sentry shim (off in dev).
- `adapters/inbound/health` with `/healthz` and `/readyz`.
- `domain/auth_identity` + JWKS verification middleware against CyberdyneAuth. No `/me` endpoint yet.
- `domain/content` with `TeamMember` + `Project` + `Domain`/`Belief`/`RoadmapPhase` (seeded from the existing `*.ts` files via a one-shot Alembic data migration).
- Endpoints: `GET /api/v1/content/team`, `GET /api/v1/content/cyberdyne`.
- Coolify deploy to a new app `cyberdyne-backend` with Postgres sidecar.
- Frontend PR: swap `TeamView.svelte` and the `CyberddyneView.svelte` to call the new endpoints via `+page.server.ts`.

**Exit criteria:**
- Both endpoints serve from prod (`api.coolify.cyberdynecorp.ai`).
- CI coverage gate passes at ≥90% on `domain + application`.
- `import-linter` runs in CI and blocks PRs that violate layers.
- Frontend Team and Cyberdyne pages render from API in production.

**Dependencies:** none (CyberdyneAuth already in prod).

### Phase 2 — Content read-side + Leads/Asks (M, ~1.5 weeks)

**Goal:** finish the read-only public catalog and ship the Contact form for real.

**Scope:**
- `domain/content` extends with `ServiceSection`, `ResourceGroup`, `ContactMethod`.
- `domain/leads` + `application/leads` + `POST /api/v1/asks` + admin list endpoint.
- hCaptcha (or Turnstile) adapter behind a port — mocked in dev with a magic token.
- Email notifier port + SMTP adapter (mock in dev, SMTP_URL in prod). Wire to fire on new ask.
- Frontend PRs: swap `ServicesView`, `ProductsView`, `ContactView`.

**Exit criteria:**
- Submit on `/contact` lands a row in Postgres, fires an email, and the admin can list via `gh api`-style curl + cookie.
- 90% coverage gate still green; `leads` domain at 100%.
- Captcha + rate limiter on `POST /api/v1/asks` both enforced and integration-tested.

**Dependencies:** Phase 1 (deploy seam, auth middleware).

### Phase 3 — Blog (M, ~1.5 weeks)

**Goal:** real CMS-less blog, drafts, RSS, admin authoring.

**Scope:**
- `domain/content/blog` (separate from the rest of `content` because authoring lifecycle is different).
- Public read endpoints + admin write endpoints (auth claim `editor: true` required).
- RSS / Atom feed.
- Markdown source-of-truth in Postgres, but ship a `tools/sync_md_blog.py` CLI that bulk-imports `*.md` from a `content/blog/` folder for git-authored posts.
- Frontend PR: swap `NewsView.svelte` to call the API.

**Exit criteria:**
- Five real posts authored via the import CLI live on prod.
- Drafts hidden from anon; visible to `editor`.
- `/blog/rss.xml` validates against W3C feed validator.

**Dependencies:** Phase 1 (auth claims).

### Phase 4 — Learning platform (M, ~2 weeks)

**Goal:** learners can enroll in paths and track progress; admins can issue (non-NFT) certificates.

**Scope:**
- `domain/learning` (`Module`, `Path`, `Enrollment`, `ModuleProgress`, `Certificate`).
- Endpoints per §5.3.
- Frontend changes in `LearnView.svelte`: replace static lists, add "Continue" CTA driven by `GET /api/v1/learning/me`.
- Certificate JSON: signed with an Ed25519 key held in Coolify env (`CERT_SIGNING_KEY`); verification endpoint included.

**Exit criteria:**
- A test user can enroll, progress through a path, and download a signed certificate JSON.
- Progress invariants enforced in domain layer with property-based tests (`hypothesis`).
- Coverage still ≥90%.

**Dependencies:** Phase 1.

### Phase 5 — Web3 read + DAO treasury & DeFi positions (M, ~2.5 weeks)

**Goal:** the DAO view's treasury and DeFi-position panels are sourced from on-chain reality on Base mainnet for the DAO smart contract address. Proposals and dividend countdown stay rendering mock data — they're deferred until a Governor contract is chosen (Open Q 11).

**Scope:**
- `domain/web3_read` + `domain/dao_readmodel` with their use cases.
- `web3.py` adapter, multi-RPC fallback (primary + backup), ABI registry covering: `CyberdyneAccessNFT` (own contracts), ERC-20 standard, AAVE v3 (`Pool`, `ProtocolDataProvider`, `aToken`, `VariableDebtToken`, `StableDebtToken`), Uniswap v4 (`PoolManager`, `PositionManager`, `StateView`).
- **AAVE v3 reader** for `TREASURY_ADDRESS`: enumerate reserves on Base, fetch per-reserve aToken / variableDebtToken / stableDebtToken balances, plus `getUserAccountData` for the health factor / LTV / liquidation threshold / total collateral / total debt / available borrows.
- **Uniswap v4 reader** for `TREASURY_ADDRESS`: enumerate Position Manager NFTs owned by the DAO, decode each position's `PoolKey` + tick range + liquidity, and read uncollected fees per token via StateView.
- **ERC-20 reader**: balances for the admin-configured `TREASURY_TOKEN_ADDRESSES` list (USDC, WETH, and anything else the DAO holds).
- USD valuation: prefer on-chain oracles (Chainlink on Base) for token-to-USD rates; fall back to a configured static map for stablecoins.
- Foundry-based integration suite in CI:
  - `anvil` + our own deployed mocks for AccessNFT / Marketplace / TrainingMaterials.
  - `anvil --fork-url <BASE_RPC>` at a pinned block for AAVE + Uniswap v4 (we don't redeploy those — too expensive in CI).
- Scheduler (`apscheduler`) refreshing `TreasurySnapshot`, `AavePositionSnapshot[]`, and `UniswapV4PositionSnapshot[]` every 5 min; `NftTierCache` populated lazily.
- Endpoints per §5.7.
- Frontend: swap `DaoView` (treasury + AAVE + Uniswap v4 panels), `InvestmentsView`, `NFTTerminal`. Proposals + dividend countdown panels keep their mock data with a small "demo data" badge until governance phase.

**Exit criteria:**
- DAO view renders real treasury (ERC-20s + AAVE supplies/borrows with health factor + Uniswap v4 LP positions with uncollected fees) in prod.
- RPC outage path: fallback RPC takes over within one retry, errors logged + Sentry breadcrumb.
- AccessNFT tier from chain agrees with CyberdyneAuth's view (sanity test).
- AAVE account summary (health factor, LTV) matches the AAVE UI for `TREASURY_ADDRESS` (manual spot check).
- Uniswap v4 positions + uncollected fees match the Uniswap UI for `TREASURY_ADDRESS` (manual spot check).
- Coverage gate still ≥90%.

**Out of scope (explicit):**
- Governance proposals — deferred (Open Q 11).
- On-chain dividend distribution mechanics — deferred (depends on Governor + tokenomics decisions).
- Write-side Web3 / signing — deferred.
- Historical PnL, fee-accrual-over-time, impermanent loss — requires an event indexer; revisit in Phase 7+ (Open Q 12).
- Auto-discovery of DAO-held tokens — token list is admin-configured.

**Dependencies:** Phase 1. Independent of Phase 3/4 — can run in parallel with them.

### Phase 6 — Marketplace + Stripe + AI chat (L, ~3 weeks)

**Goal:** make money; turn the terminal chat into the real public face.

**Scope:**

**Marketplace (L sub-scope on its own):**
- `domain/marketplace` (`Product`, `Order`, `LicenseKey`, `WebhookEvent`).
- Stripe Checkout integration, webhook handler with idempotency table.
- License key generation + email delivery + revocation endpoint.
- Refund handling: `charge.refunded` revokes license & emails.
- `service` products route to `Ask` creation, not Stripe.

**AI chat (M sub-scope):**
- `domain/ai_chat` + `application/ai_chat`.
- OpenAI adapter with tool calling, SSE response endpoint.
- CyberRAG MCP client adapter.
- Tool surface per §5.6.

These two share the phase because they're both external-dep-heavy and benefit from one Coolify config push.

**Exit criteria:**
- Stripe test mode end-to-end: training purchase → enrollment auto-granted; license purchase → key emailed + visible in `/me/licenses`.
- Chat agent answers "what is CyberSTAC?", "what training do you offer in DeFi?", and "I need help with a Web3 dApp project" (the last one creates an Ask).
- All Stripe webhook event types in scope have a corresponding application handler + idempotency test.
- Coverage gate still ≥90%.

**Dependencies:** Phase 1 (auth), Phase 4 (learning enrollment auto-grant on training purchase). CyberRAG must be reachable on the same Coolify network (or via auth-gated public URL).

### Effort summary

| Phase | Effort | Real calendar with one engineer |
|---|---|---|
| 1 | S | ~1 week |
| 2 | M | ~1.5 weeks |
| 3 | M | ~1.5 weeks |
| 4 | M | ~2 weeks |
| 5 | M | ~2.5 weeks |
| 6 | L | ~3 weeks |
| **Total** | | **~11.5 weeks** to full migration, with deployable value after each phase |

---

## 8. Testing Strategy

### What's a unit test vs. an integration test

- **Unit:** anything in `domain/` or `application/`. No I/O. No SQLAlchemy session, no real HTTP, no real OpenAI, no real Stripe. Ports are replaced with fakes (hand-written, not `MagicMock` — fakes carry behaviour). These are the only tests counted toward the 90% gate.
- **Integration:** anything in `adapters/` or anything that crosses a process boundary. Real Postgres via `testcontainers-python`, real `anvil` for Web3, `respx` for outbound HTTP, the Stripe official fixtures for webhook payloads, FastMCP test client for CyberRAG. These run on every PR but are **not** counted toward the 90% gate (they exist for adapters, where line coverage is misleading).
- **E2E:** opt-in CI job triggered by the `e2e` label or nightly. Real OpenAI key, real CyberRAG against staging, real Stripe test mode. Three flows: marketplace purchase, chat with tool call to CyberRAG, DAO view aggregation.

### Enforcing 90%

`pyproject.toml`:

```toml
[tool.coverage.report]
fail_under = 90
show_missing = true
skip_covered = true

[tool.coverage.run]
source = ["src/cyberdyne_backend/domain", "src/cyberdyne_backend/application"]
omit = ["**/__init__.py"]
```

Adapters are explicitly excluded from the denominator — same calibration as CyberdyneAuth. Their correctness lives in integration tests.

CI step: `uv run pytest -q --cov --cov-fail-under=90`. If you ever need to ship a temporary regression, the only allowed escape hatch is a PR that bumps the threshold *down* — never a per-line `# pragma: no cover` outside of `__repr__` and TYPE_CHECKING blocks.

### Architecture enforcement

`importlinter.cfg`:

```ini
[importlinter]
root_packages = cyberdyne_backend

[importlinter:contract:layers]
name = Hexagonal layers
type = layers
layers =
    cyberdyne_backend.adapters.inbound
    cyberdyne_backend.adapters.outbound
    cyberdyne_backend.infrastructure
    cyberdyne_backend.application
    cyberdyne_backend.domain
ignore_imports =
    cyberdyne_backend.main -> *

[importlinter:contract:context_isolation]
name = Bounded contexts cannot import each other's internals
type = independence
modules =
    cyberdyne_backend.domain.content
    cyberdyne_backend.domain.learning
    cyberdyne_backend.domain.marketplace
    cyberdyne_backend.domain.leads
    cyberdyne_backend.domain.ai_chat
    cyberdyne_backend.domain.web3_read
```

Run via `lint-imports` in CI; same step is a `pre-commit` hook locally.

### How we mock the external dependencies

| Dep | In unit | In integration | In e2e |
|---|---|---|---|
| CyberdyneAuth | hand-written `FakeAuthClient` returning canned introspection + profile responses | `respx` mocks of `${BASE}/api/v1/auth/introspect`, `/users/me`, `/clients/me`, `/auth/oauth2/token` covering 200 / 401 / 5xx / timeout for each | real staging CyberdyneAuth + real client-credentials issuance |
| PostgreSQL | not used (UoW is mocked) | `testcontainers-python` Postgres | real CI Postgres |
| Stripe | `FakeStripeGateway` port impl | `stripe.Webhook.construct_event` with canned official fixtures | Stripe test mode + Stripe CLI in nightly |
| OpenAI | `FakeChatCompletions` returning scripted tool-call sequences | local stub server | real key, gated behind nightly job |
| CyberRAG | `FakeRagClient` returning fixture documents | FastMCP test client against an in-process FastMCP server | real CyberRAG staging |
| Web3 / Base RPC | `FakeWeb3` returning canned values per ABI call | `anvil` + deployed `contracts/contracts/*.sol` | Base sepolia, nightly only |
| SMTP | `FakeEmailSender` capturing payloads | `aiosmtpd` test server | none |

The pattern: **one fake per outbound port, hand-written, lives next to the port**. We don't use `unittest.mock` outside of trivial cases.

---

## 9. Deployment

### Coolify app shape

One Coolify application: **cyberdyne-backend**.
- **Buildpack:** Dockerfile, target `production`, context `./backend`.
- **Networking:** `expose: ["8000"]` only — never `ports:`. Traefik label routes from `api.coolify.cyberdynecorp.ai`.
- **Healthcheck:** `/healthz` with `start_period=15s` to let `alembic upgrade head` finish.
- **Sidecar:** PostgreSQL 17 on the internal Coolify network. `DATABASE_URL` injected via env.

### Build-time vs runtime env vars

Follow the OrgPilot recipe — **anything baked into the build is `is_build = true`** in Coolify (Sentry release tag, build-time auth tokens for private indices like `NPM_TOKEN` if we ever ship a frontend artifact from this repo — which we shouldn't). Everything else is `is_runtime = true`.

**Build-time (`is_build`):**
- `UV_LINK_MODE=copy` (set in Dockerfile but reiterated in Coolify for clarity)
- `SENTRY_RELEASE` (computed from commit SHA at build)

**Runtime (`is_runtime`):**

| Var | Purpose |
|---|---|
| `DATABASE_URL` | Postgres DSN, async driver |
| `DATABASE_POOL_SIZE` | default 10 — see the Coolify trap on connection limits |
| `DATABASE_MAX_OVERFLOW` | default 20 |
| `CYBERDYNE_AUTH_BASE_URL` | `https://auth.backend.coolify.cyberdynecorp.ai` |
| `CYBERDYNE_AUTH_INTROSPECTION_TTL_S` | per-token cache TTL for `/api/v1/auth/introspect` results; default 30 |
| `CYBERDYNE_AUTH_PROFILE_TTL_S` | per-subject cache TTL for `/api/v1/users/me` and `/api/v1/clients/me` lazy lookups; default 60 |
| `CYBERDYNE_AUTH_CLIENT_ID` | this backend's OAuth client id (issued via `POST /api/v1/admin/oauth/clients`) |
| `CYBERDYNE_AUTH_CLIENT_SECRET` | the client secret (shown once at registration / rotation; rotate via `POST /api/v1/admin/oauth/clients/{id}/rotate-secret`) |
| `CYBERDYNE_AUTH_OAUTH_SCOPES` | space-separated scopes this backend requests when issuing service tokens (e.g. `cyberrag:query iam:read.tier`) |
| `CYBERDYNE_AUTH_OAUTH_AUDIENCE` | optional `audience` parameter when requesting service tokens (RFC 8707) — set to the URL of the service we're calling, e.g. `https://cyberrag.coolify.cyberdynecorp.ai` |
| `COOKIE_DOMAIN` | `.coolify.cyberdynecorp.ai` (for any redirect URLs we emit) |
| `CORS_ORIGINS` | comma-sep list including `https://cyberdynecorp.ai`, dev origins |
| `STRIPE_SECRET_KEY` | live or test; rotated quarterly |
| `STRIPE_WEBHOOK_SECRET` | unique per environment |
| `STRIPE_SUCCESS_URL`, `STRIPE_CANCEL_URL` | full URLs |
| `OPENAI_API_KEY` | scoped key, monthly cap |
| `OPENAI_MODEL_DEFAULT` | `gpt-4o-mini` |
| `OPENAI_MODEL_TOOL` | `gpt-4o` |
| `CYBERRAG_BASE_URL` | internal Coolify URL preferred |
| `CYBERRAG_BEARER_TOKEN` | *not used* — outbound CyberRAG calls authenticate with this backend's service token, minted at startup via the client-credentials flow (see §5.1); kept in the table only as a placeholder if CyberRAG ever requires a separate side-channel key |
| `BASE_RPC_URL_PRIMARY` | Alchemy or self-hosted |
| `BASE_RPC_URL_FALLBACK` | public Base RPC |
| `ACCESSNFT_ADDRESS`, `MARKETPLACE_ADDRESS`, `TRAININGMATERIALS_ADDRESS` | from `contracts/scripts` deploy output |
| `TREASURY_ADDRESS` | the DAO's smart contract address on Base; the owner whose positions we read |
| `TREASURY_TOKEN_ADDRESSES` | comma-sep ERC-20 addresses the DAO holds directly (USDC, WETH, …); no auto-discovery in v1 |
| `AAVE_V3_POOL_ADDRESS`, `AAVE_V3_DATA_PROVIDER_ADDRESS` | canonical Base mainnet deployment addresses |
| `UNISWAP_V4_POOL_MANAGER_ADDRESS`, `UNISWAP_V4_POSITION_MANAGER_ADDRESS`, `UNISWAP_V4_STATE_VIEW_ADDRESS` | canonical Base mainnet deployment addresses |
| `CHAINLINK_PRICE_FEEDS_JSON` | optional map of `{ token_address: chainlink_feed_address }` for USD valuation; stablecoins fall back to 1.0 |
| `GOVERNOR_ADDRESS` | *deferred — set when a Governor contract is chosen (Open Q 11)* |
| `CERT_SIGNING_KEY` | Ed25519 PEM, runtime only |
| `EMAIL_PROVIDER` | `smtp` / `mock` |
| `SMTP_URL` | when provider=smtp |
| `CAPTCHA_PROVIDER` | `turnstile` / `hcaptcha` / `mock` |
| `CAPTCHA_SECRET` | provider secret |
| `SENTRY_DSN` | optional |
| `LOG_LEVEL` | default `INFO` |

### Traps to plan around

These are pulled directly from `Coolify Tricks and Traps.md` and adapted:

- **`UV_LINK_MODE=copy`** — non-negotiable; missing it gives `ModuleNotFoundError` at runtime despite a green build.
- **`uv.lock` committed and `--frozen` in Docker** — otherwise builds are non-reproducible.
- **Multi-stage build, `--no-install-project` in the deps stage** — otherwise the build fails at the deps stage because source isn't copied yet.
- **`expose: ["8000"]`, not `ports:`** — otherwise port conflict with Traefik.
- **SSE for the chat endpoint** — set `X-Accel-Buffering: no`, add the Traefik middleware in Coolify Advanced Labels, and use `StreamingResponse` not `JSONResponse`.
- **DB connection pool sized for blue/green** — during a rolling deploy you have 2× the configured pool open at once. With default Postgres `max_connections=100`, that means `pool_size + max_overflow ≤ 40` per replica.
- **Stripe webhook secret per environment** — rotating one bricks the other if you share.
- **`alembic upgrade head` in entrypoint, `exec uvicorn`** — `exec` so SIGTERM reaches the app for graceful shutdown.
- **`.dockerignore`** — exclude `__pycache__`, `.venv`, `.git`, `.pytest_cache`, `.mypy_cache`, `tests/`.

### Local dev loop

`just dev` runs:
1. `docker compose -f compose.dev.yaml up -d` — Postgres + an in-network `cyberdyneauth-mock` (returns canned JWKS + claims) + `anvil` for Web3.
2. `alembic upgrade head`.
3. `uvicorn cyberdyne_backend.main:app --reload --port 8000`.

`just stripe-listen` runs `stripe listen --forward-to localhost:8000/api/v1/stripe/webhook` and prints the signing secret to paste into `.env.local`.

---

## 10. Open Questions

These need a decision before the corresponding phase starts. None block Phase 1.

1. **Stripe Connect vs single-tenant Stripe?** — Roadmap commits to single-tenant. If the marketplace ever lists third-party sellers (e.g., Surf4Me service providers), Connect becomes necessary. Decide before Phase 6.
2. **Self-host the OpenAI key vs proxy through OrgPilot's LLM service?** — OrgPilot already has an `LlmRouter` adapter with model fallbacks, budget caps, and per-org rate limits. Reusing it means one less key to rotate and centralized budget tracking. Decide before Phase 6. Default if no decision: self-host (faster to ship).
3. **CyberRAG workspace per environment or shared?** — Probably per environment (`cyberdyne-website-prod`, `cyberdyne-website-staging`). Confirm with whoever owns CyberRAG ops.
4. **Treasury off-chain finance data: own it here, or read from OrgPilot?** — OrgPilot owns company-finance. Duplicating monthly income / op costs / profit margin in the website backend is awkward. Default plan: read via OrgPilot's REST API in Phase 5, fall back to admin-uploaded snapshots if OrgPilot isn't reachable.
5. **Certificates as NFTs?** — Phase 4 ships signed JSON certificates only. NFT minting (with an admin signer + gas budget) is Phase 7+ work. Decide whether the JSON certificate's `verification_hash` should already embed an IPFS CID so the eventual NFT can reference it without re-hashing.
6. **Blog authoring UI?** — v1 is markdown via admin POST or git import CLI. Decide whether to bolt a Tiptap-based editor onto the existing admin SPA, or to keep it API-only.
7. **Background work scheduler choice** — `apscheduler` in-process (simple, one less moving part) vs `arq` + Redis (works across replicas). Default: `apscheduler` until the moment we run 2+ replicas, at which point switch to `arq`.
8. **Rate limiting strategy** — `slowapi` (in-process) vs a Redis-backed token bucket. Default: `slowapi` until traffic justifies otherwise. Captcha covers the most abusive endpoint already.
9. **~~Service-account identity for backend-to-backend calls~~** ✅ **RESOLVED** by [CyberdyneAuth#2](https://github.com/CyberdyneCorp/CyberdyneAuth/issues/2). CyberdyneAuth now ships the full OAuth 2.0 client-credentials grant (`POST /api/v1/auth/oauth2/token`), RFC 7662 introspection (`POST /api/v1/auth/introspect`), and a `GET /api/v1/clients/me` companion. Admin CRUD for clients lives under `/api/v1/admin/oauth/clients/*` including secret rotation with a grace window. Our backend registers as a client, holds `CYBERDYNE_AUTH_CLIENT_ID` + `CYBERDYNE_AUTH_CLIENT_SECRET`, exchanges them for an access token on startup, and refreshes at 90% of TTL — see §5.1. No interim hacks needed.
10. **Domain name** — `api.coolify.cyberdynecorp.ai` is the default. If we want a clean public surface for the chat endpoint (e.g., `chat.cyberdynecorp.ai`) decide before Phase 6 to avoid a CORS/cookie rebuild.
11. **Which DAO governance contract to deploy?** — Deferred from v1; the frontend's Proposals + dividend-countdown panels stay on mock data until this lands. Realistic options: (a) OpenZeppelin Governor + TimelockController — most boring, widest ecosystem support, easy to audit; (b) Compound/Tally-style Governor — deepest existing tooling, ties UI to Tally; (c) custom contract aligned to the CBY tokenomics — most flexible, most audit surface. Companion decision: on-chain dividend windows (a `Distributor` contract emitting a `DistributionScheduled` event) vs. off-chain admin-set schedules. Decide before any frontend work depends on real proposals.
12. **Position fee accrual: live read vs event indexing?** — Phase 5 takes the simple path — every 5 min poll uncollected fees and decode them. Historical fee earnings, APY-over-time charts, and IL math need an event indexer (Subgraph or self-hosted). Decide in Phase 7+ whether to consume Uniswap's official Subgraph for Base, ship our own minimal indexer, or skip historical analytics entirely.
