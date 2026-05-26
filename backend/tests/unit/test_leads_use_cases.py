"""Use-case tests for the leads context.

Uses hand-written fakes for the repository, captcha, and email
notifier — same pattern as the content tests.
"""

from __future__ import annotations

from datetime import UTC, datetime
from uuid import UUID, uuid4

import pytest

from cyberdyne_backend.application.leads import (
    AdminListAsks,
    AdminUpdateAsk,
    CreateAsk,
)
from cyberdyne_backend.application.leads.use_cases import (
    AdminListAsksQuery,
    AdminUpdateAskCommand,
    CreateAskCommand,
)
from cyberdyne_backend.domain.leads import (
    Ask,
    AskChannel,
    AskNotFoundError,
    AskStatus,
    AskTransitionError,
    CaptchaVerificationError,
    new_ask,
)


class FakeAskRepo:
    def __init__(self, seed: list[Ask] | None = None) -> None:
        self._asks: dict[UUID, Ask] = {a.id: a for a in (seed or [])}
        self.save_count = 0

    async def save(self, ask: Ask) -> None:
        self._asks[ask.id] = ask
        self.save_count += 1

    async def get(self, ask_id: UUID) -> Ask:
        try:
            return self._asks[ask_id]
        except KeyError as exc:
            raise AskNotFoundError(f"missing id {ask_id}") from exc

    async def list_admin(
        self,
        *,
        status: AskStatus | None = None,
        channel: str | None = None,
        query: str | None = None,
        page: int = 1,
        page_size: int = 50,
    ) -> tuple[list[Ask], int]:
        items = list(self._asks.values())
        if status is not None:
            items = [a for a in items if a.status == status]
        if channel:
            items = [a for a in items if a.channel.value == channel]
        if query:
            q = query.lower()
            items = [a for a in items if q in a.body.lower() or q in a.email.lower()]
        total = len(items)
        return items[(page - 1) * page_size : page * page_size], total


class FakeCaptcha:
    def __init__(self, *, allow: bool = True) -> None:
        self.allow = allow
        self.calls: list[tuple[str, str | None]] = []

    async def verify(self, token: str, remote_ip: str | None) -> None:
        self.calls.append((token, remote_ip))
        if not self.allow:
            raise CaptchaVerificationError("rejected by fake")


class FakeEmailNotifier:
    def __init__(self) -> None:
        self.sent: list[Ask] = []

    async def send_new_ask_notification(self, ask: Ask) -> None:
        self.sent.append(ask)


# ── CreateAsk ────────────────────────────────────────────────────────


class TestCreateAsk:
    async def test_persists_and_notifies_on_success(self) -> None:
        repo, captcha, notifier = FakeAskRepo(), FakeCaptcha(), FakeEmailNotifier()
        uc = CreateAsk(repo=repo, captcha=captcha, notifier=notifier)
        cmd = CreateAskCommand(
            name="Alice",
            email="alice@example.com",
            body="hi",
            channel=AskChannel.CONTACT_FORM,
            captcha_token="ok",
            remote_ip="1.2.3.4",
            product_slug=None,
            source_url=None,
        )
        ask = await uc.execute(cmd)
        assert ask.status is AskStatus.NEW
        assert repo.save_count == 1
        assert len(notifier.sent) == 1
        assert notifier.sent[0] is ask
        assert captcha.calls == [("ok", "1.2.3.4")]

    async def test_captcha_failure_short_circuits(self) -> None:
        repo, captcha, notifier = FakeAskRepo(), FakeCaptcha(allow=False), FakeEmailNotifier()
        uc = CreateAsk(repo=repo, captcha=captcha, notifier=notifier)
        cmd = CreateAskCommand(
            name="A",
            email="a@b.c",
            body="x",
            channel=AskChannel.CONTACT_FORM,
            captcha_token="bad",
            remote_ip=None,
            product_slug=None,
            source_url=None,
        )
        with pytest.raises(CaptchaVerificationError):
            await uc.execute(cmd)
        assert repo.save_count == 0
        assert notifier.sent == []


# ── AdminListAsks ────────────────────────────────────────────────────


class TestAdminListAsks:
    async def test_filters_by_status(self) -> None:
        ask_a = new_ask(channel=AskChannel.CONTACT_FORM, name="a", email="a@b.c", body="x")
        ask_b = new_ask(channel=AskChannel.CONTACT_FORM, name="b", email="b@c.d", body="y")
        ask_b.transition_to(AskStatus.CLOSED, by_user_id=uuid4())
        repo = FakeAskRepo(seed=[ask_a, ask_b])
        uc = AdminListAsks(repo=repo)
        items, total = await uc.execute(AdminListAsksQuery(status=AskStatus.CLOSED))
        assert total == 1
        assert items[0].id == ask_b.id

    async def test_pagination(self) -> None:
        asks = [
            new_ask(channel=AskChannel.CONTACT_FORM, name=f"p{i}", email=f"p{i}@x.y", body="body")
            for i in range(5)
        ]
        uc = AdminListAsks(repo=FakeAskRepo(seed=asks))
        _, total = await uc.execute(AdminListAsksQuery(page=1, page_size=2))
        assert total == 5

    async def test_query_searches_body_and_email(self) -> None:
        a = new_ask(channel=AskChannel.CONTACT_FORM, name="A", email="a@example.com", body="x")
        b = new_ask(channel=AskChannel.CONTACT_FORM, name="B", email="b@x.com", body="WHATEVER")
        uc = AdminListAsks(repo=FakeAskRepo(seed=[a, b]))
        items, total = await uc.execute(AdminListAsksQuery(query="whatever"))
        assert total == 1
        assert items[0].id == b.id


# ── AdminUpdateAsk ───────────────────────────────────────────────────


class TestAdminUpdateAsk:
    async def test_applies_status_note_owner_in_one_call(self) -> None:
        ask = new_ask(channel=AskChannel.CONTACT_FORM, name="A", email="a@b.c", body="x")
        repo = FakeAskRepo(seed=[ask])
        uc = AdminUpdateAsk(repo=repo)
        admin = uuid4()
        new_owner = uuid4()
        result = await uc.execute(
            AdminUpdateAskCommand(
                ask_id=ask.id,
                by_user_id=admin,
                new_status=AskStatus.TRIAGED,
                note="initial triage",
                new_owner_user_id=new_owner,
            )
        )
        assert result.status is AskStatus.TRIAGED
        assert result.owner_user_id == new_owner
        assert "initial triage" in result.notes_md
        # CREATED + NOTE_ADDED + OWNER_ASSIGNED + STATUS_CHANGED
        assert len(result.events) == 4
        assert repo.save_count == 1

    async def test_missing_ask_raises(self) -> None:
        uc = AdminUpdateAsk(repo=FakeAskRepo())
        with pytest.raises(AskNotFoundError):
            await uc.execute(
                AdminUpdateAskCommand(
                    ask_id=uuid4(),
                    by_user_id=uuid4(),
                    new_status=AskStatus.TRIAGED,
                )
            )

    async def test_invalid_transition_propagates(self) -> None:
        ask = new_ask(channel=AskChannel.CONTACT_FORM, name="A", email="a@b.c", body="x")
        ask.transition_to(AskStatus.CLOSED, by_user_id=uuid4())
        repo = FakeAskRepo(seed=[ask])
        uc = AdminUpdateAsk(repo=repo)
        with pytest.raises(AskTransitionError):
            await uc.execute(
                AdminUpdateAskCommand(
                    ask_id=ask.id,
                    by_user_id=uuid4(),
                    new_status=AskStatus.NEW,  # forbidden
                )
            )


# Silence unused-import for clarity in case mypy/ruff complain
_ = datetime, UTC
