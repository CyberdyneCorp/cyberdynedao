"""Use cases for the leads context."""

from __future__ import annotations

from dataclasses import dataclass
from uuid import UUID

from cyberdyne_backend.domain.leads import (
    Ask,
    AskChannel,
    AskRepository,
    AskStatus,
    CaptchaPort,
    EmailNotifierPort,
    new_ask,
)


@dataclass(slots=True)
class CreateAskCommand:
    name: str
    email: str
    body: str
    channel: AskChannel
    captcha_token: str
    remote_ip: str | None
    product_slug: str | None = None
    source_url: str | None = None


@dataclass(slots=True)
class CreateAsk:
    """Public-facing ask submission.

    Captcha runs first (rejection short-circuits the use case); on
    success the Ask is persisted and the notifier fires. Notifier
    failures must not surface to the caller — the adapter is responsible
    for swallowing them.
    """

    repo: AskRepository
    captcha: CaptchaPort
    notifier: EmailNotifierPort

    async def execute(self, cmd: CreateAskCommand) -> Ask:
        await self.captcha.verify(cmd.captcha_token, cmd.remote_ip)
        ask = new_ask(
            channel=cmd.channel,
            name=cmd.name,
            email=cmd.email,
            body=cmd.body,
            product_slug=cmd.product_slug,
            source_url=cmd.source_url,
        )
        await self.repo.save(ask)
        await self.notifier.send_new_ask_notification(ask)
        return ask


@dataclass(slots=True)
class AdminListAsksQuery:
    status: AskStatus | None = None
    channel: str | None = None
    query: str | None = None
    page: int = 1
    page_size: int = 50


@dataclass(slots=True)
class AdminListAsks:
    repo: AskRepository

    async def execute(self, q: AdminListAsksQuery) -> tuple[list[Ask], int]:
        return await self.repo.list_admin(
            status=q.status,
            channel=q.channel,
            query=q.query,
            page=q.page,
            page_size=q.page_size,
        )


@dataclass(slots=True)
class AdminUpdateAskCommand:
    ask_id: UUID
    by_user_id: UUID
    new_status: AskStatus | None = None
    note: str | None = None
    new_owner_user_id: UUID | None = None


@dataclass(slots=True)
class AdminUpdateAsk:
    """Editor-only update — any combination of status change, note add,
    and/or owner assignment can be applied in one call. Each one emits
    its own AskEvent."""

    repo: AskRepository

    async def execute(self, cmd: AdminUpdateAskCommand) -> Ask:
        ask = await self.repo.get(cmd.ask_id)
        if cmd.note is not None:
            ask.add_note(cmd.note, by_user_id=cmd.by_user_id)
        if cmd.new_owner_user_id is not None:
            ask.assign_owner(cmd.new_owner_user_id, by_user_id=cmd.by_user_id)
        if cmd.new_status is not None:
            ask.transition_to(cmd.new_status, by_user_id=cmd.by_user_id)
        await self.repo.save(ask)
        return ask
