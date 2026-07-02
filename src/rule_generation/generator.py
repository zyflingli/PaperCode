from src.utils.models import SequencePattern, TAPRule


class TAPRuleGenerator:
    def from_patterns(self, patterns: list[SequencePattern]) -> list[TAPRule]:
        rules: list[TAPRule] = []
        for pattern in patterns:
            trigger = pattern.sequence[0]
            action = pattern.sequence[-1]
            condition = " AND ".join(pattern.sequence[1:-1]) or None
            rules.append(
                TAPRule(
                    trigger=trigger,
                    condition=condition,
                    action=action,
                    source_pattern=pattern.sequence,
                )
            )
        return rules
