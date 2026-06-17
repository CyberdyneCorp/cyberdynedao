"""Use-case tests for the code-interpreter (RunLessonCode)."""

from __future__ import annotations

import uuid

from cyberdyne_backend.application.code import RunLessonCode
from cyberdyne_backend.domain.ai_chat import (
    CodeVariable,
    MatlabRunResult,
    PythonExecResult,
    RichOutput,
)


class _FakeMatlab:
    def __init__(self) -> None:
        self.calls: list[dict[str, object]] = []

    async def run_repl(self, *, source, session_id, bearer):
        self.calls.append({"source": source, "session_id": session_id, "bearer": bearer})
        return MatlabRunResult(ok=True, stdout="4", stderr="", session_id=session_id)

    async def run_plot(self, *, source, session_id, bearer, fmt="png"):
        return MatlabRunResult(ok=True, stdout="", stderr="", session_id=session_id)


class _FakePython:
    def __init__(self) -> None:
        self.calls: list[dict[str, object]] = []
        self.created = 0

    async def create_session(self, *, bearer):
        self.created += 1
        return f"srv-{self.created}"

    async def execute(self, *, code, session_id, bearer, restricted=True):
        self.calls.append({"code": code, "session_id": session_id, "bearer": bearer})
        return PythonExecResult(
            ok=True, stdout="hello\n", stderr="", result=None, error=None, session_id=session_id
        )


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

    async def test_python_language_runs_on_interpreter(self) -> None:
        matlab = _FakeMatlab()
        python = _FakePython()
        res = await RunLessonCode(matlab=matlab, python=python).execute(
            lesson_id=uuid.uuid4(),
            source="print('hello')",
            user_id=uuid.uuid4(),
            bearer="tok",
            language="python",
        )
        assert res.ok is True
        assert res.stdout == "hello\n"
        assert res.timed_out is False
        # Ran on the interpreter (server-issued session), NOT MATLAB.
        assert python.created == 1
        assert python.calls[0]["code"] == "print('hello')"
        assert python.calls[0]["bearer"] == "tok"
        assert matlab.calls == []

    async def test_python_error_is_folded_into_stderr(self) -> None:
        matlab = _FakeMatlab()

        class _ErrPython(_FakePython):
            async def execute(self, *, code, session_id, bearer, restricted=True):
                return PythonExecResult(
                    ok=False, stdout="", stderr="", error="NameError: x", session_id=session_id
                )

        res = await RunLessonCode(matlab=matlab, python=_ErrPython()).execute(
            lesson_id=uuid.uuid4(), source="x", user_id=uuid.uuid4(), bearer=None, language="python"
        )
        assert res.ok is False
        assert "NameError: x" in res.stderr

    async def test_matlab_is_the_default_language(self) -> None:
        matlab = _FakeMatlab()
        python = _FakePython()
        await RunLessonCode(matlab=matlab, python=python).execute(
            lesson_id=uuid.uuid4(), source="2+2", user_id=uuid.uuid4(), bearer=None
        )
        assert len(matlab.calls) == 1
        assert python.calls == []

    async def test_python_surfaces_variables_and_rich_outputs(self) -> None:
        class _RichPython(_FakePython):
            async def execute(self, *, code, session_id, bearer, restricted=True):
                return PythonExecResult(
                    ok=True,
                    stdout="",
                    stderr="",
                    session_id=session_id,
                    variables=(CodeVariable(name="x", type="int", repr="42", size_bytes=28),),
                    rich_outputs=(RichOutput(mime_type="image/png", artifact="fig1.png"),),
                )

        res = await RunLessonCode(matlab=_FakeMatlab(), python=_RichPython()).execute(
            lesson_id=uuid.uuid4(),
            source="x = 42",
            user_id=uuid.uuid4(),
            bearer=None,
            language="python",
        )
        assert [v.name for v in res.variables] == ["x"]
        assert res.variables[0].repr == "42"
        assert res.variables[0].size_bytes == 28
        assert res.rich_outputs[0].mime_type == "image/png"
        assert res.rich_outputs[0].artifact == "fig1.png"

    async def test_matlab_run_has_empty_variables_and_rich_outputs(self) -> None:
        res = await RunLessonCode(matlab=_FakeMatlab()).execute(
            lesson_id=uuid.uuid4(), source="2+2", user_id=uuid.uuid4(), bearer=None
        )
        assert res.variables == ()
        assert res.rich_outputs == ()
