# Coolify deploy — docker-compose

`docker-compose.yml` at the repo root is the single source of truth for production. It bundles `postgres`, `backend`, and `frontend` into one Coolify application so Traefik routing, network attachment, and TLS issuance all happen against a known-good topology.

The rules below are lifted from
`leo-obsidian-vault/Infrastructure/Coolify/Coolify Tricks and Traps.md` and
`Coolify Docker Compose Deployments.md` — every one is from a real incident.

## 1 · Create the application in Coolify

- **Type:** Docker Compose (Public Repository)
- **Repository:** `https://github.com/CyberdyneCorp/cyberdynedao`
- **Branch:** `main`
- **Docker Compose file location:** `docker-compose.yml`

Do **not** create separate Coolify apps for the frontend and backend — they live in one compose stack.

## 2 · Domains (per service)

In the application → **General → Domains** section, set FQDNs **with the internal container port** suffixed. Coolify uses the port to generate the `traefik.http.services.<svc>.loadbalancer.server.port` label; without it Traefik returns `503 no available server`.

```
SERVICE_FQDN_BACKEND   = https://api.cyberdyne.coolify.cyberdynecorp.ai:8000
SERVICE_FQDN_FRONTEND  = https://cyberdyne.coolify.cyberdynecorp.ai:80
```

`postgres` gets **no** domain — internal only.

## 3 · Environment variables

Set these in **Application → Environment Variables**. The compose references each with `${…}` and Coolify substitutes them at deploy time.

### Runtime — required

| Key | Notes |
| --- | --- |
| `POSTGRES_USER` / `POSTGRES_PASSWORD` / `POSTGRES_DB` | Database credentials. Defaults to `cyberdyne` if unset. |
| `ENVIRONMENT` | `production` |
| `LOG_LEVEL` | `INFO` |
| `CORS_ORIGINS` | Comma-separated; must include the frontend FQDN |
| `PUBLIC_SITE_URL` | Frontend FQDN — used by the RSS feed |

### CyberdyneAuth (Phase 1+)

| Key | Notes |
| --- | --- |
| `CYBERDYNE_AUTH_BASE_URL` | Defaults to `https://auth.backend.coolify.cyberdynecorp.ai` |
| `CYBERDYNE_AUTH_CLIENT_ID` | OAuth client for outbound calls (Phase 6 chat → CyberRAG) |
| `CYBERDYNE_AUTH_CLIENT_SECRET` | Toggle **Is secret?** on. |
| `CYBERDYNE_AUTH_OAUTH_SCOPES` | e.g. `cyberrag:query iam:read.tier` |
| `CYBERDYNE_AUTH_OAUTH_AUDIENCE` | e.g. `https://cyberrag.coolify.cyberdynecorp.ai` |

### Captcha (Phase 2 — Contact form)

| Key | Notes |
| --- | --- |
| `CAPTCHA_PROVIDER` | `turnstile` in prod; default `mock` only for dev |
| `CAPTCHA_SECRET` | Cloudflare Turnstile siteverify secret. **Is secret?** on. |

### Learning certificates (Phase 4)

| Key | Notes |
| --- | --- |
| `CERT_SIGNING_KEY` | HMAC-SHA256 shared secret. **Is secret?** on. Required in prod; without it, certificates use an ephemeral key that resets on every container restart. |

### DAO treasury / Web3 (Phase 5)

| Key | Notes |
| --- | --- |
| `CHAIN_READER_PROVIDER` | `web3py` once `BASE_RPC_URL` + `DAO_TREASURY_ADDRESS` are set. Default `fake`. |
| `DAO_TREASURY_ADDRESS` | The DAO multisig on Base. Until set, `/api/v1/dao/overview` 503s. |
| `BASE_RPC_URL` | Base mainnet RPC. Required when provider is `web3py`. |
| `DAO_SNAPSHOT_TTL_S` | Default `300`. |

### Marketplace / Stripe (Phase 6)

| Key | Notes |
| --- | --- |
| `STRIPE_SECRET_KEY` | **Is secret?** on. Without it, the Mock checkout client runs. |
| `STRIPE_WEBHOOK_SECRET` | **Is secret?** on. Without it, the Mock verifier trusts every payload. |
| `STRIPE_SUCCESS_URL` / `STRIPE_CANCEL_URL` | Frontend URLs. |

### AI chat (Phase 6)

| Key | Notes |
| --- | --- |
| `OPENAI_API_KEY` | **Is secret?** on. Without it, every chat call returns the offline-mode reply. |
| `OPENAI_MODEL` | Default `gpt-4o-mini`. |
| `CYBERRAG_MCP_URL` | Optional. CyberRAG MCP endpoint; stub runs when unset. |

### Frontend (build-time, Vite)

`VITE_*` vars are baked into the bundle at `npm run build` time. Each one **must** have **Is build variable?** toggled on in Coolify — otherwise the value is empty in the built JS even though it's set at runtime.

| Key | Required | Notes |
| --- | --- | --- |
| `NPM_TOKEN` | yes | GitHub Packages auth for `@cyberdynecorp/*`. **Is build variable?** and **Is secret?** on. |
| `VITE_BACKEND_API_URL` | yes | Backend FQDN (without the `:8000` port suffix Coolify needs in the FQDN field — this one is the public URL Vite emits to fetch calls). |
| `VITE_INFURA_ENDPOINT` | yes | RPC URL for the Base network. |
| `VITE_CHAIN_ID` | yes | `8453` (Base mainnet). |
| `VITE_NETWORK_NAME` | yes | `Base`. |
| `VITE_NATIVE_CURRENCY` | yes | `ETH`. |
| `VITE_APP_NAME` | yes | `Cyberdyne`. |
| `VITE_REOWN_PROJECT_ID` | yes | WalletConnect project id. |
| `VITE_REOWN_APP_NAME` | yes | |
| `VITE_REOWN_APP_DESCRIPTION` | yes | |
| `VITE_REOWN_APP_URL` | yes | |
| `VITE_REOWN_APP_ICON` | yes | |
| `VITE_WEB3AUTH_CLIENT_ID` | yes | |
| `VITE_WEB3AUTH_NETWORK` | yes | `sapphire_mainnet` in prod. |
| `VITE_CYBERDYNE_ACCESS_NFT_ADDRESS` | yes | Contract address on Base. |

## 4 · Sanity checks after deploy

From your laptop:

```bash
# Each should be 200 (or 503 if Traefik isn't routing — see below).
curl -sSI https://api.cyberdyne.coolify.cyberdynecorp.ai/healthz
curl -sSI https://cyberdyne.coolify.cyberdynecorp.ai/

# OpenAPI surface should list /api/v1/* routes.
curl -s https://api.cyberdyne.coolify.cyberdynecorp.ai/openapi.json \
  | python -c "import json,sys; print('\n'.join(sorted(json.load(sys.stdin)['paths'])))"
```

## 5 · 503 "no available server" — the playbook

This is the single most common Coolify failure mode and almost always one of:

1. **`SERVICE_FQDN_*` is missing the port suffix.** Add `:8000` / `:80`.
2. **Custom Traefik labels** snuck into `docker-compose.yml`. Remove them; let Coolify generate.
3. **Custom `networks:` block** in `docker-compose.yml`. Remove it; Coolify attaches its own bridge.
4. **`ports:` instead of `expose:`** in a service. Switch to `expose`.
5. **Healthcheck failing.** Traefik silently drops unhealthy containers. SSH to the host and run `docker ps` — look for `(unhealthy)`. If yes, check the container's HEALTHCHECK command works inside the container (probably uses `localhost` or HEAD — switch to `127.0.0.1` GET).
6. **`container_name` set.** Coolify prefixes names; conflict kills rolling deploys.

## 6 · Restart the Coolify proxy

If everything looks right but Traefik still serves the default cert + 503s, force a reload from **Servers → [host] → Proxy → Restart**. This re-scans labels.
