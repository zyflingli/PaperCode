from __future__ import annotations

import re
from datetime import datetime
from pathlib import Path

from src.data.models import ActivityAnnotation, SensorEvent


class KasterenDataLoader:
    """Load van Kasteren sensors and evaluation labels through separate APIs."""

    default_dataset_dir = Path("CPS40/3. kasterenDataset")
    sensor_filename = "kasterenSenseData.txt"
    annotation_filename = "kasterenActData.txt"

    device_locations = {
        "microwave": "kitchen",
        "hall_toilet_door": "hall",
        "hall_bathroom_door": "hall",
        "cups_cupboard": "kitchen",
        "fridge": "kitchen",
        "plates_cupboard": "kitchen",
        "frontdoor": "entrance",
        "dishwasher": "kitchen",
        "toiletflush": "toilet",
        "freezer": "kitchen",
        "pans_cupboard": "kitchen",
        "washingmachine": "bathroom",
        "groceries_cupboard": "kitchen",
        "hall_bedroom_door": "hall",
    }
    contact_devices = {
        "hall_toilet_door",
        "hall_bathroom_door",
        "cups_cupboard",
        "fridge",
        "plates_cupboard",
        "frontdoor",
        "freezer",
        "pans_cupboard",
        "groceries_cupboard",
        "hall_bedroom_door",
    }

    def __init__(
        self,
        dataset_dir: str | Path | None = None,
        *,
        house: str | None = None,
        resident: str = "resident_1",
    ) -> None:
        self.dataset_dir = Path(dataset_dir) if dataset_dir is not None else self.default_dataset_dir
        self.house = house
        self.resident = resident

    def load_sensor_events(self, path: str | Path | None = None) -> list[SensorEvent]:
        """Return sensor state transitions only (both interval start and end)."""

        source = Path(path) if path is not None else self.dataset_dir / self.sensor_filename
        rows, labels = self._read_table(source, expected_columns=4)
        events: list[SensorEvent] = []
        for start_text, end_text, device_id, raw_value in rows:
            start = self._parse_timestamp(start_text)
            end = self._parse_timestamp(end_text)
            if start is None:
                continue
            value = self._numeric_value(raw_value)
            normalized_id = device_id.strip()
            raw_name = labels.get(normalized_id, f"sensor_{normalized_id or 'unknown'}")
            device_name = self._normalize_name(raw_name)
            sensor_type = self._sensor_type(device_name)
            events.append(self._sensor_event(start, normalized_id, device_name, sensor_type, value))
            if end is not None and end > start:
                events.append(self._sensor_event(end, normalized_id, device_name, sensor_type, 0))
        return sorted(events, key=lambda event: event.timestamp)

    def load_activity_annotations(
        self, path: str | Path | None = None
    ) -> list[ActivityAnnotation]:
        """Return ground-truth intervals; these are never added to sensor events."""

        source = Path(path) if path is not None else self.dataset_dir / self.annotation_filename
        rows, labels = self._read_table(source, expected_columns=3)
        annotations: list[ActivityAnnotation] = []
        for start_text, end_text, activity_id_text in rows:
            start = self._parse_timestamp(start_text)
            end = self._parse_timestamp(end_text)
            if start is None or end is None or end <= start:
                continue
            activity_id = int(activity_id_text.strip())
            activity_name = labels.get(str(activity_id), f"activity_{activity_id}").strip()
            annotations.append(
                ActivityAnnotation(
                    start_time=start,
                    end_time=end,
                    activity_id=activity_id,
                    activity_name=activity_name,
                    resident=self.resident,
                    dataset="KASTEREN",
                    house=self.house,
                )
            )
        return sorted(annotations, key=lambda annotation: annotation.start_time)

    def _sensor_event(
        self,
        timestamp: datetime,
        device_id: str,
        device_name: str,
        sensor_type: str,
        value: int | float | None,
    ) -> SensorEvent:
        active = value is not None and value != 0
        if sensor_type == "contact":
            action = "OPEN" if active else "CLOSE"
        elif sensor_type == "presence":
            action = "DETECTED" if active else "CLEARED"
        else:
            action = "ON" if active else "OFF"
        return SensorEvent(
            timestamp=timestamp,
            dataset="KASTEREN",
            house=self.house,
            device_id=device_id or "unknown",
            device_name=device_name,
            sensor_type=sensor_type,
            location=self.device_locations.get(device_name),
            action=action,
            value=value,
        )

    def _sensor_type(self, device_name: str) -> str:
        if device_name in self.contact_devices:
            return "contact"
        if device_name == "toiletflush":
            return "presence"
        return "switch"

    @staticmethod
    def _read_table(path: Path, *, expected_columns: int) -> tuple[list[list[str]], dict[str, str]]:
        if not path.exists():
            raise FileNotFoundError(f"Kasteren data file not found: {path}")
        labels: dict[str, str] = {}
        rows: list[list[str]] = []
        in_table = False
        with path.open("r", encoding="latin-1") as handle:
            for raw_line in handle:
                line = raw_line.rstrip("\r\n")
                stripped = line.strip()
                if not stripped:
                    continue
                label = KasterenDataLoader._parse_label(stripped)
                if label is not None:
                    labels[label[0]] = label[1]
                compact = stripped.replace("\t", "").replace(" ", "")
                if compact and set(compact) == {"-"}:
                    in_table = True
                    continue
                if not in_table or stripped.lower().startswith("start time"):
                    continue
                parts = [part.strip() for part in line.split("\t")]
                if len(parts) >= expected_columns:
                    rows.append(parts[:expected_columns])
        return rows, labels

    @staticmethod
    def _parse_label(line: str) -> tuple[str, str] | None:
        match = re.match(r"(?:\[\s*)?(\d+)(?:\s*\])?\s*:?\s*['\"](.+?)['\"]", line)
        return (match.group(1), match.group(2)) if match else None

    @staticmethod
    def _parse_timestamp(value: str) -> datetime | None:
        try:
            return datetime.strptime(value.strip(), "%d-%b-%Y %H:%M:%S")
        except ValueError:
            return None

    @staticmethod
    def _numeric_value(value: str) -> int | float | None:
        text = value.strip()
        if not text:
            return None
        number = float(text)
        return int(number) if number.is_integer() else number

    @staticmethod
    def _normalize_name(value: str) -> str:
        text = re.sub(r"[^a-z0-9]+", "_", value.strip().lower())
        return re.sub(r"_+", "_", text).strip("_") or "unknown"


KasterenLoader = KasterenDataLoader
