"""Ask domain entities and the state machine for status transitions."""

from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from datetime import UTC, datetime
from enum import StrEnum
from typing import Any
from uuid import UUID

from cyberdyne_backend.domain.leads.errors import AskTransitionError


class AskChannel(StrEnum):
    CONTACT_FORM = "contact_form"
    MARKETPLACE_SERVICE_INQUIRY = "marketplace_service_inquiry"
    CHAT_AGENT_HANDOFF = "chat_agent_handoff"


class AskStatus(StrEnum):
    NEW = "new"
    TRIAGED = "triaged"
    IN_PROGRESS = "in_progress"
    CLOSED = "closed"


class AskEventKind(StrEnum):
    CREATED = "created"
    STATUS_CHANGED = "status_changed"
    NOTE_ADDED = "note_added"
    OWNER_ASSIGNED = "owner_assigned"


# Allowed transitions per the state machine. Closed asks can only be
# reopened back to ``in_progress`` (and only by adding a note — the
# router enforces the note requirement; the domain just allows the
# transition).
_ALLOWED_TRANSITIONS: dict[AskStatus, frozenset[AskStatus]] = {
    AskStatus.NEW: frozenset({AskStatus.TRIAGED, AskStatus.IN_PROGRESS, AskStatus.CLOSED}),
    AskStatus.TRIAGED: frozenset({AskStatus.IN_PROGRESS, AskStatus.CLOSED}),
    AskStatus.IN_PROGRESS: frozenset({AskStatus.CLOSED, AskStatus.TRIAGED}),
    AskStatus.CLOSED: frozenset({AskStatus.IN_PROGRESS}),
}


@dataclass(frozen=True, slots=True)
class AskEvent:
    id: UUID
    ask_id: UUID
    kind: AskEventKind
    by_user_id: UUID | None
    payload: dict[str, Any]
    at: datetime


@dataclass(slots=True)
class Ask:
    id: UUID
    channel: AskChannel
    name: str
    email: str
    body: str
    product_slug: str | None
    source_url: str | None
    status: AskStatus
    owner_user_id: UUID | None
    notes_md: str
    created_at: datetime
    events: list[AskEvent] = field(default_factory=list)

    def can_transition_to(self, target: AskStatus) -> bool:
        return target in _ALLOWED_TRANSITIONS[self.status]

    def transition_to(
        self,
        target: AskStatus,
        by_user_id: UUID | None,
        now: datetime | None = None,
    ) -> AskEvent:
        """Emit a STATUS_CHANGED event after validating the transition."""
        if target == self.status:
            raise AskTransitionError(f"already {self.status}")
        if not self.can_transition_to(target):
            raise AskTransitionError(f"cannot transition {self.status} -> {target}")
        evt = AskEvent(
            id=uuid.uuid4(),
            ask_id=self.id,
            kind=AskEventKind.STATUS_CHANGED,
            by_user_id=by_user_id,
            payload={"from": self.status.value, "to": target.value},
            at=now or datetime.now(tz=UTC),
        )
        self.status = target
        self.events.append(evt)
        return evt

    def add_note(
        self,
        text: str,
        by_user_id: UUID | None,
        now: datetime | None = None,
    ) -> AskEvent:
        cleaned = text.strip()
        if not cleaned:
            raise AskTransitionError("note text cannot be empty")
        if self.notes_md:
            self.notes_md = f"{self.notes_md.rstrip()}\n\n---\n\n{cleaned}"
        else:
            self.notes_md = cleaned
        evt = AskEvent(
            id=uuid.uuid4(),
            ask_id=self.id,
            kind=AskEventKind.NOTE_ADDED,
            by_user_id=by_user_id,
            payload={"text": cleaned},
            at=now or datetime.now(tz=UTC),
        )
        self.events.append(evt)
        return evt

    def assign_owner(
        self,
        owner_user_id: UUID,
        by_user_id: UUID | None,
        now: datetime | None = None,
    ) -> AskEvent:
        self.owner_user_id = owner_user_id
        evt = AskEvent(
            id=uuid.uuid4(),
            ask_id=self.id,
            kind=AskEventKind.OWNER_ASSIGNED,
            by_user_id=by_user_id,
            payload={"owner_user_id": str(owner_user_id)},
            at=now or datetime.now(tz=UTC),
        )
        self.events.append(evt)
        return evt


def new_ask(
    *,
    channel: AskChannel,
    name: str,
    email: str,
    body: str,
    product_slug: str | None = None,
    source_url: str | None = None,
    now: datetime | None = None,
) -> Ask:
    """Factory for a fresh Ask in ``new`` state with a CREATED event."""
    created_at = now or datetime.now(tz=UTC)
    ask_id = uuid.uuid4()
    ask = Ask(
        id=ask_id,
        channel=channel,
        name=name.strip(),
        email=email.strip(),
        body=body.strip(),
        product_slug=product_slug,
        source_url=source_url,
        status=AskStatus.NEW,
        owner_user_id=None,
        notes_md="",
        created_at=created_at,
        events=[],
    )
    ask.events.append(
        AskEvent(
            id=uuid.uuid4(),
            ask_id=ask_id,
            kind=AskEventKind.CREATED,
            by_user_id=None,
            payload={"channel": channel.value, "source_url": source_url},
            at=created_at,
        )
    )
    return ask
