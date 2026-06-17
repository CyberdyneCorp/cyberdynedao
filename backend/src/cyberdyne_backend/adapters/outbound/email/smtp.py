"""SMTP-backed email adapters implementing the notifier ports.

The Phase-2 default is the logging notifiers in ``notifiers.py``; this
module is the real "one-class swap" (issue #7): when ``EMAIL_PROVIDER=smtp``
and an SMTP host is configured, new-ask notifications go to the team inbox
and license keys are emailed to the buyer.

It deliberately uses the stdlib ``smtplib`` (no new dependency). The
blocking send runs in a worker thread via ``asyncio.to_thread`` so it never
stalls the event loop. Works against any SMTP relay — Postmark, SES,
Mailgun, Gmail — since they all speak SMTP. The actual network send is
injected as ``transport`` so unit tests exercise message construction and
the never-raise contract without opening a socket.
"""

from __future__ import annotations

import asyncio
import logging
import smtplib
from collections.abc import Callable
from dataclasses import dataclass
from email.message import EmailMessage

from cyberdyne_backend.domain.leads import Ask
from cyberdyne_backend.infrastructure.redaction import redact_email

logger = logging.getLogger("cyberdyne_backend.email")


@dataclass(frozen=True, slots=True)
class SmtpSettings:
    """Connection settings for the SMTP relay. Built by the container from
    the app ``Settings`` — kept as a plain adapter-local dataclass so this
    module doesn't depend on the settings object."""

    host: str
    port: int
    from_addr: str
    username: str | None = None
    password: str | None = None
    use_tls: bool = True


def _send_via_smtplib(settings: SmtpSettings, message: EmailMessage) -> None:
    """Blocking SMTP send — opens a connection, optionally upgrades to TLS
    and authenticates, then delivers one message. Run off-loop via
    ``asyncio.to_thread``."""
    with smtplib.SMTP(settings.host, settings.port, timeout=10.0) as client:
        if settings.use_tls:
            client.starttls()
        if settings.username and settings.password:
            client.login(settings.username, settings.password)
        client.send_message(message)


# The network send is injectable so tests can capture messages without a
# real SMTP server. Defaults to the stdlib path above.
SmtpTransport = Callable[[SmtpSettings, EmailMessage], None]


class SmtpMailer:
    """Low-level mailer: builds an ``EmailMessage`` and delegates the
    blocking send to ``transport`` on a worker thread."""

    def __init__(self, settings: SmtpSettings, *, transport: SmtpTransport = _send_via_smtplib):
        self._settings = settings
        self._transport = transport

    async def send(self, *, to: str, subject: str, body: str) -> None:
        message = EmailMessage()
        message["From"] = self._settings.from_addr
        message["To"] = to
        message["Subject"] = subject
        message.set_content(body)
        await asyncio.to_thread(self._transport, self._settings, message)


class SmtpEmailNotifier:
    """Emails the team inbox on every new ask. Honors the port contract:
    a delivery failure is logged (recipient PII masked) but never raised, so
    it can't block ask creation."""

    def __init__(self, mailer: SmtpMailer, *, recipient: str) -> None:
        self._mailer = mailer
        self._recipient = recipient

    async def send_new_ask_notification(self, ask: Ask) -> None:
        subject = f"New {ask.channel.value} ask from {ask.name}"
        body = (
            f"A new ask was submitted.\n\n"
            f"Channel:  {ask.channel.value}\n"
            f"Name:     {ask.name}\n"
            f"Email:    {ask.email}\n"
            f"Product:  {ask.product_slug or '-'}\n"
            f"Source:   {ask.source_url or '-'}\n"
            f"Ask id:   {ask.id}\n\n"
            f"{ask.body}\n"
        )
        try:
            await self._mailer.send(to=self._recipient, subject=subject, body=body)
        except Exception:
            logger.warning("failed to email new-ask notification | id=%s", ask.id, exc_info=True)


class SmtpLicenseEmailNotifier:
    """Emails a purchased license key to the buyer. Like the ask notifier it
    swallows delivery failures so a transient SMTP error can't fail the
    order; the key is still persisted/recoverable server-side."""

    def __init__(self, mailer: SmtpMailer) -> None:
        self._mailer = mailer

    async def send_license_email(
        self,
        *,
        to_email: str,
        product_title: str,
        plaintext_key: str,
        expires_at_iso: str | None,
    ) -> None:
        expiry_line = f"Expires: {expires_at_iso}\n" if expires_at_iso else ""
        subject = f"Your {product_title} license key"
        body = (
            f"Thank you for your purchase of {product_title}.\n\n"
            f"License key: {plaintext_key}\n"
            f"{expiry_line}\n"
            f"Keep this key safe — it unlocks your access.\n"
        )
        try:
            await self._mailer.send(to=to_email, subject=subject, body=body)
        except Exception:
            logger.warning(
                "failed to email license key | to=%s product=%r",
                redact_email(to_email),
                product_title,
                exc_info=True,
            )


__all__ = [
    "SmtpEmailNotifier",
    "SmtpLicenseEmailNotifier",
    "SmtpMailer",
    "SmtpSettings",
    "SmtpTransport",
]
