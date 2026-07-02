from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field


class Event(BaseModel):
    action: str
    device: str
    timestamp: datetime
    location: str
    sensor_state: dict[str, Any] = Field(default_factory=dict)


class SequencePattern(BaseModel):
    sequence: list[str]
    support: int


class TAPRule(BaseModel):
    trigger: str
    condition: str | None = None
    action: str
    confidence: float | None = None
    source_pattern: list[str] = Field(default_factory=list)
