"""Leads bounded context.

Handles inbound "asks" from the website — Contact-form submissions,
service-inquiry follow-ups from the marketplace, and chat-agent
handoffs. Asks are persisted with a small CRM-style state machine
(``new`` → ``triaged`` → ``in_progress`` → ``closed``) and audit
events so anyone with the editor scope can see who did what when.
"""

from cyberdyne_backend.domain.leads.entities import (
    Ask,
    AskChannel,
    AskEvent,
    AskEventKind,
    AskStatus,
    new_ask,
)
from cyberdyne_backend.domain.leads.errors import (
    AskNotFoundError,
    AskTransitionError,
)
from cyberdyne_backend.domain.leads.ports import (
    AskRepository,
    CaptchaPort,
    CaptchaVerificationError,
    EmailNotifierPort,
)

__all__ = [
    "Ask",
    "AskChannel",
    "AskEvent",
    "AskEventKind",
    "AskNotFoundError",
    "AskRepository",
    "AskStatus",
    "AskTransitionError",
    "CaptchaPort",
    "CaptchaVerificationError",
    "EmailNotifierPort",
    "new_ask",
]
