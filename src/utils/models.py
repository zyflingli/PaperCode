from typing import Any, Literal

from pydantic import BaseModel, Field


class SequencePattern(BaseModel):
    sequence: list[str]
    support: int


class Pattern(BaseModel):
    type: Literal["single", "set", "sequence"]
    context: dict[str, Any] = Field(default_factory=dict)
    items: list[str] = Field(default_factory=list)
    support: float


class TAPRule(BaseModel):
    trigger: str
    condition: str | None = None
    action: str
    confidence: float | None = None
    source_pattern: list[str] = Field(default_factory=list)
