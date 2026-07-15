from datetime import datetime
from enum import Enum

from pydantic import BaseModel, ConfigDict, model_validator


class SensorAction(str, Enum):
    ON = "ON"
    OFF = "OFF"
    OPEN = "OPEN"
    CLOSE = "CLOSE"
    DETECTED = "DETECTED"
    CLEARED = "CLEARED"
    OCCUPIED = "OCCUPIED"
    VACANT = "VACANT"


class SensorEvent(BaseModel):
    """A physical sensor state change; this is the model's only input type."""

    model_config = ConfigDict(extra="forbid", frozen=True, use_enum_values=True)

    timestamp: datetime
    dataset: str
    house: str | None = None
    device_id: str
    device_name: str
    sensor_type: str | None = None
    location: str | None = None
    action: SensorAction
    value: int | float | None = None


class ActivityAnnotation(BaseModel):
    """Ground truth used only after inference, during experiment evaluation."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    start_time: datetime
    end_time: datetime
    activity_id: int
    activity_name: str
    resident: str
    dataset: str
    house: str | None = None

    @model_validator(mode="after")
    def validate_interval(self) -> "ActivityAnnotation":
        if self.end_time <= self.start_time:
            raise ValueError("end_time must be later than start_time")
        return self
