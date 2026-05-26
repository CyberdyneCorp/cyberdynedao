"""Tests for the leads domain (state machine + new_ask factory)."""

from __future__ import annotations

from datetime import UTC, datetime
from uuid import uuid4

import pytest

from cyberdyne_backend.domain.leads import (
    Ask,
    AskChannel,
    AskEventKind,
    AskStatus,
    AskTransitionError,
    new_ask,
)


def _make_ask() -> Ask:
    return new_ask(
        channel=AskChannel.CONTACT_FORM,
        name="Alice",
        email="alice@example.com",
        body="Hi, I'd like to know more.",
        product_slug=None,
        source_url="https://cyberdyne.example/contact",
    )


# ── new_ask ──────────────────────────────────────────────────────────


class TestNewAsk:
    def test_starts_in_new_with_created_event(self) -> None:
        ask = _make_ask()
        assert ask.status is AskStatus.NEW
        assert ask.notes_md == ""
        assert ask.owner_user_id is None
        assert ask.channel is AskChannel.CONTACT_FORM
        assert len(ask.events) == 1
        evt = ask.events[0]
        assert evt.kind is AskEventKind.CREATED
        assert evt.ask_id == ask.id
        assert evt.payload["channel"] == "contact_form"

    def test_strips_whitespace(self) -> None:
        ask = new_ask(
            channel=AskChannel.CONTACT_FORM,
            name="  Alice  ",
            email="  alice@example.com  ",
            body="  Hi  ",
        )
        assert ask.name == "Alice"
        assert ask.email == "alice@example.com"
        assert ask.body == "Hi"


# ── State machine ────────────────────────────────────────────────────


class TestTransitions:
    def test_new_to_triaged_allowed(self) -> None:
        ask = _make_ask()
        ask.transition_to(AskStatus.TRIAGED, by_user_id=uuid4())
        assert ask.status is AskStatus.TRIAGED
        assert ask.events[-1].kind is AskEventKind.STATUS_CHANGED
        assert ask.events[-1].payload == {"from": "new", "to": "triaged"}

    def test_new_to_closed_allowed(self) -> None:
        ask = _make_ask()
        ask.transition_to(AskStatus.CLOSED, by_user_id=uuid4())
        assert ask.status is AskStatus.CLOSED

    def test_closed_to_in_progress_allowed(self) -> None:
        ask = _make_ask()
        ask.transition_to(AskStatus.CLOSED, by_user_id=uuid4())
        ask.transition_to(AskStatus.IN_PROGRESS, by_user_id=uuid4())
        assert ask.status is AskStatus.IN_PROGRESS

    def test_closed_to_new_forbidden(self) -> None:
        ask = _make_ask()
        ask.transition_to(AskStatus.CLOSED, by_user_id=uuid4())
        with pytest.raises(AskTransitionError):
            ask.transition_to(AskStatus.NEW, by_user_id=uuid4())

    def test_closed_to_triaged_forbidden(self) -> None:
        ask = _make_ask()
        ask.transition_to(AskStatus.CLOSED, by_user_id=uuid4())
        with pytest.raises(AskTransitionError):
            ask.transition_to(AskStatus.TRIAGED, by_user_id=uuid4())

    def test_same_state_transition_forbidden(self) -> None:
        ask = _make_ask()
        with pytest.raises(AskTransitionError):
            ask.transition_to(AskStatus.NEW, by_user_id=uuid4())

    def test_triaged_to_new_forbidden(self) -> None:
        ask = _make_ask()
        ask.transition_to(AskStatus.TRIAGED, by_user_id=uuid4())
        with pytest.raises(AskTransitionError):
            ask.transition_to(AskStatus.NEW, by_user_id=uuid4())

    def test_can_transition_to_predicate_reflects_allow_list(self) -> None:
        ask = _make_ask()
        assert ask.can_transition_to(AskStatus.TRIAGED)
        assert not ask.can_transition_to(AskStatus.NEW)


# ── Notes ────────────────────────────────────────────────────────────


class TestNotes:
    def test_empty_note_rejected(self) -> None:
        ask = _make_ask()
        with pytest.raises(AskTransitionError):
            ask.add_note("   ", by_user_id=uuid4())

    def test_first_note_sets_notes_md(self) -> None:
        ask = _make_ask()
        ask.add_note("first thoughts", by_user_id=uuid4())
        assert ask.notes_md == "first thoughts"
        assert ask.events[-1].kind is AskEventKind.NOTE_ADDED

    def test_second_note_appends_with_separator(self) -> None:
        ask = _make_ask()
        ask.add_note("first", by_user_id=uuid4())
        ask.add_note("second", by_user_id=uuid4())
        assert "first" in ask.notes_md
        assert "second" in ask.notes_md
        assert "---" in ask.notes_md

    def test_note_uses_provided_clock(self) -> None:
        ask = _make_ask()
        fixed = datetime(2030, 1, 1, tzinfo=UTC)
        ask.add_note("with clock", by_user_id=uuid4(), now=fixed)
        assert ask.events[-1].at == fixed


# ── Owner assignment ─────────────────────────────────────────────────


class TestOwner:
    def test_assign_owner_records_event_and_sets_field(self) -> None:
        ask = _make_ask()
        new_owner = uuid4()
        ask.assign_owner(new_owner, by_user_id=uuid4())
        assert ask.owner_user_id == new_owner
        assert ask.events[-1].kind is AskEventKind.OWNER_ASSIGNED
        assert ask.events[-1].payload == {"owner_user_id": str(new_owner)}
