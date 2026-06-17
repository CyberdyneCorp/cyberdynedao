"""Unit tests for the SMTP email adapters (issue #7).

The network send is injected, so these exercise message construction and
the never-raise port contract without opening a socket.
"""

from __future__ import annotations

import uuid
from datetime import UTC, datetime
from email.message import EmailMessage

import pytest

from cyberdyne_backend.adapters.outbound.email.smtp import (
    SmtpEmailNotifier,
    SmtpLicenseEmailNotifier,
    SmtpMailer,
    SmtpSettings,
)
from cyberdyne_backend.domain.leads import Ask, AskChannel, AskStatus

pytestmark = pytest.mark.unit

_SETTINGS = SmtpSettings(host="smtp.test", port=587, from_addr="no-reply@cyberdynecorp.ai")


def _capturing_mailer() -> tuple[SmtpMailer, list[EmailMessage]]:
    sent: list[EmailMessage] = []

    def transport(_settings: SmtpSettings, message: EmailMessage) -> None:
        sent.append(message)

    return SmtpMailer(_SETTINGS, transport=transport), sent


def _exploding_mailer() -> SmtpMailer:
    def transport(_settings: SmtpSettings, _message: EmailMessage) -> None:
        raise OSError("connection refused")

    return SmtpMailer(_SETTINGS, transport=transport)


def _ask(email: str = "lead@example.com") -> Ask:
    return Ask(
        id=uuid.uuid4(),
        channel=AskChannel.CONTACT_FORM,
        name="Ada Lovelace",
        email=email,
        body="I'd like to talk about a project.",
        product_slug="consulting",
        source_url="https://cyberdynecorp.ai/contact",
        status=AskStatus.NEW,
        owner_user_id=None,
        notes_md="",
        created_at=datetime(2026, 6, 17, tzinfo=UTC),
    )


class TestSmtpMailer:
    async def test_builds_message_envelope(self) -> None:
        mailer, sent = _capturing_mailer()
        await mailer.send(to="ops@cyberdynecorp.ai", subject="Hi", body="Body text")
        assert len(sent) == 1
        msg = sent[0]
        assert msg["From"] == "no-reply@cyberdynecorp.ai"
        assert msg["To"] == "ops@cyberdynecorp.ai"
        assert msg["Subject"] == "Hi"
        assert msg.get_content().strip() == "Body text"


class TestSmtpEmailNotifier:
    async def test_emails_admin_with_ask_details(self) -> None:
        mailer, sent = _capturing_mailer()
        notifier = SmtpEmailNotifier(mailer, recipient="ops@cyberdynecorp.ai")
        ask = _ask()
        await notifier.send_new_ask_notification(ask)
        assert len(sent) == 1
        msg = sent[0]
        assert msg["To"] == "ops@cyberdynecorp.ai"
        body = msg.get_content()
        assert "Ada Lovelace" in body
        assert "lead@example.com" in body
        assert str(ask.id) in body
        assert "I'd like to talk about a project." in body

    async def test_never_raises_on_send_failure(self) -> None:
        # Regression: the port contract says a delivery failure must not
        # block ask creation.
        notifier = SmtpEmailNotifier(_exploding_mailer(), recipient="ops@cyberdynecorp.ai")
        await notifier.send_new_ask_notification(_ask())  # must not raise


class TestSmtpLicenseEmailNotifier:
    async def test_emails_buyer_with_key_and_expiry(self) -> None:
        mailer, sent = _capturing_mailer()
        notifier = SmtpLicenseEmailNotifier(mailer)
        await notifier.send_license_email(
            to_email="buyer@example.com",
            product_title="MATLAB Mastery",
            plaintext_key="CYBR-1234-ABCD",
            expires_at_iso="2027-01-01T00:00:00Z",
        )
        assert len(sent) == 1
        msg = sent[0]
        assert msg["To"] == "buyer@example.com"
        assert "MATLAB Mastery" in msg["Subject"]
        body = msg.get_content()
        assert "CYBR-1234-ABCD" in body
        assert "2027-01-01T00:00:00Z" in body

    async def test_omits_expiry_line_when_none(self) -> None:
        mailer, sent = _capturing_mailer()
        notifier = SmtpLicenseEmailNotifier(mailer)
        await notifier.send_license_email(
            to_email="buyer@example.com",
            product_title="Perpetual License",
            plaintext_key="CYBR-PERP",
            expires_at_iso=None,
        )
        assert "Expires:" not in sent[0].get_content()

    async def test_never_raises_on_send_failure(self) -> None:
        notifier = SmtpLicenseEmailNotifier(_exploding_mailer())
        await notifier.send_license_email(
            to_email="buyer@example.com",
            product_title="X",
            plaintext_key="K",
            expires_at_iso=None,
        )  # must not raise
