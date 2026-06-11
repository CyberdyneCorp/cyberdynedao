"""AI chat bounded context.

Backs the existing terminal-style chat surface with an OpenAI agent
that has tools over Cyberdyne's own content (projects, learning,
marketplace) and lead-capture.

Knowledge backend (semantic search) is consumed via a CyberRAG MCP
client port. v1 ships with a stub that returns "no semantic index
configured" — the agent's exact-lookup tools (slug-keyed) work
without CyberRAG. Hooking up real CyberRAG is a follow-up adapter swap.
"""

from cyberdyne_backend.domain.ai_chat.entities import (
    ChatMessage,
    ChatRole,
    ChatSession,
    ToolCall,
    new_assistant_message,
    new_session,
    new_tool_message,
    new_user_message,
)
from cyberdyne_backend.domain.ai_chat.errors import (
    ChatProviderError,
    ChatSessionNotFoundError,
)
from cyberdyne_backend.domain.ai_chat.ports import (
    ChatLLMPort,
    ChatRepository,
    CyberfliesPort,
    DocumentRendererPort,
    KnowledgeSearchPort,
    LLMResponse,
    LLMStreamChunk,
    ManimRenderResult,
    MatlabCheckResult,
    MatlabCodegenResult,
    MatlabDiagnostic,
    MatlabPort,
    MatlabRunResult,
    MeetingDetail,
    MeetingSummary,
    PythonExecResult,
    PythonInterpreterPort,
    RichOutput,
    ToolSchema,
)

__all__ = [
    "ChatLLMPort",
    "ChatMessage",
    "ChatProviderError",
    "ChatRepository",
    "ChatRole",
    "ChatSession",
    "ChatSessionNotFoundError",
    "CyberfliesPort",
    "DocumentRendererPort",
    "KnowledgeSearchPort",
    "LLMResponse",
    "LLMStreamChunk",
    "ManimRenderResult",
    "MatlabCheckResult",
    "MatlabCodegenResult",
    "MatlabDiagnostic",
    "MatlabPort",
    "MatlabRunResult",
    "MeetingDetail",
    "MeetingSummary",
    "PythonExecResult",
    "PythonInterpreterPort",
    "RichOutput",
    "ToolCall",
    "ToolSchema",
    "new_assistant_message",
    "new_session",
    "new_tool_message",
    "new_user_message",
]
