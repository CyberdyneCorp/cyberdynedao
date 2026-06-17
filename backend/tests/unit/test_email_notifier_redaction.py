"""The logging email notifiers redact PII (issue #7)."""

from __future__ import annotations

import logging

import pytest

from cyberdyne_backend.adapters.outbound.email.notifiers import (
    LoggingEmailNotifier,
    LoggingLicenseEmailNotifier,
)
from cyberdyne_backend.domain.leads import AskChannel, new_ask


async def test_new_ask_notification_masks_email(caplog: pytest.LogCaptureFixture) -> None:
    ask = new_ask(
        channel=AskChannel.CONTACT_FORM,
        name="Alice Example",
        email="alice@example.com",
        body="please call me",
    )
    with caplog.at_level(logging.INFO, logger="cyberdyne_backend.email"):
        await LoggingEmailNotifier().send_new_ask_notification(ask)
    assert "alice@example.com" not in caplog.text
    assert "a***@example.com" in caplog.text


async def test_license_email_masks_recipient_but_keeps_key(
    caplog: pytest.LogCaptureFixture,
) -> None:
    with caplog.at_level(logging.INFO, logger="cyberdyne_backend.email"):
        await LoggingLicenseEmailNotifier().send_license_email(
            to_email="buyer@corp.com",
            product_title="Blockchain Dev",
            plaintext_key="ABCDE-FGHIJ-KLMNO-PQRST-UVWXY",
            expires_at_iso="2027-01-01T00:00:00Z",
        )
    assert "buyer@corp.com" not in caplog.text
    assert "b***@corp.com" in caplog.text
    # The key is the deliverable in the no-SMTP fallback — must stay intact.
    assert "ABCDE-FGHIJ-KLMNO-PQRST-UVWXY" in caplog.text
