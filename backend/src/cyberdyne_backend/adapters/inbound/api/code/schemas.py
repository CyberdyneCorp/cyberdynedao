"""Pydantic schemas for the code-interpreter endpoint."""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field
from pydantic.alias_generators import to_camel


class _CamelModel(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)


class RunCodeRequest(_CamelModel):
    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True, extra="forbid")

    source: str = Field(min_length=1, description="Source to execute.")
    language: Literal["matlab", "python"] = Field(
        default="matlab", description="Engine to run on; defaults to MATLAB."
    )


class CodeVariableView(_CamelModel):
    """One entry in the post-run variable namespace (Lab Variables panel)."""

    name: str
    type: str
    repr: str
    size_bytes: int | None = None


class RichOutputView(_CamelModel):
    """An inline rich output (plot/image/HTML/JSON). ``artifact`` names a
    workspace file to download for binary outputs (e.g. ``image/png``);
    ``text`` carries inline content for ``text/*`` / ``application/json``."""

    mime_type: str
    artifact: str | None = None
    text: str | None = None


class RunCodeResponse(_CamelModel):
    ok: bool
    stdout: str
    stderr: str
    artifacts: list[str]
    session_id: str
    timed_out: bool
    # Additive (#166): the Lab Variables + Plot panels. Both default empty —
    # MATLAB runs and backends that don't expose a namespace leave them so,
    # keeping the response backward compatible.
    variables: list[CodeVariableView] = []
    rich_outputs: list[RichOutputView] = []
