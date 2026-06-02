"""Pydantic schemas for the code-interpreter endpoint."""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field
from pydantic.alias_generators import to_camel


class _CamelModel(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)


class RunCodeRequest(_CamelModel):
    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True, extra="forbid")

    source: str = Field(min_length=1, description="Source to execute on the MATLAB engine.")


class RunCodeResponse(_CamelModel):
    ok: bool
    stdout: str
    stderr: str
    artifacts: list[str]
    session_id: str
    timed_out: bool
