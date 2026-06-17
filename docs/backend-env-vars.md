# Backend env-var cheat sheet

> Source of truth: `backend/src/cyberdyne_backend/infrastructure/settings.py`
> (pydantic-settings, `case_sensitive=false` — the env var is the
> UPPER_SNAKE of each field). This page is the Coolify-config companion;
> when you add a setting, add a row here. Issue #7.

Settings load from process env first, then a local `.env` file. Anything
unset falls back to the default below — and several defaults are **mock /
dev-only adapters** that must be replaced before a real go-live (see
[Production checklist](#production-checklist)).

## Runtime

| Env var | Default | Notes |
|---------|---------|-------|
| `ENVIRONMENT` | `local` | `local` \| `ci` \| `staging` \| `production`. Gates the production guardrail. |
| `LOG_LEVEL` | `INFO` | DEBUG / INFO / WARNING / ERROR (upper-cased). |
| `PORT` | `8000` | |
| `ENFORCE_PRODUCTION_ADAPTERS` | `false` | When `true`, app startup **hard-fails** in staging/production if any dev-default mock adapter is still active. Default warns + boots. Flip on once everything below is provisioned. |
| `CORS_ORIGINS` | `http://localhost:5173` | Comma-separated allowed origins; set to the frontend FQDN(s) in prod. |
| `PUBLIC_SITE_URL` | `http://localhost:5173` | Used for absolute URLs (RSS, certificate verify links). |

## Database

| Env var | Default | Notes |
|---------|---------|-------|
| `DATABASE_URL` | `postgresql+asyncpg://cyberdyne:cyberdyne@localhost:5433/cyberdyne` | Async SQLAlchemy DSN. Coolify injects the sidecar DSN in prod. |
| `DATABASE_ECHO` | `false` | SQL echo (debug). |
| `DATABASE_POOL_SIZE` | `10` | |
| `DATABASE_MAX_OVERFLOW` | `20` | |

## CyberdyneAuth

| Env var | Default | Notes |
|---------|---------|-------|
| `CYBERDYNE_AUTH_BASE_URL` | `https://auth.backend.coolify.cyberdynecorp.ai` | Upstream auth root (RFC 7662 introspection + profile). |
| `CYBERDYNE_AUTH_INTROSPECTION_TTL_S` | `30` | Introspection cache TTL. |
| `CYBERDYNE_AUTH_PROFILE_TTL_S` | `60` | `/users/me` profile cache TTL. |
| `CYBERDYNE_AUTH_REQUEST_TIMEOUT_S` | `5.0` | |
| `CYBERDYNE_AUTH_CLIENT_ID` | _(unset)_ | Client-credentials for this backend's own outbound calls (chat → CyberRAG, NFT-tier). |
| `CYBERDYNE_AUTH_CLIENT_SECRET` | _(unset)_ | 🔒 secret. |
| `CYBERDYNE_AUTH_OAUTH_SCOPES` | `""` | |
| `CYBERDYNE_AUTH_OAUTH_AUDIENCE` | _(unset)_ | |

## Captcha (contact form)

| Env var | Default | Notes |
|---------|---------|-------|
| `CAPTCHA_PROVIDER` | `mock` ⚠️ | `mock` (always-pass) \| `turnstile` (Cloudflare). |
| `CAPTCHA_SECRET` | _(unset)_ | 🔒 required when provider is `turnstile`. |

## Certificates (learning)

| Env var | Default | Notes |
|---------|---------|-------|
| `CERT_SIGNING_KEY` | _(unset)_ | 🔒 HMAC-SHA256 key for signing certificates. Unset → ephemeral key (dev only; verify-by-id won't survive a restart). |

## DAO treasury / Web3

| Env var | Default | Notes |
|---------|---------|-------|
| `CHAIN_READER_PROVIDER` | `fake` ⚠️ | `fake` (deterministic stub) \| `web3py` (real RPC). |
| `DAO_TREASURY_ADDRESS` | _(unset)_ | Multisig on Base. Unset → `/api/v1/dao/overview` 503s. |
| `BASE_RPC_URL` | _(unset)_ | Required when provider is `web3py`. |
| `AAVE_POOL_DATA_PROVIDER` | `0x2A09…dFBa` | Base deployment; override only if it moves. |
| `UNISWAP_V4_POSITION_MANAGER` | `0x7C5f…9bDc` | Base deployment. |
| `CYBERDYNE_ACCESS_NFT_ADDRESS` | _(unset)_ | CyberdyneAccessNFT contract backing `GET /api/v1/wallet/{address}/access-tier`. Unset → stub reader reports "no access NFT" for every address; real web3py reader lands with `BASE_RPC_URL`. |
| `DAO_SNAPSHOT_TTL_S` | `300` | Chain-snapshot cache TTL. |
| `DAO_HOLDERS_COUNT` | `0` | Surfaced in `/dao/overview` until the governance subgraph ships. |

## Marketplace / Stripe

| Env var | Default | Notes |
|---------|---------|-------|
| `STRIPE_SECRET_KEY` | _(unset)_ ⚠️ | 🔒 unset → `MockStripeCheckoutClient`. |
| `STRIPE_WEBHOOK_SECRET` | _(unset)_ ⚠️ | 🔒 unset → `MockStripeWebhookVerifier` (trusts every payload). |
| `STRIPE_SUCCESS_URL` | `http://localhost:5173/marketplace?session={CHECKOUT_SESSION_ID}` | |
| `STRIPE_CANCEL_URL` | `http://localhost:5173/marketplace?cancelled=1` | |

## AI chat

| Env var | Default | Notes |
|---------|---------|-------|
| `OPENAI_API_KEY` | _(unset)_ ⚠️ | 🔒 unset → `StaticChatClient` (fixed offline reply). |
| `OPENAI_MODEL` | `gpt-4o-mini` | |
| `CYBERRAG_MCP_URL` | _(unset)_ | Unset → stub knowledge search ("no semantic index"). |
| `MATLAB_BACKEND_URL` | `https://matlab-backend.coolify.cyberdynecorp.ai` | `matlab_*` tools proxy here. |
| `PYTHON_INTERPRETER_URL` | `https://interpreter.backend.coolify.cyberdynecorp.ai` | `python_exec` + code-run lessons. |
| `CYBERFLIES_URL` | `https://cyberflies.backend.coolify.cyberdynecorp.ai` | Meetings tools. |

## Uploads / media

| Env var | Default | Notes |
|---------|---------|-------|
| `MEDIA_ROOT` | `./uploads` | Point at the Coolify persistent volume in prod. |
| `MEDIA_URL_PREFIX` | `/media` | Read-only static mount prefix. |

## Production checklist

Defaults marked ⚠️ above are dev-only mocks. Before flipping
`ENFORCE_PRODUCTION_ADAPTERS=true` (which will then refuse to boot until
each is resolved), provision:

- `CHAIN_READER_PROVIDER=web3py` + `BASE_RPC_URL` (+ `DAO_TREASURY_ADDRESS`)
- `CAPTCHA_PROVIDER=turnstile` + `CAPTCHA_SECRET`
- `STRIPE_SECRET_KEY` + `STRIPE_WEBHOOK_SECRET`
- `OPENAI_API_KEY`

Also recommended for prod regardless of the guardrail: `CERT_SIGNING_KEY`
(stable certificate verification), real `CORS_ORIGINS` / `PUBLIC_SITE_URL`,
and a `MEDIA_ROOT` on a persistent volume.

### Local dev

Run `stripe listen --forward-to localhost:8000/api/v1/stripe/webhook` and
use the printed `whsec_…` as `STRIPE_WEBHOOK_SECRET` — never point the dev
box at the production Stripe webhook.
