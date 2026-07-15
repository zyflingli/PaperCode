from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

from src.data.models import SensorEvent


@dataclass(frozen=True)
class DatasetSplit:
    train: list[SensorEvent]
    validation: list[SensorEvent]
    test: list[SensorEvent]


def chronological_split(
    events: Iterable[SensorEvent],
    *,
    train_ratio: float = 0.7,
    validation_ratio: float = 0.1,
) -> DatasetSplit:
    """Split sensor events chronologically without consulting activity labels."""

    if not 0 <= train_ratio <= 1 or not 0 <= validation_ratio <= 1:
        raise ValueError("split ratios must be between 0 and 1")
    if train_ratio + validation_ratio > 1:
        raise ValueError("train_ratio + validation_ratio must not exceed 1")

    ordered = list(events)
    for index, event in enumerate(ordered):
        if type(event) is not SensorEvent:
            raise TypeError(f"events[{index}] must be a SensorEvent")
    ordered.sort(key=lambda event: event.timestamp)

    train_end = int(len(ordered) * train_ratio)
    validation_end = train_end + int(len(ordered) * validation_ratio)
    return DatasetSplit(
        train=ordered[:train_end],
        validation=ordered[train_end:validation_end],
        test=ordered[validation_end:],
    )
