"""Ports the leads context depends on.

Concrete adapters live in ``adapters/outbound``. Fakes live next to
the application use-case tests.
"""

from __future__ import annotations

from typing import Protocol, runtime_checkable
from uuid import UUID

from cyberdyne_backend.domain.leads.entities import Ask, AskStatus

# ── Persistence ──────────────────────────────────────────────────────


@runtime_checkable
class AskRepository(Protocol):
    async def save(self, ask: Ask) -> None:
        """Insert or update an Ask (and any new events on it)."""
        ...

    async def get(self, ask_id: UUID) -> Ask:
        """Load an Ask + its events. Raises ``AskNotFoundError``."""
        ...

    async def list_admin(
        self,
        *,
        status: AskStatus | None = None,
        channel: str | None = None,
        query: str | None = None,
        page: int = 1,
        page_size: int = 50,
    ) -> tuple[list[Ask], int]:
        """Paginated admin list. Returns (items, total_count)."""
        ...


# ── Captcha ──────────────────────────────────────────────────────────


class CaptchaVerificationError(Exception):
    """Captcha token is missing or rejected by the upstream provider."""


@runtime_checkable
class CaptchaPort(Protocol):
    async def verify(self, token: str, remote_ip: str | None) -> None:
        """Validate the captcha token. Raises ``CaptchaVerificationError`` on rejection."""
        ...


# ── Email notifications ──────────────────────────────────────────────


@runtime_checkable
class EmailNotifierPort(Protocol):
    async def send_new_ask_notification(self, ask: Ask) -> None:
        """Fire-and-forget notification on every new ask.

        The concrete adapter decides where it goes (SMTP, log, Slack
        webhook, …). Failures must not block ask creation — the adapter
        catches/logs internally and never raises.
        """
        ...
