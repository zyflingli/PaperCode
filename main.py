from datetime import datetime, timezone

from src.event_processor.processor import EventProcessor
from src.pattern_mining.miner import SequencePatternMiner
from src.rule_generation.generator import TAPRuleGenerator
from src.utils.models import Event


def main() -> None:
    events = [
        Event(
            action="motion_detected",
            device="motion_sensor",
            timestamp=datetime.now(timezone.utc),
            location="living_room",
            sensor_state={"motion": True},
        ),
        Event(
            action="turn_on",
            device="light",
            timestamp=datetime.now(timezone.utc),
            location="living_room",
            sensor_state={"brightness": 80},
        ),
    ]

    processor = EventProcessor()
    sequences = processor.to_device_action_sequences(events)

    miner = SequencePatternMiner(min_support=1)
    patterns = miner.mine(sequences)

    generator = TAPRuleGenerator()
    rules = generator.from_patterns(patterns)

    for rule in rules:
        print(rule.model_dump())


if __name__ == "__main__":
    main()
