from datetime import datetime
from typing import Any, Literal

from pydantic import BaseModel, Field


class Event(BaseModel):
    action: str
    device: str
    timestamp: datetime
    location: str
    sensor_state: dict[str, Any] = Field(default_factory=dict)


class UnifiedEvent(BaseModel):
    timestamp: datetime | str
    device: str
    location: str
    action: str
    value: Any = None
    resident: str | None = None
    source_dataset: str

    def to_dict(self) -> dict[str, Any]:
        return self.model_dump()


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
