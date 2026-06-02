"""Use case for the interactive code-interpreter lesson type.

Runs a learner's code against the MATLAB-LLVM engine (the same engine the
chat agent's ``matlab_*`` tools use). Each (lesson, user) pair gets its
own stateful workspace so variables persist across runs within a lesson
but never bleed between learners. The bearer is forwarded so execution
and any artifacts land in the signed-in user's sandbox.
"""

from __future__ import annotations

from dataclasses import dataclass
from uuid import UUID

from cyberdyne_backend.domain.ai_chat import MatlabPort, MatlabRunResult


@dataclass(slots=True)
class RunLessonCode:
    matlab: MatlabPort

    async def execute(
        self, *, lesson_id: UUID, source: str, user_id: UUID, bearer: str | None
    ) -> MatlabRunResult:
        # Per-(lesson, user) workspace: stateful within a lesson, isolated
        # between learners.
        session_id = f"lesson-{lesson_id}-{user_id}"
        return await self.matlab.run_repl(source=source, session_id=session_id, bearer=bearer)


__all__ = ["RunLessonCode"]
