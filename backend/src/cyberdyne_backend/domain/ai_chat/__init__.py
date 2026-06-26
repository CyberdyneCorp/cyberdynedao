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
    AttachmentRef,
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
    AttachmentIngestorPort,
    ChatLLMPort,
    ChatRepository,
    CodeRunResult,
    CodeVariable,
    CyberfliesPort,
    DocumentRendererPort,
    IngestedAttachment,
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
    TextExtractorPort,
    ToolSchema,
    VisionPort,
)

__all__ = [
    "AttachmentIngestorPort",
    "AttachmentRef",
    "ChatLLMPort",
    "ChatMessage",
    "ChatProviderError",
    "ChatRepository",
    "ChatRole",
    "ChatSession",
    "ChatSessionNotFoundError",
    "CodeRunResult",
    "CodeVariable",
    "CyberfliesPort",
    "DocumentRendererPort",
    "IngestedAttachment",
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
    "TextExtractorPort",
    "ToolCall",
    "ToolSchema",
    "VisionPort",
    "new_assistant_message",
    "new_session",
    "new_tool_message",
    "new_user_message",
]
