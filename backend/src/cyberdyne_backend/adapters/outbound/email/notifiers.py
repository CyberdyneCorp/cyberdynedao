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
