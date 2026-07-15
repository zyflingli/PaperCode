from datetime import datetime, timezone

from src.event_processor.processor import EventProcessor
from src.pattern_mining.miner import SequencePatternMiner
from src.rule_generation.generator import TAPRuleGenerator
from src.data.models import SensorEvent


def main() -> None:
    events = [
        SensorEvent(
            action="DETECTED",
            device_id="motion_sensor",
            device_name="Motion Sensor",
            timestamp=datetime.now(timezone.utc),
            dataset="demo",
            location="living_room",
            sensor_type="motion",
            value=1,
        ),
        SensorEvent(
            action="ON",
            device_id="light",
            device_name="Light",
            timestamp=datetime.now(timezone.utc),
            dataset="demo",
            location="living_room",
            sensor_type="switch",
            value=1,
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
