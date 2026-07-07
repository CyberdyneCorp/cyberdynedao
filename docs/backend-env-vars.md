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
| `CYBERDYNE_AUTH_BASE_URL` | `https://auth.backend.coolify.cyberdynecorp.ai` | Upstream auth root (JWKS + `/users/me` profile). |
| `CYBERDYNE_AUTH_JWKS_PATH` | `/.well-known/jwks.json` | Path (under base URL) of the public signing keys used to verify RS256 access tokens. |
| `CYBERDYNE_AUTH_ACCEPTED_ISSUERS` | `cyberdyne-auth https://auth.backend.coolify.cyberdynecorp.ai` | Space-separated `iss` values trusted on access tokens. Two are accepted while CyberdyneAuth's token `iss` and OIDC discovery issuer are being aligned (CyberdyneAuth#47). |
| `CYBERDYNE_AUTH_TOKEN_LEEWAY_S` | `60` | Clock-skew tolerance for `exp`/`iat`/`nbf`. |
| `CYBERDYNE_AUTH_JWKS_MIN_REFRESH_S` | `10.0` | Minimum seconds between JWKS re-fetches triggered by an unknown `kid`. |
| `CYBERDYNE_AUTH_INTROSPECTION_TTL_S` | `30` | Verified-token cache TTL (token → principal). |
| `CYBERDYNE_AUTH_PROFILE_TTL_S` | `60` | `/users/me` profile cache TTL. |
| `CYBERDYNE_AUTH_REQUEST_TIMEOUT_S` | `5.0` | Timeout for the JWKS / profile HTTP calls. |
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
| `CERT_SIGNER` | `hmac` | `hmac` (shared secret, our backend verifies) or `ed25519` (keypair — external verifiers use the published public key at `GET /api/v1/learning/certificates/signing-key`). |
| `CERT_SIGNING_KEY` | _(unset)_ | 🔒 HMAC-SHA256 key (`CERT_SIGNER=hmac`). Unset → ephemeral key (dev only; verify-by-id won't survive a restart). |
| `CERT_ED25519_PRIVATE_KEY` | _(unset)_ | 🔒 base64url 32-byte seed (`CERT_SIGNER=ed25519`). Required when that scheme is selected. |

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
| `DAO_SNAPSHOT_PREWARM` | `true` | Background worker re-reads the snapshot every `DAO_SNAPSHOT_TTL_S` so the DaoView is served from a warm cache. Inert unless `DAO_TREASURY_ADDRESS` is set; disable for purely-lazy caching. |
| `DAO_HOLDERS_COUNT` | `0` | Surfaced in `/dao/overview` until the governance subgraph ships. |

## Course recommendations

| Env var | Default | Notes |
|---------|---------|-------|
| `RECOMMENDATIONS_CACHE_TTL_S` | `21600` (6h) | Per-user TTL for the `GET /api/v1/recommendations/me` result. Without it every request pays a synchronous LLM round-trip on the app-launch hot path. Recommendations change rarely, so results may be up to this stale (mid-TTL progress won't reflect until expiry). The cache is in-process, hence **per-worker** with `--workers > 1`; the Dockerfile runs a single worker so today it is process-wide. The endpoint and the chat-agent recommend tool share one cache per user. |

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

## Email (notifications + license delivery)

| Env var | Default | Notes |
|---------|---------|-------|
| `EMAIL_PROVIDER` | `logging` | `logging` (logs every notification — dev/test default) \| `smtp` (deliver via the relay below). |
| `SMTP_HOST` | _(unset)_ | Relay hostname. Required to actually send when provider is `smtp`; unset → falls back to logging. |
| `SMTP_PORT` | `587` | Submission port (STARTTLS). |
| `SMTP_USERNAME` | _(unset)_ | SMTP auth user (optional for unauthenticated relays). |
| `SMTP_PASSWORD` | _(unset)_ | 🔒 SMTP auth password. |
| `SMTP_USE_TLS` | `true` | STARTTLS on connect. Disable only for a local plaintext relay (e.g. MailHog). |
| `EMAIL_FROM` | `no-reply@cyberdynecorp.ai` | Envelope From for outbound mail. |
| `EMAIL_ADMIN_RECIPIENT` | _(unset)_ | Team inbox new-ask (lead/contact) notifications go to. Required for SMTP ask notifications; unset → asks log only while license emails still send. |

Any SMTP relay works (Postmark / SES / Mailgun / Gmail). License-key
emails always go to the buyer's address; new-ask notifications go to
`EMAIL_ADMIN_RECIPIENT`.

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
(stable certificate verification), `EMAIL_PROVIDER=smtp` + the SMTP relay
vars (so lead notifications + license keys actually get delivered instead
of only logged), real `CORS_ORIGINS` / `PUBLIC_SITE_URL`, and a
`MEDIA_ROOT` on a persistent volume.

### Local dev

Run `stripe listen --forward-to localhost:8000/api/v1/stripe/webhook` and
use the printed `whsec_…` as `STRIPE_WEBHOOK_SECRET` — never point the dev
box at the production Stripe webhook.
