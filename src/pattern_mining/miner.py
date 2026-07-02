from prefixspan import PrefixSpan

from src.utils.models import SequencePattern


class SequencePatternMiner:
    def __init__(self, min_support: int = 2, max_pattern_length: int = 5) -> None:
        self.min_support = min_support
        self.max_pattern_length = max_pattern_length

    def mine(self, sequences: list[list[str]]) -> list[SequencePattern]:
        if not sequences:
            return []

        prefix_span = PrefixSpan(sequences)
        raw_patterns = prefix_span.frequent(self.min_support)

        patterns: list[SequencePattern] = []
        for support, sequence in raw_patterns:
            if 1 < len(sequence) <= self.max_pattern_length:
                patterns.append(SequencePattern(sequence=sequence, support=support))

        return patterns
