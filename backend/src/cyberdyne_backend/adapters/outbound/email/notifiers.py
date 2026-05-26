"""Email notifier adapters implementing ``EmailNotifierPort``.

Phase 2 ships one default: ``LoggingEmailNotifier`` — emits structured
log lines for every new ask. This is the safe default; real SMTP /
Postmark / Mailgun / etc. lands in a follow-up adapter when an account
is provisioned. The use case only cares about the port shape.
"""

from __future__ import annotations

import contextlib
import logging

from cyberdyne_backend.domain.leads import Ask

logger = logging.getLogger("cyberdyne_backend.email")


class LoggingEmailNotifier:
    """Logs new asks; never raises (port contract)."""

    async def send_new_ask_notification(self, ask: Ask) -> None:
        # Even logging shouldn't blow up the request path.
        with contextlib.suppress(Exception):
            logger.info(
                "new ask received | id=%s channel=%s from=%s product=%s",
                ask.id,
                ask.channel.value,
                ask.email,
                ask.product_slug,
            )


class LoggingLicenseEmailNotifier:
    """Logs license-key delivery instead of emailing. Default when no SMTP
    provider is configured. The plaintext key is logged because it's
    already going to land in our own server log either way — the
    persistence layer never stores it."""

    async def send_license_email(
        self,
        *,
        to_email: str,
        product_title: str,
        plaintext_key: str,
        expires_at_iso: str | None,
    ) -> None:
        with contextlib.suppress(Exception):
            logger.info(
                "license issued | to=%s product=%r key=%s expires=%s",
                to_email,
                product_title,
                plaintext_key,
                expires_at_iso,
            )
