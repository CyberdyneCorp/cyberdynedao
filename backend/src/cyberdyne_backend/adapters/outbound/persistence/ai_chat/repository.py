"""SQLAlchemy adapter for ``ChatRepository``."""

from __future__ import annotations

from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from cyberdyne_backend.adapters.outbound.persistence.ai_chat.models import (
    ChatMessageRow,
    ChatSessionRow,
)
from cyberdyne_backend.domain.ai_chat import (
    AttachmentRef,
    ChatMessage,
    ChatRole,
    ChatSession,
    ChatSessionNotFoundError,
    ToolCall,
)


def _row_to_session(row: ChatSessionRow) -> ChatSession:
    return ChatSession(
        id=row.id,
        user_id=row.user_id,
        created_at=row.created_at,
        last_message_at=row.last_message_at,
    )


def _row_to_message(row: ChatMessageRow) -> ChatMessage:
    tool_calls = tuple(
        ToolCall(
            id=str(tc.get("id", "")),
            name=str(tc.get("name", "")),
            arguments_json=str(tc.get("arguments_json", "")),
        )
        for tc in row.tool_calls or []
    )
    attachments = tuple(
        AttachmentRef(
            id=UUID(str(a.get("id"))),
            filename=str(a.get("filename", "")),
            content_type=str(a.get("contentType", "")),
        )
        for a in row.attachments or []
    )
    return ChatMessage(
        id=row.id,
        session_id=row.session_id,
        role=ChatRole(row.role),
        content=row.content,
        tool_calls=tool_calls,
        tool_call_id=row.tool_call_id,
        tokens_in=row.tokens_in,
        tokens_out=row.tokens_out,
        model=row.model,
        attachments=attachments,
        created_at=row.created_at,
    )


class SqlAlchemyChatRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def save_session(self, session: ChatSession) -> None:
        existing = await self._session.get(ChatSessionRow, session.id)
        if existing is None:
            self._session.add(
                ChatSessionRow(
                    id=session.id,
                    user_id=session.user_id,
                    created_at=session.created_at,
                    last_message_at=session.last_message_at,
                )
            )
        else:
            existing.last_message_at = session.last_message_at
        await self._session.flush()

    async def get_session(self, session_id: UUID) -> ChatSession:
        row = await self._session.get(ChatSessionRow, session_id)
        if row is None:
            raise ChatSessionNotFoundError(f"no chat session with id={session_id}")
        return _row_to_session(row)

    async def append_message(self, message: ChatMessage) -> None:
        self._session.add(
            ChatMessageRow(
                id=message.id,
                session_id=message.session_id,
                role=message.role.value,
                content=message.content,
                tool_calls=[
                    {
                        "id": tc.id,
                        "name": tc.name,
                        "arguments_json": tc.arguments_json,
                    }
                    for tc in message.tool_calls
                ],
                attachments=[
                    {
                        "id": str(a.id),
                        "filename": a.filename,
                        "contentType": a.content_type,
                    }
                    for a in message.attachments
                ]
                or None,
                tool_call_id=message.tool_call_id,
                tokens_in=message.tokens_in,
                tokens_out=message.tokens_out,
                model=message.model,
                created_at=message.created_at,
            )
        )
        # Touch the session's last_message_at marker so listing recent
        # sessions doesn't require a per-row aggregate.
        sess_row = await self._session.get(ChatSessionRow, message.session_id)
        if sess_row is not None:
            sess_row.last_message_at = message.created_at
        await self._session.flush()

    async def list_messages(self, session_id: UUID) -> list[ChatMessage]:
        rows = (
            (
                await self._session.execute(
                    select(ChatMessageRow)
                    .where(ChatMessageRow.session_id == session_id)
                    .order_by(ChatMessageRow.created_at, ChatMessageRow.id)
                )
            )
            .scalars()
            .all()
        )
        return [_row_to_message(r) for r in rows]
