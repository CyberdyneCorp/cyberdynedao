"""Global Agent Chat application layer (issue #234).

A top-level answer agent for signed-in learners: answers directly, grounds on
the learner's own history via a small learner-context tool set, accepts image
attachments, points each answer at the course/lesson that covers it, and logs
out-of-catalog topics to the demand registry (#232).
"""

from cyberdyne_backend.application.agent_chat.tools import (
    AGENT_TOOLS,
    LEARNER_CONTEXT_TOOLS,
    LearnerContextDispatcher,
    LearnerContextToolset,
    NotebookActionProposal,
)
from cyberdyne_backend.application.agent_chat.use_cases import (
    ANSWER_AGENT_SYSTEM_PROMPT,
    AnswerAgentTurn,
    AnswerTurnResult,
    UnmatchedTopic,
)

__all__ = [
    "AGENT_TOOLS",
    "ANSWER_AGENT_SYSTEM_PROMPT",
    "LEARNER_CONTEXT_TOOLS",
    "AnswerAgentTurn",
    "AnswerTurnResult",
    "LearnerContextDispatcher",
    "LearnerContextToolset",
    "NotebookActionProposal",
    "UnmatchedTopic",
]
