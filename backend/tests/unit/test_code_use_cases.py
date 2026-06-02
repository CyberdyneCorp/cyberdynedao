"""Use-case tests for the code-interpreter (RunLessonCode)."""

from __future__ import annotations

import uuid

from cyberdyne_backend.application.code import RunLessonCode
from cyberdyne_backend.domain.ai_chat import MatlabRunResult


class _FakeMatlab:
    def __init__(self) -> None:
        self.calls: list[dict[str, object]] = []

    async def run_repl(self, *, source, session_id, bearer):
        self.calls.append({"source": source, "session_id": session_id, "bearer": bearer})
        return MatlabRunResult(ok=True, stdout="4", stderr="", session_id=session_id)

    async def run_plot(self, *, source, session_id, bearer, fmt="png"):
        return MatlabRunResult(ok=True, stdout="", stderr="", session_id=session_id)


class TestRunLessonCode:
    async def test_runs_on_per_lesson_user_session(self) -> None:
        matlab = _FakeMatlab()
        lesson_id = uuid.uuid4()
        user_id = uuid.uuid4()
        res = await RunLessonCode(matlab=matlab).execute(
            lesson_id=lesson_id, source="2 + 2", user_id=user_id, bearer="tok"
        )
        assert res.ok is True
        assert res.stdout == "4"
        # Session is isolated per (lesson, user); bearer forwarded.
        call = matlab.calls[0]
        assert call["session_id"] == f"lesson-{lesson_id}-{user_id}"
        assert call["bearer"] == "tok"
        assert call["source"] == "2 + 2"

    async def test_two_users_get_separate_sessions(self) -> None:
        matlab = _FakeMatlab()
        lesson_id = uuid.uuid4()
        uc = RunLessonCode(matlab=matlab)
        await uc.execute(lesson_id=lesson_id, source="x=1", user_id=uuid.uuid4(), bearer=None)
        await uc.execute(lesson_id=lesson_id, source="x=1", user_id=uuid.uuid4(), bearer=None)
        assert matlab.calls[0]["session_id"] != matlab.calls[1]["session_id"]
