from pathlib import Path

import pandas as pd

from src.utils.models import Event


class EventDataLoader:
    required_columns = {"action", "device", "timestamp", "location"}

    def load_csv(self, path: str | Path) -> list[Event]:
        frame = pd.read_csv(path)
        missing = self.required_columns.difference(frame.columns)
        if missing:
            raise ValueError(f"Missing required columns: {sorted(missing)}")

        events: list[Event] = []
        for record in frame.to_dict(orient="records"):
            sensor_state = record.get("sensor_state", {})
            if not isinstance(sensor_state, dict):
                sensor_state = {"raw": sensor_state}
            events.append(
                Event(
                    action=record["action"],
                    device=record["device"],
                    timestamp=pd.to_datetime(record["timestamp"]).to_pydatetime(),
                    location=record["location"],
                    sensor_state=sensor_state,
                )
            )
        return events
