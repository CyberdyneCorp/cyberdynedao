"""Container wiring: which email notifier the provider selection yields
(issue #7)."""

from __future__ import annotations

import pytest

from cyberdyne_backend.adapters.outbound.email.notifiers import (
    LoggingEmailNotifier,
    LoggingLicenseEmailNotifier,
)
from cyberdyne_backend.adapters.outbound.email.smtp import (
    SmtpEmailNotifier,
    SmtpLicenseEmailNotifier,
)
from cyberdyne_backend.infrastructure.container import Container
from cyberdyne_backend.infrastructure.settings import Settings

pytestmark = pytest.mark.unit

_SMTP = {
    "email_provider": "smtp",
    "smtp_host": "smtp.test",
    "email_admin_recipient": "ops@cyberdynecorp.ai",
}


def test_default_is_logging() -> None:
    c = Container(Settings())
    assert isinstance(c.email_notifier, LoggingEmailNotifier)
    assert isinstance(c.license_email_notifier, LoggingLicenseEmailNotifier)


def test_smtp_selected_when_configured() -> None:
    c = Container(Settings(**_SMTP))
    assert isinstance(c.email_notifier, SmtpEmailNotifier)
    assert isinstance(c.license_email_notifier, SmtpLicenseEmailNotifier)


def test_ask_notifier_needs_recipient() -> None:
    # SMTP + host but no team inbox: license mail (buyer address) still goes
    # SMTP, ask notifications fall back to logging rather than silently drop.
    c = Container(Settings(email_provider="smtp", smtp_host="smtp.test"))
    assert isinstance(c.email_notifier, LoggingEmailNotifier)
    assert isinstance(c.license_email_notifier, SmtpLicenseEmailNotifier)


def test_smtp_requested_without_host_stays_logging() -> None:
    c = Container(Settings(email_provider="smtp", email_admin_recipient="ops@cyberdynecorp.ai"))
    assert isinstance(c.email_notifier, LoggingEmailNotifier)
    assert isinstance(c.license_email_notifier, LoggingLicenseEmailNotifier)
