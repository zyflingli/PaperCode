from __future__ import annotations

import re
from dataclasses import dataclass
from datetime import datetime, timedelta
from pathlib import Path
from typing import Iterable

import pandas as pd

from src.data.models import ActivityAnnotation, SensorEvent


@dataclass(frozen=True)
class ARASSensorDefinition:
    column: int
    device_id: str
    sensor_type: str
    device_name: str


@dataclass(frozen=True)
class ARASMetadata:
    house: str
    sensors: tuple[ARASSensorDefinition, ...]
    activities: dict[int, str]


class ARASDataLoader:
    """Load ARAS state transitions separately from its resident annotations."""

    default_dataset_dir = Path("CPS40/2. ARAS datasets")
    house_dirs = {"A": "House A", "B": "House B"}
    expected_rows_per_day = 86_400

    def __init__(
        self,
        dataset_dir: str | Path | None = None,
        *,
        houses: Iterable[str] = ("A", "B"),
        days: Iterable[int] | None = None,
        base_date: datetime = datetime(2000, 1, 1),
        validate: bool = False,
    ) -> None:
        self.dataset_dir = Path(dataset_dir) if dataset_dir is not None else self.default_dataset_dir
        self.houses = tuple(self.normalize_house(house) for house in houses)
        self.days = tuple(days) if days is not None else None
        self.base_date = base_date
        self.validate = validate

    def load_sensor_events(self) -> list[SensorEvent]:
        """Read only the 20 sensor columns and emit state changes."""

        events: list[SensorEvent] = []
        for house in self.houses:
            metadata = self.load_metadata(house)
            previous: list[int] | None = None
            previous_day: int | None = None
            for day in self._selected_days(house):
                path = self._day_path(house, day)
                frame = pd.read_csv(
                    path,
                    sep=r"\s+",
                    header=None,
                    usecols=range(len(metadata.sensors)),
                    dtype="int8",
                )
                self._validate_sensor_frame(frame, path, len(metadata.sensors))
                contiguous = previous_day is not None and day == previous_day + 1
                for column, sensor in enumerate(metadata.sensors):
                    values = frame.iloc[:, column]
                    initial = previous[column] if contiguous and previous is not None else 0
                    changed = values.ne(values.shift(fill_value=initial))
                    for row_index in values.index[changed]:
                        value = int(values.loc[row_index])
                        events.append(
                            SensorEvent(
                                timestamp=self._timestamp(day, int(row_index)),
                                dataset="ARAS",
                                house=house,
                                device_id=sensor.device_id,
                                device_name=sensor.device_name,
                                sensor_type=sensor.sensor_type,
                                location=self._infer_location(sensor.device_name),
                                action=self._sensor_action(sensor, value),
                                value=value,
                            )
                        )
                previous = [int(frame.iloc[-1, column]) for column in range(len(metadata.sensors))]
                previous_day = day
        return sorted(events, key=lambda event: (event.timestamp, event.house or "", event.device_id))

    def load_activity_annotations(self) -> list[ActivityAnnotation]:
        """Read label columns into evaluation-only activity intervals."""

        annotations: list[ActivityAnnotation] = []
        for house in self.houses:
            metadata = self.load_metadata(house)
            house_annotations: list[ActivityAnnotation] = []
            for day in self._selected_days(house):
                path = self._day_path(house, day)
                frame = pd.read_csv(
                    path,
                    sep=r"\s+",
                    header=None,
                    usecols=[20, 21],
                    names=["R1", "R2"],
                    dtype="int16",
                )
                self._validate_annotation_frame(frame, path, metadata.activities)
                for resident in ("R1", "R2"):
                    values = frame[resident]
                    starts = list(values.index[values.ne(values.shift())])
                    for position, start_second in enumerate(starts):
                        end_second = starts[position + 1] if position + 1 < len(starts) else len(values)
                        activity_id = int(values.loc[start_second])
                        house_annotations.append(
                            ActivityAnnotation(
                                start_time=self._timestamp(day, int(start_second)),
                                end_time=self._timestamp(day, int(end_second)),
                                activity_id=activity_id,
                                activity_name=metadata.activities.get(
                                    activity_id, f"Activity {activity_id}"
                                ),
                                resident=resident,
                                dataset="ARAS",
                                house=house,
                            )
                        )
            annotations.extend(self._merge_adjacent_annotations(house_annotations))
        return sorted(
            annotations,
            key=lambda annotation: (annotation.start_time, annotation.house or "", annotation.resident),
        )

    def load_metadata(self, house: str) -> ARASMetadata:
        normalized_house = self.normalize_house(house)
        path = self.dataset_dir / self.house_dirs[normalized_house] / "README"
        if not path.exists():
            raise FileNotFoundError(f"ARAS metadata file not found: {path}")
        sensors: list[ARASSensorDefinition] = []
        activities: dict[int, str] = {}
        section: str | None = None
        with path.open("r", encoding="utf-8") as handle:
            for raw_line in handle:
                line = raw_line.strip()
                upper = line.upper()
                if upper.startswith("SENSOR EXPLANATIONS"):
                    section = "sensors"
                    continue
                if upper.startswith("ACTIVITY EXPLANATIONS"):
                    section = "activities"
                    continue
                if not line or line.lower().startswith(("column", "id")):
                    continue
                if section == "sensors":
                    sensor = self._parse_sensor(line)
                    if sensor is not None:
                        sensors.append(sensor)
                elif section == "activities":
                    match = re.match(r"^(\d+)\s+(.+)$", line)
                    if match:
                        activities[int(match.group(1))] = match.group(2).strip()
        sensors.sort(key=lambda sensor: sensor.column)
        if len(sensors) != 20:
            raise ValueError(f"Expected 20 ARAS sensors in {path}, found {len(sensors)}")
        if not activities:
            raise ValueError(f"No ARAS activities found in {path}")
        return ARASMetadata(normalized_house, tuple(sensors), activities)

    def available_days(self, house: str) -> list[int]:
        directory = self.dataset_dir / self.house_dirs[self.normalize_house(house)]
        days: list[int] = []
        for path in directory.glob("DAY_*.txt"):
            match = re.fullmatch(r"DAY_(\d+)\.txt", path.name)
            if match:
                days.append(int(match.group(1)))
        return sorted(days)

    def _selected_days(self, house: str) -> list[int]:
        return sorted(self.days) if self.days is not None else self.available_days(house)

    def _day_path(self, house: str, day: int) -> Path:
        path = self.dataset_dir / self.house_dirs[house] / f"DAY_{day}.txt"
        if not path.exists():
            raise FileNotFoundError(f"ARAS day file not found: {path}")
        return path

    def _timestamp(self, day: int, second: int) -> datetime:
        return self.base_date + timedelta(days=day - 1, seconds=second)

    def _validate_sensor_frame(self, frame: pd.DataFrame, path: Path, count: int) -> None:
        if self.validate and len(frame) != self.expected_rows_per_day:
            raise ValueError(f"Expected 86400 rows in {path}, found {len(frame)}")
        if frame.shape[1] != count or not frame.isin([0, 1]).all().all():
            raise ValueError(f"Invalid discrete sensor data in {path}")

    def _validate_annotation_frame(
        self, frame: pd.DataFrame, path: Path, activities: dict[int, str]
    ) -> None:
        if self.validate and len(frame) != self.expected_rows_per_day:
            raise ValueError(f"Expected 86400 rows in {path}, found {len(frame)}")
        if not frame.isin(set(activities)).all().all():
            raise ValueError(f"Unknown activity ID in {path}")

    @staticmethod
    def _parse_sensor(line: str) -> ARASSensorDefinition | None:
        parts = [part.strip() for part in re.split(r"\t+|\s{2,}", line) if part.strip()]
        if len(parts) < 4 or not parts[0].isdigit():
            return None
        return ARASSensorDefinition(int(parts[0]), parts[1], parts[2], " ".join(parts[3:]))

    @staticmethod
    def _sensor_action(sensor: ARASSensorDefinition, value: int) -> str:
        name = sensor.device_name.lower()
        kind = sensor.sensor_type.lower()
        if "contact" in kind or any(
            word in name for word in ("cabinet", "cupboard", "door", "drawer", "fridge", "wardrobe")
        ):
            return "OPEN" if value else "CLOSE"
        if "force" in kind or any(word in name for word in ("bed", "chair", "couch", "armchair")):
            return "OCCUPIED" if value else "VACANT"
        if any(word in kind for word in ("ir", "distance", "sonar")):
            return "DETECTED" if value else "CLEARED"
        return "ON" if value else "OFF"

    @staticmethod
    def _infer_location(device_name: str) -> str | None:
        text = device_name.lower()
        mappings = (
            ("kitchen", ("fridge", "kitchen", "tap")),
            ("bathroom", ("bathroom", "shower", "water closet")),
            ("bedroom", ("bed", "wardrobe")),
            ("living_room", ("couch", "tv", "armchair")),
            ("hall", ("hall",)),
            ("entrance", ("house door",)),
        )
        for location, words in mappings:
            if any(word in text for word in words):
                return location
        return None

    @staticmethod
    def _merge_adjacent_annotations(
        annotations: list[ActivityAnnotation],
    ) -> list[ActivityAnnotation]:
        ordered = sorted(annotations, key=lambda item: (item.resident, item.start_time))
        merged: list[ActivityAnnotation] = []
        for annotation in ordered:
            previous = merged[-1] if merged else None
            if (
                previous is not None
                and previous.resident == annotation.resident
                and previous.activity_id == annotation.activity_id
                and previous.end_time == annotation.start_time
            ):
                merged[-1] = previous.model_copy(update={"end_time": annotation.end_time})
            else:
                merged.append(annotation)
        return merged

    @classmethod
    def normalize_house(cls, house: str) -> str:
        normalized = str(house).strip().upper().removeprefix("HOUSE ").strip()
        if normalized not in cls.house_dirs:
            raise ValueError(f"Unsupported ARAS house: {house!r}")
        return normalized


ARASLoader = ARASDataLoader
