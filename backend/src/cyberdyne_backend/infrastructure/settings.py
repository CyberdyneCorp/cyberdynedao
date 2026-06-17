"""Application settings (pydantic-settings).

Single source of truth — every adapter and use case reads from
``get_settings()``. Phase 1 covers DB + CyberdyneAuth; the rest of the
env-var inventory in docs/backend-roadmap.md §9 lands per-phase.
"""

from __future__ import annotations

import logging
from functools import lru_cache
from typing import Literal

from pydantic import Field, SecretStr, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

Environment = Literal["local", "ci", "staging", "production"]


class InsecureProductionConfigError(RuntimeError):
    """Raised when a staging/production process is configured with the
    dev-default mock adapters that must never run in a shared environment."""


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # ── Runtime ───────────────────────────────────────────────────────
    environment: Environment = "local"
    log_level: str = Field("INFO", description="Root log level — DEBUG / INFO / WARNING / ERROR")
    port: int = 8000

    # When true, app startup HARD-FAILS in staging/production if any
    # dev-default mock adapter is still active (see ``mock_adapter_problems``).
    # Default false: the app still boots and only logs warnings, so a
    # partially-provisioned environment (e.g. real DB but the DAO multisig /
    # Stripe / OpenAI not wired yet) isn't blocked. Flip this on once every
    # production adapter is configured. See issue #7's Operational guardrails.
    enforce_production_adapters: bool = False

    # Comma-separated list of allowed origins for browser fetches.
    # Locally defaults to the SvelteKit dev server. In prod set to the
    # frontend FQDN(s) — e.g. ``https://cyberdyne.coolify.cyberdynecorp.ai``.
    cors_origins: str = "http://localhost:5173"

    # Public URL the frontend is served from. Used by the RSS feed to
    # build absolute post URLs. Should match the primary CORS origin
    # in prod.
    public_site_url: str = "http://localhost:5173"

    @property
    def cors_origin_list(self) -> list[str]:
        return [o.strip() for o in self.cors_origins.split(",") if o.strip()]

    # ── Database ──────────────────────────────────────────────────────
    # Default points at the compose.dev.yaml Postgres on the non-standard
    # 5433 port (avoids collision with other local sidecars). In prod
    # Coolify injects the sidecar DSN; in CI the env var points at the
    # `services: postgres:` container.
    database_url: str = Field(
        "postgresql+asyncpg://cyberdyne:cyberdyne@localhost:5433/cyberdyne",
        description="Async SQLAlchemy DSN. Override in prod to point at the Coolify Postgres sidecar.",
    )
    database_echo: bool = False
    database_pool_size: int = 10
    database_max_overflow: int = 20

    # ── CyberdyneAuth ─────────────────────────────────────────────────
    cyberdyne_auth_base_url: str = Field(
        "https://auth.backend.coolify.cyberdynecorp.ai",
        description="Upstream CyberdyneAuth root. Override locally to a mock.",
    )
    cyberdyne_auth_introspection_ttl_s: int = 30
    cyberdyne_auth_profile_ttl_s: int = 60
    cyberdyne_auth_request_timeout_s: float = 5.0

    # Client-credentials for this backend's own outbound calls.
    # Optional in v1 because Phase 1 endpoints are public reads; future
    # phases (chat agent calling CyberRAG, NFT-tier lookups) require them.
    cyberdyne_auth_client_id: str | None = None
    cyberdyne_auth_client_secret: SecretStr | None = None
    cyberdyne_auth_oauth_scopes: str = ""
    cyberdyne_auth_oauth_audience: str | None = None

    # ── Captcha (Phase 2 — Contact form) ──────────────────────────────
    # "mock" = always-pass (safe for dev / tests). "turnstile" = real
    # Cloudflare siteverify; requires captcha_secret.
    captcha_provider: Literal["mock", "turnstile"] = "mock"
    captcha_secret: SecretStr | None = None

    # ── Certificates (Phase 4 — Learning platform) ────────────────────
    # HMAC-SHA256 shared secret used to sign learning certificates.
    # If unset the EphemeralCertificateSigner kicks in — fine for local
    # dev, loud in staging/prod via a startup warning.
    cert_signing_key: SecretStr | None = None

    # ── DAO treasury / Web3 (Phase 5) ─────────────────────────────────
    # ``fake`` ships deterministic data and is the default until a real
    # DAO multisig is registered. ``web3py`` activates the real RPC
    # reader (scaffolded; lands in a follow-up PR).
    chain_reader_provider: Literal["fake", "web3py"] = "fake"

    # The DAO multisig address on Base. The frontend never sees it
    # except through the /dao endpoints — keep it server-side so we can
    # rotate without a redeploy of the frontend.
    dao_treasury_address: str | None = None

    # Base mainnet RPC. Required when chain_reader_provider == "web3py".
    base_rpc_url: str | None = None

    # AAVE v3 + Uniswap v4 contract addresses on Base. Defaults pulled
    # from the canonical deployments (see docs/backend-roadmap.md §5.2).
    aave_pool_data_provider: str = "0x2A0979257105834789bC6b9E1B00446DFbA8dFBa"
    uniswap_v4_position_manager: str = "0x7C5f5A4bBd8fD63184577525326123B519429bDc"

    # CyberdyneAccessNFT contract on Base — backs the wallet access-tier
    # lookup (and the chat agent's get_user_tier tool). Mirrors the
    # frontend's VITE_CYBERDYNE_ACCESS_NFT_ADDRESS. Unset → the stub reader
    # reports "no access NFT" for every address; the real web3py reader
    # lands with BASE_RPC_URL + this address.
    cyberdyne_access_nft_address: str | None = None

    # Cache TTL for chain snapshots. Default 5 minutes; tune up for
    # rate-limited RPCs.
    dao_snapshot_ttl_s: int = 300

    # Optional: number of token holders, surfaced in /dao/overview.
    # Filled in by the governance subgraph once it ships; defaults to 0.
    dao_holders_count: int = 0

    # ── Marketplace / Stripe (Phase 6) ────────────────────────────────
    # Both unset = MockStripeCheckoutClient + MockStripeWebhookVerifier
    # (local-dev only). Settings hard-refuses to start with mocks in
    # staging/production via ``model_post_init``.
    stripe_secret_key: SecretStr | None = None
    stripe_webhook_secret: SecretStr | None = None
    # URLs Stripe redirects to after Checkout.
    stripe_success_url: str = "http://localhost:5173/marketplace?session={CHECKOUT_SESSION_ID}"
    stripe_cancel_url: str = "http://localhost:5173/marketplace?cancelled=1"

    # ── AI chat (Phase 6) ─────────────────────────────────────────────
    # Unset = StaticChatClient mock — local dev only.
    openai_api_key: SecretStr | None = None
    openai_model: str = "gpt-4o-mini"
    # CyberRAG MCP URL — stub fallback runs when unset. Real client is a
    # follow-up adapter (see docs/backend-roadmap.md §5.6).
    cyberrag_mcp_url: str | None = None

    # MATLAB-LLVM backend the chat agent's matlab_repl / matlab_plot
    # tools call (as the signed-in user). Same upstream the frontend's
    # matlabApi.ts proxies to.
    matlab_backend_url: str = "https://matlab-backend.coolify.cyberdynecorp.ai"

    # Python interpreter backend the chat agent's python_exec tool calls
    # (as the signed-in user). Same upstream the frontend's
    # interpreterApi.ts proxies to.
    python_interpreter_url: str = "https://interpreter.backend.coolify.cyberdynecorp.ai"

    # Cyberflies (meetings) backend the chat agent's ask_meetings /
    # list_meetings tools call (as the signed-in user).
    cyberflies_url: str = "https://cyberflies.backend.coolify.cyberdynecorp.ai"

    # ── Uploads / media (Phase 8 — course content) ────────────────────
    # Where uploaded course/lesson media is written. In prod point this
    # at the Coolify persistent volume mount; locally it defaults to a
    # gitignored ./uploads dir. Served read-only under ``media_url_prefix``.
    media_root: str = "./uploads"
    media_url_prefix: str = "/media"

    @field_validator("log_level")
    @classmethod
    def _upper_log_level(cls, value: str) -> str:
        return value.upper()

    def mock_adapter_problems(self) -> list[str]:
        """Dev-default mock adapters that should not run in a shared
        environment. Empty outside staging/production, so this is a pure,
        side-effect-free check (does NOT run on settings construction — it
        must not break ``alembic upgrade`` or other tooling that only needs
        the DB URL)."""
        if self.environment not in ("staging", "production"):
            return []

        problems: list[str] = []
        if self.chain_reader_provider == "fake":
            problems.append(
                "chain_reader_provider=fake (set CHAIN_READER_PROVIDER=web3py + BASE_RPC_URL)"
            )
        if self.captcha_provider == "mock":
            problems.append(
                "captcha_provider=mock (set CAPTCHA_PROVIDER=turnstile + CAPTCHA_SECRET)"
            )
        if self.stripe_secret_key is None:
            problems.append("STRIPE_SECRET_KEY is unset (MockStripeCheckoutClient)")
        if self.stripe_webhook_secret is None:
            problems.append(
                "STRIPE_WEBHOOK_SECRET is unset (MockStripeWebhookVerifier trusts every payload)"
            )
        if self.openai_api_key is None:
            problems.append("OPENAI_API_KEY is unset (StaticChatClient offline mode)")
        return problems

    def check_production_adapters(self, log: logging.Logger) -> None:
        """Gate app serving (call from the app factory, NOT from settings
        construction). Logs a warning per active mock adapter; raises
        ``InsecureProductionConfigError`` only when
        ``enforce_production_adapters`` is set, so a partially-provisioned
        environment still boots while a fully-provisioned one can be locked
        down. See issue #7's Operational guardrails."""
        problems = self.mock_adapter_problems()
        if not problems:
            return
        joined = "\n  - ".join(problems)
        if self.enforce_production_adapters:
            raise InsecureProductionConfigError(
                f"refusing to start in {self.environment!r} with dev-default "
                f"mock adapters active:\n  - {joined}"
            )
        log.warning(
            "running in %r with dev-default mock adapters active (set "
            "ENFORCE_PRODUCTION_ADAPTERS=true to hard-fail once provisioned):"
            "\n  - %s",
            self.environment,
            joined,
        )


@lru_cache
def get_settings() -> Settings:
    return Settings()


def reset_settings_cache() -> None:
    """Tests use this to apply env-var overrides between cases."""
    get_settings.cache_clear()
