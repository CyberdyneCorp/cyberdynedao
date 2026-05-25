"""Application settings (pydantic-settings).

Single source of truth — every adapter and use case reads from
``get_settings()``. Phase 1 keeps the surface small; the roadmap doc §9
lists every env var we'll grow into.
"""

from __future__ import annotations

from functools import lru_cache
from typing import Literal

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

Environment = Literal["local", "ci", "staging", "production"]


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    environment: Environment = "local"
    log_level: str = Field("INFO", description="Root log level — DEBUG / INFO / WARNING / ERROR")
    port: int = 8000


@lru_cache
def get_settings() -> Settings:
    return Settings()
