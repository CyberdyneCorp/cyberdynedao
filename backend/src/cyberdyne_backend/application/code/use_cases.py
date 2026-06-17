"""Use case for the interactive code-interpreter lesson type.

Runs a learner's code on the engine that matches the lesson's language:
MATLAB lessons execute on the MATLAB-LLVM engine (the same one the chat
agent's ``matlab_*`` tools use); Python lessons execute on the Python
interpreter sandbox. The bearer is forwarded either way so execution and
any artifacts land in the signed-in user's workspace.

MATLAB uses a deterministic per-(lesson, user) session so variables persist
across runs within a lesson. The Python interpreter only accepts
server-issued session ids, so each Python run gets a fresh session (each run
is self-contained) — see [[interpreter-backend-constraints]].
"""

from __future__ import annotations

from dataclasses import dataclass
from uuid import UUID

from cyberdyne_backend.domain.ai_chat import (
    CodeRunResult,
    MatlabPort,
    PythonInterpreterPort,
)


@dataclass(slots=True)
class RunLessonCode:
    matlab: MatlabPort
    python: PythonInterpreterPort | None = None

    async def execute(
        self,
        *,
        lesson_id: UUID,
        source: str,
        user_id: UUID,
        bearer: str | None,
        language: str = "matlab",
    ) -> CodeRunResult:
        if language == "python" and self.python is not None:
            return await self._run_python(source=source, bearer=bearer)
        # Default: MATLAB. Per-(lesson, user) workspace — stateful within a
        # lesson, isolated between learners. MATLAB exposes no variable
        # namespace / inline rich outputs here — figures land in artifacts.
        session_id = f"lesson-{lesson_id}-{user_id}"
        res = await self.matlab.run_repl(source=source, session_id=session_id, bearer=bearer)
        return CodeRunResult(
            ok=res.ok,
            stdout=res.stdout,
            stderr=res.stderr,
            artifacts=res.artifacts,
            session_id=res.session_id,
            timed_out=res.timed_out,
        )

    async def _run_python(self, *, source: str, bearer: str | None) -> CodeRunResult:
        assert self.python is not None
        session_id = await self.python.create_session(bearer=bearer)
        res = await self.python.execute(code=source, session_id=session_id, bearer=bearer)
        # Fold the interpreter's `error` into stderr; surface the variable
        # namespace + inline rich outputs the interpreter captured (the Lab
        # Variables/Plot panels). Python has no timeout signal.
        stderr = res.stderr
        if res.error:
            stderr = f"{stderr}\n{res.error}" if stderr else res.error
        return CodeRunResult(
            ok=res.ok,
            stdout=res.stdout,
            stderr=stderr,
            artifacts=res.artifacts,
            session_id=res.session_id,
            timed_out=False,
            variables=res.variables,
            rich_outputs=res.rich_outputs,
        )


__all__ = ["RunLessonCode"]
