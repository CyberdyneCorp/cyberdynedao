"""AI chat use cases — session bootstrap, turn execution, history."""

from __future__ import annotations

import logging
from dataclasses import dataclass
from uuid import UUID

from cyberdyne_backend.application.ai_chat.tools import CYBERDYNE_TOOLS, ToolDispatcher
from cyberdyne_backend.domain.ai_chat import (
    ChatLLMPort,
    ChatMessage,
    ChatRepository,
    ChatSession,
    new_assistant_message,
    new_session,
    new_tool_message,
    new_user_message,
)

logger = logging.getLogger("cyberdyne_backend.ai_chat")

SYSTEM_PROMPT = (
    "You are Cyberdyne's terminal assistant. You help users learn about the company's "
    "projects, training paths, and marketplace products. Use the provided tools to "
    "look up real data instead of guessing. Be concise, terminal-style, no emoji. "
    "If the user asks for human follow-up, confirm their email before calling "
    "create_ask_for_handoff."
)

MAX_TOOL_ROUNDS = 4


@dataclass(slots=True)
class StartChatSession:
    repo: ChatRepository

    async def execute(self, *, user_id: UUID | None = None) -> ChatSession:
        session = new_session(user_id=user_id)
        await self.repo.save_session(session)
        return session


@dataclass(slots=True)
class GetChatHistory:
    repo: ChatRepository

    async def execute(self, session_id: UUID) -> list[ChatMessage]:
        # Raises ChatSessionNotFoundError if missing.
        await self.repo.get_session(session_id)
        return await self.repo.list_messages(session_id)


@dataclass(slots=True)
class RunChatTurn:
    """Runs one user turn end-to-end: persist user message, call LLM in a
    tool-call loop, persist intermediate tool results, persist final
    assistant message. Returns the final assistant message."""

    repo: ChatRepository
    llm: ChatLLMPort
    dispatcher: ToolDispatcher
    system_prompt: str = SYSTEM_PROMPT
    max_tool_rounds: int = MAX_TOOL_ROUNDS

    async def execute(self, *, session_id: UUID, user_content: str) -> ChatMessage:
        # Raises ChatSessionNotFoundError if missing.
        await self.repo.get_session(session_id)
        user_msg = new_user_message(session_id=session_id, content=user_content)
        await self.repo.append_message(user_msg)

        for _ in range(self.max_tool_rounds):
            transcript = await self.repo.list_messages(session_id)
            response = await self.llm.complete(
                messages=transcript,
                tools=CYBERDYNE_TOOLS,
                system_prompt=self.system_prompt,
            )
            assistant_msg = new_assistant_message(
                session_id=session_id,
                content=response.content,
                tool_calls=response.tool_calls,
                tokens_in=response.tokens_in,
                tokens_out=response.tokens_out,
                model=response.model,
            )
            await self.repo.append_message(assistant_msg)
            if not response.tool_calls:
                return assistant_msg
            for call in response.tool_calls:
                result_text = await self.dispatcher.dispatch(call)
                tool_msg = new_tool_message(
                    session_id=session_id,
                    tool_call_id=call.id,
                    content=result_text,
                )
                await self.repo.append_message(tool_msg)
        # Hit the cap — return the last assistant turn we wrote.
        transcript = await self.repo.list_messages(session_id)
        return transcript[-1]
