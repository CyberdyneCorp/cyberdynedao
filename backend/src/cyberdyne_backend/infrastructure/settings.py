"""Application settings (pydantic-settings).

Single source of truth — every adapter and use case reads from
``get_settings()``. Phase 1 covers DB + CyberdyneAuth; the rest of the
env-var inventory in docs/backend-roadmap.md §9 lands per-phase.
"""

from __future__ import annotations

from functools import lru_cache
from typing import Literal

from pydantic import Field, SecretStr, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

Environment = Literal["local", "ci", "staging", "production"]


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

    @field_validator("log_level")
    @classmethod
    def _upper_log_level(cls, value: str) -> str:
        return value.upper()


@lru_cache
def get_settings() -> Settings:
    return Settings()


def reset_settings_cache() -> None:
    """Tests use this to apply env-var overrides between cases."""
    get_settings.cache_clear()
