from collections import defaultdict

from src.utils.models import SequencePattern


class PatternClusterer:
    def by_trigger_device(
        self,
        patterns: list[SequencePattern],
    ) -> dict[str, list[SequencePattern]]:
        clusters: dict[str, list[SequencePattern]] = defaultdict(list)
        for pattern in patterns:
            trigger = pattern.sequence[0]
            device = trigger.split(":", maxsplit=1)[0]
            clusters[device].append(pattern)
        return dict(clusters)
