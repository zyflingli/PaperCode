from __future__ import annotations

import re
from dataclasses import dataclass
from datetime import datetime, timedelta
from pathlib import Path
from typing import Iterable

import pandas as pd

from src.utils.models import Event


@dataclass(frozen=True)
class ARASSensorDefinition:
    column: int
    sensor_id: str
    sensor_type: str
    place: str


@dataclass(frozen=True)
class ARASMetadata:
    house: str
    sensors: list[ARASSensorDefinition]
    activities: dict[int, str]

    @property
    def sensor_columns(self) -> list[str]:
        return [sensor.sensor_id for sensor in self.sensors]


class ARASDataLoader:
    """Loader for the ARAS smart home dataset.

    ARAS stores dense one-row-per-second files. The primary loading methods
    therefore return DataFrames; ``to_events`` can derive sparse Event objects
    for the rest of this project.
    """

    default_dataset_dir = Path("CPS40/2. ARAS datasets")
    expected_rows_per_day = 86400
    expected_sensor_count = 20
    resident_columns = ["R1", "R2"]
    processed_columns = [
        "activity_id",
        "avg_duration_hours",
        "num_occurrences",
        "num_sensors",
    ]

    house_dirs = {
        "A": "House A",
        "B": "House B",
    }

    def load(
        self,
        dataset_dir: str | Path | None = None,
        *,
        houses: Iterable[str] = ("A", "B"),
        days: Iterable[int] | None = None,
        include_time: bool = True,
        validate: bool = True,
    ) -> pd.DataFrame:
        """Load one or more houses into a single DataFrame."""

        frames = [
            self.load_house(
                dataset_dir,
                house=house,
                days=days,
                include_time=include_time,
                validate=validate,
            )
            for house in houses
        ]
        if not frames:
            return pd.DataFrame()
        return pd.concat(frames, ignore_index=True)

    def load_house(
        self,
        dataset_dir: str | Path | None = None,
        *,
        house: str,
        days: Iterable[int] | None = None,
        include_time: bool = True,
        validate: bool = True,
    ) -> pd.DataFrame:
        """Load all requested day files for one house."""

        day_numbers = list(days) if days is not None else self.available_days(dataset_dir, house)
        frames = [
            self.load_day(
                dataset_dir,
                house=house,
                day=day,
                include_time=include_time,
                validate=validate,
            )
            for day in day_numbers
        ]
        if not frames:
            return pd.DataFrame()
        return pd.concat(frames, ignore_index=True)

    def load_day(
        self,
        dataset_dir: str | Path | None = None,
        *,
        house: str,
        day: int,
        include_time: bool = True,
        validate: bool = True,
    ) -> pd.DataFrame:
        """Load a single ``DAY_n.txt`` file.

        The returned DataFrame contains the 20 house-specific sensor columns,
        ``R1`` and ``R2`` activity ID columns, plus optional derived time fields.
        """

        metadata = self.load_metadata(dataset_dir, house)
        path = self.day_path(dataset_dir, house, day)
        if not path.exists():
            raise FileNotFoundError(f"ARAS day file not found: {path}")

        columns = metadata.sensor_columns + self.resident_columns
        frame = pd.read_csv(path, sep=r"\s+", header=None, names=columns)

        if validate:
            self._validate_day_frame(frame, path)

        if include_time:
            frame.insert(0, "time_of_day", pd.to_timedelta(frame.index, unit="s"))
            frame.insert(0, "second_of_day", frame.index.astype("int64"))
            frame.insert(0, "day", int(day))
            frame.insert(0, "house", self.normalize_house(house))

        return frame

    def load_metadata(
        self,
        dataset_dir: str | Path | None = None,
        house: str = "A",
    ) -> ARASMetadata:
        """Read sensor and activity definitions from the house README."""

        normalized_house = self.normalize_house(house)
        readme_path = self.house_path(dataset_dir, normalized_house) / "README"
        if not readme_path.exists():
            raise FileNotFoundError(f"ARAS README not found: {readme_path}")

        sensors: list[ARASSensorDefinition] = []
        activities: dict[int, str] = {}
        section: str | None = None

        with readme_path.open("r", encoding="utf-8") as handle:
            for raw_line in handle:
                line = raw_line.strip()
                if not line:
                    continue
                upper = line.upper()
                if upper.startswith("SENSOR EXPLANATIONS"):
                    section = "sensors"
                    continue
                if upper.startswith("ACTIVITY EXPLANATIONS"):
                    section = "activities"
                    continue
                if line.lower().startswith("column") or line.lower().startswith("id"):
                    continue

                if section == "sensors":
                    sensor = self._parse_sensor_definition(line)
                    if sensor is not None:
                        sensors.append(sensor)
                elif section == "activities":
                    activity = self._parse_activity_definition(line)
                    if activity is not None:
                        activity_id, activity_name = activity
                        activities[activity_id] = activity_name

        sensors = sorted(sensors, key=lambda sensor: sensor.column)
        if len(sensors) != self.expected_sensor_count:
            raise ValueError(
                f"Expected {self.expected_sensor_count} sensors in {readme_path}, "
                f"found {len(sensors)}"
            )
        if not activities:
            raise ValueError(f"No activity definitions found in {readme_path}")

        return ARASMetadata(
            house=normalized_house,
            sensors=sensors,
            activities=dict(sorted(activities.items())),
        )

    def load_processed_stats(
        self,
        dataset_dir: str | Path | None = None,
        *,
        house: str,
        resident: str,
    ) -> pd.DataFrame:
        """Load derived ``processed_ARAS_R*.txt`` activity statistics."""

        resident_name = self.normalize_resident(resident)
        path = self.house_path(dataset_dir, house) / f"processed_ARAS_{resident_name}.txt"
        if not path.exists():
            raise FileNotFoundError(f"ARAS processed stats file not found: {path}")

        frame = pd.read_csv(
            path,
            sep="\t",
            header=None,
            names=self.processed_columns,
        )
        metadata = self.load_metadata(dataset_dir, house)
        frame.insert(0, "resident", resident_name)
        frame.insert(0, "house", self.normalize_house(house))
        frame["activity_name"] = frame["activity_id"].map(metadata.activities)
        return frame

    def available_days(self, dataset_dir: str | Path | None = None, house: str = "A") -> list[int]:
        """Return sorted day numbers available for a house."""

        house_dir = self.house_path(dataset_dir, house)
        day_numbers = []
        for path in house_dir.glob("DAY_*.txt"):
            match = re.fullmatch(r"DAY_(\d+)\.txt", path.name)
            if match:
                day_numbers.append(int(match.group(1)))
        return sorted(day_numbers)

    def to_events(
        self,
        frame: pd.DataFrame,
        metadata: ARASMetadata,
        *,
        base_date: datetime | None = None,
        sensor_transitions_only: bool = True,
        activity_changes_only: bool = True,
    ) -> list[Event]:
        """Convert loaded ARAS rows to sparse Event objects.

        Sensor events are emitted when a sensor value is 1. With
        ``sensor_transitions_only=True``, only 0 -> 1 transitions are emitted.
        Activity events are emitted when a resident label changes; the first row
        for each house/day/resident is kept as the initial annotation.
        """

        if frame.empty:
            return []

        base = base_date or datetime(2000, 1, 1)
        sensor_by_id = {sensor.sensor_id: sensor for sensor in metadata.sensors}
        sensor_columns = metadata.sensor_columns
        missing = [column for column in sensor_columns + self.resident_columns if column not in frame]
        if missing:
            raise ValueError(f"Frame is missing ARAS columns: {missing}")

        working = self._ensure_time_columns(frame, metadata.house)
        houses_in_frame = {self.normalize_house(house) for house in working["house"].unique()}
        if houses_in_frame != {metadata.house}:
            raise ValueError(
                "Frame house values do not match metadata house: "
                f"frame={sorted(houses_in_frame)}, metadata={metadata.house}"
            )
        events: list[Event] = []

        for _, group in working.groupby(["house", "day"], sort=True):
            group = group.sort_values("second_of_day")
            timestamps = group.apply(
                lambda row: base
                + timedelta(days=int(row["day"]) - 1, seconds=int(row["second_of_day"])),
                axis=1,
            )

            for sensor_id in sensor_columns:
                values = group[sensor_id].astype(int)
                active = values.eq(1)
                if sensor_transitions_only:
                    previous = values.shift(fill_value=0)
                    active = active & previous.eq(0)

                sensor = sensor_by_id[sensor_id]
                for index in group.index[active]:
                    events.append(
                        Event(
                            action="sensor_fired",
                            device=sensor.sensor_id,
                            timestamp=timestamps.loc[index],
                            location=sensor.place,
                            sensor_state={
                                "value": 1,
                                "sensor_type": sensor.sensor_type,
                                "house": metadata.house,
                                "day": int(group.loc[index, "day"]),
                                "second_of_day": int(group.loc[index, "second_of_day"]),
                            },
                        )
                    )

            for resident in self.resident_columns:
                values = group[resident].astype(int)
                changed = values.ne(values.shift())
                if not activity_changes_only:
                    changed = pd.Series(True, index=group.index)

                for index in group.index[changed]:
                    activity_id = int(group.loc[index, resident])
                    events.append(
                        Event(
                            action=self.normalize_name(
                                metadata.activities.get(activity_id, f"activity_{activity_id}")
                            ),
                            device=f"{resident}_activity",
                            timestamp=timestamps.loc[index],
                            location="activity_annotation",
                            sensor_state={
                                "activity_id": activity_id,
                                "activity_name": metadata.activities.get(activity_id),
                                "resident": resident,
                                "house": metadata.house,
                                "day": int(group.loc[index, "day"]),
                                "second_of_day": int(group.loc[index, "second_of_day"]),
                            },
                        )
                    )

        return sorted(events, key=lambda event: event.timestamp)

    def to_frame(self, events: list[Event]) -> pd.DataFrame:
        records = [
            {
                "action": event.action,
                "device": event.device,
                "timestamp": event.timestamp,
                "location": event.location,
                "sensor_state": event.sensor_state or {},
            }
            for event in events
        ]
        return pd.DataFrame(
            records,
            columns=["action", "device", "timestamp", "location", "sensor_state"],
        ).sort_values("timestamp", ignore_index=True)

    def dataset_path(self, dataset_dir: str | Path | None = None) -> Path:
        return Path(dataset_dir) if dataset_dir is not None else self.default_dataset_dir

    def house_path(self, dataset_dir: str | Path | None, house: str) -> Path:
        normalized_house = self.normalize_house(house)
        return self.dataset_path(dataset_dir) / self.house_dirs[normalized_house]

    def day_path(self, dataset_dir: str | Path | None, house: str, day: int) -> Path:
        if day < 1:
            raise ValueError(f"ARAS day must be >= 1, got {day}")
        return self.house_path(dataset_dir, house) / f"DAY_{int(day)}.txt"

    @classmethod
    def normalize_house(cls, house: str) -> str:
        text = str(house).strip().upper()
        if text.startswith("HOUSE "):
            text = text.removeprefix("HOUSE ").strip()
        if text not in cls.house_dirs:
            raise ValueError(f"Unsupported ARAS house {house!r}; expected one of {sorted(cls.house_dirs)}")
        return text

    @staticmethod
    def normalize_resident(resident: str) -> str:
        text = str(resident).strip().upper()
        if text in {"1", "RESIDENT1", "RESIDENT_1", "R1"}:
            return "R1"
        if text in {"2", "RESIDENT2", "RESIDENT_2", "R2"}:
            return "R2"
        raise ValueError(f"Unsupported ARAS resident {resident!r}; expected R1 or R2")

    @staticmethod
    def normalize_name(value: object) -> str:
        text = str(value).strip().strip("'\"").lower()
        text = re.sub(r"[^a-z0-9]+", "_", text)
        text = re.sub(r"_+", "_", text).strip("_")
        return text or "unknown"

    def _validate_day_frame(self, frame: pd.DataFrame, path: Path) -> None:
        if len(frame) != self.expected_rows_per_day:
            raise ValueError(
                f"Expected {self.expected_rows_per_day} rows in {path}, found {len(frame)}"
            )
        expected_columns = self.expected_sensor_count + len(self.resident_columns)
        if len(frame.columns) != expected_columns:
            raise ValueError(f"Expected {expected_columns} columns in {path}, found {len(frame.columns)}")

        sensor_values = frame.iloc[:, : self.expected_sensor_count]
        invalid_sensor_values = ~sensor_values.isin([0, 1])
        if invalid_sensor_values.any().any():
            raise ValueError(f"Sensor columns in {path} contain values outside 0/1")

        resident_values = frame[self.resident_columns]
        invalid_activity_values = ~resident_values.apply(lambda column: column.between(1, 27))
        if invalid_activity_values.any().any():
            raise ValueError(f"Resident activity columns in {path} contain IDs outside 1..27")

    def _ensure_time_columns(self, frame: pd.DataFrame, house: str) -> pd.DataFrame:
        working = frame.copy()
        if "house" not in working:
            working.insert(0, "house", house)
        if "day" not in working:
            working.insert(1, "day", 1)
        if "second_of_day" not in working:
            working.insert(2, "second_of_day", range(len(working)))
        return working

    @staticmethod
    def _parse_sensor_definition(line: str) -> ARASSensorDefinition | None:
        if not re.match(r"^\d+\s+", line):
            return None

        parts = re.split(r"\t+|\s{2,}", line)
        parts = [part.strip() for part in parts if part.strip()]
        if len(parts) < 4:
            return None

        column_text, sensor_id, sensor_type = parts[:3]
        place = " ".join(parts[3:])
        try:
            column = int(column_text)
        except ValueError:
            return None

        return ARASSensorDefinition(
            column=column,
            sensor_id=sensor_id,
            sensor_type=sensor_type,
            place=place,
        )

    @staticmethod
    def _parse_activity_definition(line: str) -> tuple[int, str] | None:
        match = re.match(r"^(\d+)\s+(.+)$", line)
        if not match:
            return None
        return int(match.group(1)), match.group(2).strip()
