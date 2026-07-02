from collections import defaultdict

from src.utils.models import Event


class EventProcessor:
    def sort_events(self, events: list[Event]) -> list[Event]:
        return sorted(events, key=lambda event: event.timestamp)

    def to_device_action_sequences(self, events: list[Event]) -> list[list[str]]:
        grouped: dict[str, list[Event]] = defaultdict(list)
        for event in self.sort_events(events):
            grouped[event.location].append(event)

        return [
            [f"{event.device}:{event.action}" for event in location_events]
            for location_events in grouped.values()
            if location_events
        ]
