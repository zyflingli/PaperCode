from collections import defaultdict

from src.data.models import SensorEvent


class EventProcessor:
    def sort_events(self, events: list[SensorEvent]) -> list[SensorEvent]:
        self._validate(events)
        return sorted(events, key=lambda event: event.timestamp)

    def to_device_action_sequences(self, events: list[SensorEvent]) -> list[list[str]]:
        grouped: dict[str, list[SensorEvent]] = defaultdict(list)
        for event in self.sort_events(events):
            grouped[event.location or "unknown"].append(event)

        return [
            [f"{event.device_id}:{event.action}" for event in location_events]
            for location_events in grouped.values()
            if location_events
        ]

    @staticmethod
    def _validate(events: list[SensorEvent]) -> None:
        for index, event in enumerate(events):
            if type(event) is not SensorEvent:
                raise TypeError(f"events[{index}] must be a SensorEvent")
