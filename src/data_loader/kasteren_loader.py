from __future__ import annotations

import re
from pathlib import Path
from typing import Any

import pandas as pd

from src.utils.models import Event, UnifiedEvent


class KasterenDataLoader:
    """Loader for the van Kasteren smart home dataset text files."""

    default_sensor_file = "kasterenSenseData.txt"
    default_activity_file = "kasterenActData.txt"

    activity_locations = {
        "leave_house": "outside",
        "use_toilet": "toilet",
        "take_shower": "bathroom",
        "go_to_bed": "bedroom",
        "prepare_breakfast": "kitchen",
        "prepare_dinner": "kitchen",
        "get_drink": "kitchen",
    }

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

    def load(
        self,
        dataset_dir: str | Path,
        *,
        include_activities: bool = True,
    ) -> tuple[pd.DataFrame, list[Event]]:
        """Load Kasteren sensor events and optional activity annotations.

        Returns a timestamp-sorted DataFrame and the equivalent list of Event
        objects. Sensor rows become ``sensor_fired`` events; activity rows use
        the normalized activity label as the action.
        """

        dataset_path = Path(dataset_dir)
        sensor_path = dataset_path / self.default_sensor_file
        activity_path = dataset_path / self.default_activity_file

        events = self.load_sensor_events(sensor_path)
        if include_activities and activity_path.exists():
            events.extend(self.load_activity_events(activity_path))

        events = sorted(events, key=lambda event: event.timestamp)
        return self.to_frame(events), events

    def load_sensor_events(self, path: str | Path) -> list[Event]:
        rows, labels = self._read_event_rows(path, expected_columns=4)
        events: list[Event] = []

        for row in rows:
            start_time, end_time, sensor_id, value = self._pad_row(row, 4)
            timestamp = self._parse_timestamp(start_time)
            if pd.isna(timestamp):
                continue

            normalized_id = self._clean_scalar(sensor_id)
            raw_device = labels.get(normalized_id) or f"sensor_{normalized_id or 'unknown'}"
            device = self.normalize_name(raw_device)
            location = self.device_locations.get(device, "unknown")

            events.append(
                Event(
                    action="sensor_fired",
                    device=device,
                    timestamp=timestamp.to_pydatetime(),
                    location=location,
                    sensor_state={
                        "value": self._coerce_value(value),
                        "end_time": self._parse_optional_datetime(end_time),
                        "sensor_id": normalized_id or None,
                        "source": "sensor",
                    },
                )
            )

        return sorted(events, key=lambda event: event.timestamp)

    def load_activity_events(self, path: str | Path) -> list[Event]:
        rows, labels = self._read_event_rows(path, expected_columns=3)
        events: list[Event] = []

        for row in rows:
            start_time, end_time, activity_id = self._pad_row(row, 3)
            timestamp = self._parse_timestamp(start_time)
            if pd.isna(timestamp):
                continue

            normalized_id = self._clean_scalar(activity_id)
            raw_action = labels.get(normalized_id) or f"activity_{normalized_id or 'unknown'}"
            action = self.normalize_name(raw_action)

            events.append(
                Event(
                    action=action,
                    device="activity_annotation",
                    timestamp=timestamp.to_pydatetime(),
                    location=self.activity_locations.get(action, "unknown"),
                    sensor_state={
                        "end_time": self._parse_optional_datetime(end_time),
                        "activity_id": normalized_id or None,
                        "source": "activity",
                    },
                )
            )

        return sorted(events, key=lambda event: event.timestamp)

    def to_frame(self, events: list[Event]) -> pd.DataFrame:
        records = []
        for event in events:
            records.append(
                {
                    "action": event.action,
                    "device": event.device,
                    "timestamp": event.timestamp,
                    "location": event.location or "unknown",
                    "sensor_state": event.sensor_state or {},
                }
            )

        return pd.DataFrame(
            records,
            columns=["action", "device", "timestamp", "location", "sensor_state"],
        ).sort_values("timestamp", ignore_index=True)

    def to_unified_events(
        self,
        events: list[Event] | None = None,
        *,
        dataset_dir: str | Path | None = None,
        include_activities: bool = True,
    ) -> list[UnifiedEvent]:
        """Convert Kasteren events to the cross-dataset UnifiedEvent format.

        Provide ``dataset_dir`` to convert the raw Kasteren files directly.
        Passing preloaded ``events`` is kept as a compatibility path for callers
        that already use ``load``.
        """

        if dataset_dir is not None:
            dataset_path = Path(dataset_dir)
            unified_events = self.load_sensor_unified_events(dataset_path / self.default_sensor_file)
            activity_path = dataset_path / self.default_activity_file
            if include_activities and activity_path.exists():
                unified_events.extend(self.load_activity_unified_events(activity_path))
            return sorted(unified_events, key=lambda event: event.timestamp)

        if events is None:
            raise ValueError("Either dataset_dir or events must be provided")

        unified_events = [
            UnifiedEvent(
                timestamp=event.timestamp,
                device=self._unified_device(event),
                location=self._title_location(event.location),
                action=self._unified_action(event),
                value=self._unified_value(event),
                resident=None,
                source_dataset="KASTEREN",
            )
            for event in events
        ]
        return sorted(unified_events, key=lambda event: event.timestamp)

    def load_sensor_unified_events(self, path: str | Path) -> list[UnifiedEvent]:
        rows, labels = self._read_event_rows(path, expected_columns=4)
        events: list[UnifiedEvent] = []

        for row in rows:
            start_time, _, sensor_id, value = self._pad_row(row, 4)
            timestamp = self._parse_timestamp(start_time)
            if pd.isna(timestamp):
                continue

            normalized_id = self._clean_scalar(sensor_id)
            raw_device = labels.get(normalized_id) or f"sensor_{normalized_id or 'unknown'}"
            device = self._title_name(raw_device)
            normalized_device = self.normalize_name(raw_device)
            coerced_value = self._coerce_value(value)

            events.append(
                UnifiedEvent(
                    timestamp=timestamp.to_pydatetime(),
                    device=device,
                    location=self._title_location(
                        self.device_locations.get(normalized_device, "unknown")
                    ),
                    action=self._sensor_action(coerced_value),
                    value=coerced_value,
                    resident=None,
                    source_dataset="KASTEREN",
                )
            )

        return sorted(events, key=lambda event: event.timestamp)

    def load_activity_unified_events(self, path: str | Path) -> list[UnifiedEvent]:
        rows, labels = self._read_event_rows(path, expected_columns=3)
        events: list[UnifiedEvent] = []

        for row in rows:
            start_time, _, activity_id = self._pad_row(row, 3)
            timestamp = self._parse_timestamp(start_time)
            if pd.isna(timestamp):
                continue

            normalized_id = self._clean_scalar(activity_id)
            raw_action = labels.get(normalized_id) or f"activity_{normalized_id or 'unknown'}"
            action = self.normalize_name(raw_action)

            events.append(
                UnifiedEvent(
                    timestamp=timestamp.to_pydatetime(),
                    device="Activity Annotation",
                    location=self._title_location(self.activity_locations.get(action, "unknown")),
                    action=self._activity_action(action),
                    value=self._coerce_activity_id(normalized_id),
                    resident=None,
                    source_dataset="KASTEREN",
                )
            )

        return sorted(events, key=lambda event: event.timestamp)

    @staticmethod
    def normalize_name(value: Any) -> str:
        text = str(value).strip().strip("'\"").lower()
        text = re.sub(r"[^a-z0-9]+", "_", text)
        text = re.sub(r"_+", "_", text).strip("_")
        return text or "unknown"

    @staticmethod
    def _title_location(value: str | None) -> str:
        text = str(value or "unknown").replace("_", " ").strip()
        return text.title() if text else "Unknown"

    @staticmethod
    def _activity_action(action: str) -> str:
        text = re.sub(r"[^A-Za-z0-9]+", "_", action.strip().upper())
        return re.sub(r"_+", "_", text).strip("_") or "UNKNOWN"

    @staticmethod
    def _title_name(value: str | None) -> str:
        text = str(value or "unknown").replace("_", " ").strip()
        return text.title() if text else "Unknown"

    @staticmethod
    def _sensor_action(value: Any) -> str:
        if value == 1:
            return "ON"
        if value == 0:
            return "OFF"
        return "SENSOR_FIRED"

    @staticmethod
    def _coerce_activity_id(value: Any) -> int | str | None:
        if value is None or value == "":
            return None
        try:
            return int(value)
        except (TypeError, ValueError):
            return str(value)

    @staticmethod
    def _unified_device(event: Event) -> str:
        sensor_state = event.sensor_state or {}
        if sensor_state.get("source") == "activity":
            return "Activity Annotation"
        return KasterenDataLoader._title_name(event.device)

    def _unified_action(self, event: Event) -> str:
        sensor_state = event.sensor_state or {}
        if sensor_state.get("source") == "activity":
            return self._activity_action(event.action)

        return self._sensor_action(self._unified_value(event))

    @staticmethod
    def _unified_value(event: Event) -> Any:
        sensor_state = event.sensor_state or {}
        if sensor_state.get("source") == "activity":
            activity_id = sensor_state.get("activity_id")
            try:
                return int(activity_id)
            except (TypeError, ValueError):
                return activity_id
        return sensor_state.get("value")

    def _read_event_rows(
        self,
        path: str | Path,
        *,
        expected_columns: int,
    ) -> tuple[list[list[str]], dict[str, str]]:
        labels: dict[str, str] = {}
        rows: list[list[str]] = []
        in_table = False

        with Path(path).open("r", encoding="latin-1") as handle:
            for raw_line in handle:
                line = raw_line.rstrip("\n")
                stripped = line.strip()
                if not stripped:
                    continue

                labels.update(self._parse_label_line(stripped))

                if set(stripped.replace("\t", "").replace(" ", "")) == {"-"}:
                    in_table = True
                    continue
                if not in_table:
                    continue
                if stripped.lower().startswith("start time"):
                    continue

                parts = [part.strip() for part in line.split("\t")]
                if len(parts) >= expected_columns:
                    rows.append(parts[:expected_columns])

        return rows, labels

    @staticmethod
    def _parse_label_line(line: str) -> dict[str, str]:
        bracket_match = re.match(r"\[\s*(\d+)\]\s+['\"](.+?)['\"]", line)
        if bracket_match:
            return {bracket_match.group(1): bracket_match.group(2)}

        colon_match = re.match(r"(\d+)\s*:\s*['\"](.+?)['\"]", line)
        if colon_match:
            return {colon_match.group(1): colon_match.group(2)}

        return {}

    @staticmethod
    def _pad_row(row: list[str], size: int) -> list[str]:
        return (row + [""] * size)[:size]

    @staticmethod
    def _clean_scalar(value: Any) -> str:
        if value is None or pd.isna(value):
            return ""
        return str(value).strip()

    @staticmethod
    def _parse_timestamp(value: Any) -> pd.Timestamp:
        return pd.to_datetime(value, format="%d-%b-%Y %H:%M:%S", errors="coerce")

    def _parse_optional_datetime(self, value: Any) -> str | None:
        timestamp = self._parse_timestamp(value)
        if pd.isna(timestamp):
            return None
        return timestamp.isoformat()

    @staticmethod
    def _coerce_value(value: Any) -> int | float | str | None:
        text = str(value).strip()
        if not text:
            return None
        numeric = pd.to_numeric(text, errors="coerce")
        if pd.isna(numeric):
            return text
        if float(numeric).is_integer():
            return int(numeric)
        return float(numeric)


KasterenLoader = KasterenDataLoader
