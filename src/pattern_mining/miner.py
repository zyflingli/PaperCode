from __future__ import annotations

from collections import Counter, defaultdict
from datetime import datetime
from itertools import combinations
from math import floor
from typing import Any, Iterable

import pandas as pd

try:
    from prefixspan import PrefixSpan
except ImportError:  # pragma: no cover - exercised only when optional dep is absent.
    PrefixSpan = None

from src.utils.models import Pattern, SequencePattern


Record = dict[str, Any]
ContextKey = tuple[tuple[str, Any], ...]


class PatternMiner:
    """Mine single-action, action-set, and sequence patterns from event records."""

    def __init__(
        self,
        *,
        context_fields: Iterable[str] = ("location",),
        min_support: float | int = 0.1,
        max_pattern_length: int = 5,
        transaction_window_seconds: int = 30 * 60,
        session_gap_seconds: int = 30 * 60,
    ) -> None:
        self.context_fields = tuple(context_fields)
        self.min_support = min_support
        self.max_pattern_length = max_pattern_length
        self.transaction_window_seconds = transaction_window_seconds
        self.session_gap_seconds = session_gap_seconds

    def mine(self, events: Any, *, top_k: int = 10) -> dict[str, list[Pattern]]:
        """Return top-K patterns for each category."""

        records = self._normalize_records(events)
        return {
            "single": self.mine_single_action_patterns(records, top_k=top_k),
            "set": self.mine_action_set_patterns(records, top_k=top_k),
            "sequence": self.mine_sequence_patterns(records, top_k=top_k),
        }

    def mine_single_action_patterns(self, events: Any, *, top_k: int = 10) -> list[Pattern]:
        """Mine P(action | context) for every action observed in each context."""

        records = self._normalize_records(events)
        context_totals: Counter[ContextKey] = Counter()
        action_counts: Counter[tuple[ContextKey, str]] = Counter()

        for record in records:
            action = self._action(record)
            if action is None:
                continue
            context_key = self._context_key(record)
            context_totals[context_key] += 1
            action_counts[(context_key, action)] += 1

        patterns = [
            Pattern(
                type="single",
                context=self._context_dict(context_key),
                items=[action],
                support=count / context_totals[context_key],
            )
            for (context_key, action), count in action_counts.items()
            if context_totals[context_key] > 0
        ]
        return self._top_k(patterns, top_k)

    def mine_action_set_patterns(self, events: Any, *, top_k: int = 10) -> list[Pattern]:
        """Mine frequent action itemsets with an Apriori pass per context."""

        records = self._normalize_records(events)
        transactions_by_context = self._transactions_by_context(records)
        patterns: list[Pattern] = []

        for context_key, transactions in transactions_by_context.items():
            support_count = self._support_threshold(len(transactions))
            frequent_itemsets = self._apriori(transactions, support_count)
            for itemset, count in frequent_itemsets.items():
                if len(itemset) < 2:
                    continue
                patterns.append(
                    Pattern(
                        type="set",
                        context=self._context_dict(context_key),
                        items=sorted(itemset),
                        support=count / len(transactions),
                    )
                )

        return self._top_k(patterns, top_k)

    def mine_sequence_patterns(self, events: Any, *, top_k: int = 10) -> list[Pattern]:
        """Mine frequent action sequences using PrefixSpan when available."""

        records = self._normalize_records(events)
        sequences_by_context = self._sequences_by_context(records)
        patterns: list[Pattern] = []

        for context_key, sequences in sequences_by_context.items():
            support_count = self._support_threshold(len(sequences))
            if PrefixSpan is not None:
                raw_patterns = PrefixSpan(sequences).frequent(support_count)
            else:
                raw_patterns = self._contiguous_sequence_counts(sequences, support_count)

            for count, sequence in raw_patterns:
                if not 1 < len(sequence) <= self.max_pattern_length:
                    continue
                patterns.append(
                    Pattern(
                        type="sequence",
                        context=self._context_dict(context_key),
                        items=list(sequence),
                        support=count / len(sequences),
                    )
                )

        return self._top_k(patterns, top_k)

    def _normalize_records(self, events: Any) -> list[Record]:
        if events is None:
            return []
        if isinstance(events, pd.DataFrame):
            return events.to_dict("records")

        records: list[Record] = []
        for event in events:
            if hasattr(event, "model_dump"):
                record = event.model_dump()
            elif hasattr(event, "to_dict"):
                record = event.to_dict()
            elif isinstance(event, dict):
                record = dict(event)
            else:
                record = {
                    "action": getattr(event, "action", None),
                    "device": getattr(event, "device", None),
                    "timestamp": getattr(event, "timestamp", None),
                    "location": getattr(event, "location", None),
                    "resident": getattr(event, "resident", None),
                    "source_dataset": getattr(event, "source_dataset", None),
                }
            records.append(record)

        return sorted(records, key=self._sort_key)

    def _transactions_by_context(self, records: list[Record]) -> dict[ContextKey, list[frozenset[str]]]:
        grouped: dict[tuple[ContextKey, int], set[str]] = defaultdict(set)
        fallback_index = 0

        for record in records:
            action = self._action(record)
            if action is None:
                continue
            context_key = self._context_key(record)
            timestamp = self._timestamp(record)
            if timestamp is None:
                bucket = fallback_index
                fallback_index += 1
            else:
                bucket = floor(timestamp.timestamp() / self.transaction_window_seconds)
            grouped[(context_key, bucket)].add(action)

        transactions_by_context: dict[ContextKey, list[frozenset[str]]] = defaultdict(list)
        for (context_key, _), actions in grouped.items():
            if actions:
                transactions_by_context[context_key].append(frozenset(actions))

        return dict(transactions_by_context)

    def _sequences_by_context(self, records: list[Record]) -> dict[ContextKey, list[list[str]]]:
        grouped: dict[ContextKey, list[tuple[datetime | None, str]]] = defaultdict(list)
        for record in records:
            action = self._action(record)
            if action is not None:
                grouped[self._context_key(record)].append((self._timestamp(record), action))

        sequences_by_context: dict[ContextKey, list[list[str]]] = {}
        for context_key, entries in grouped.items():
            entries = sorted(entries, key=lambda item: item[0] or datetime.min)
            sequences: list[list[str]] = []
            current: list[str] = []
            previous_timestamp: datetime | None = None

            for timestamp, action in entries:
                starts_new_session = (
                    current
                    and timestamp is not None
                    and previous_timestamp is not None
                    and (timestamp - previous_timestamp).total_seconds() > self.session_gap_seconds
                )
                if starts_new_session:
                    sequences.append(current)
                    current = []
                current.append(action)
                previous_timestamp = timestamp

            if current:
                sequences.append(current)
            if sequences:
                sequences_by_context[context_key] = sequences

        return sequences_by_context

    def _apriori(
        self,
        transactions: list[frozenset[str]],
        support_count: int,
    ) -> dict[frozenset[str], int]:
        frequent: dict[frozenset[str], int] = {}
        item_counts: Counter[frozenset[str]] = Counter()
        for transaction in transactions:
            for item in transaction:
                item_counts[frozenset([item])] += 1

        current_level = {
            itemset: count for itemset, count in item_counts.items() if count >= support_count
        }
        frequent.update(current_level)
        size = 2

        while current_level and size <= self.max_pattern_length:
            candidates = self._join_itemsets(current_level.keys(), size)
            if not candidates:
                break

            counts: Counter[frozenset[str]] = Counter()
            for transaction in transactions:
                for candidate in candidates:
                    if candidate.issubset(transaction):
                        counts[candidate] += 1

            current_level = {
                itemset: count for itemset, count in counts.items() if count >= support_count
            }
            frequent.update(current_level)
            size += 1

        return frequent

    @staticmethod
    def _join_itemsets(itemsets: Iterable[frozenset[str]], size: int) -> set[frozenset[str]]:
        items = sorted({item for itemset in itemsets for item in itemset})
        return {frozenset(candidate) for candidate in combinations(items, size)}

    def _contiguous_sequence_counts(
        self,
        sequences: list[list[str]],
        support_count: int,
    ) -> list[tuple[int, list[str]]]:
        counts: Counter[tuple[str, ...]] = Counter()
        for sequence in sequences:
            seen: set[tuple[str, ...]] = set()
            max_length = min(self.max_pattern_length, len(sequence))
            for length in range(2, max_length + 1):
                for start in range(0, len(sequence) - length + 1):
                    seen.add(tuple(sequence[start : start + length]))
            counts.update(seen)

        return [
            (count, list(sequence))
            for sequence, count in counts.items()
            if count >= support_count
        ]

    def _context_key(self, record: Record) -> ContextKey:
        context = {
            field: self._hashable_value(record.get(field, "unknown"))
            for field in self.context_fields
            if record.get(field) is not None
        }
        return tuple(sorted(context.items()))

    @staticmethod
    def _context_dict(context_key: ContextKey) -> dict[str, Any]:
        return dict(context_key)

    @staticmethod
    def _hashable_value(value: Any) -> Any:
        if isinstance(value, (str, int, float, bool, type(None))):
            return value
        return str(value)

    @staticmethod
    def _action(record: Record) -> str | None:
        action = record.get("action")
        if action is None or pd.isna(action):
            return None
        return str(action)

    @staticmethod
    def _timestamp(record: Record) -> datetime | None:
        value = record.get("timestamp")
        if value is None or pd.isna(value):
            return None
        if isinstance(value, datetime):
            return value.replace(tzinfo=None)
        timestamp = pd.to_datetime(value, errors="coerce")
        if pd.isna(timestamp):
            return None
        return timestamp.to_pydatetime().replace(tzinfo=None)

    def _sort_key(self, record: Record) -> tuple[int, datetime]:
        timestamp = self._timestamp(record)
        if timestamp is None:
            return (1, datetime.min)
        return (0, timestamp)

    def _support_threshold(self, total: int) -> int:
        if total <= 0:
            return 1
        if isinstance(self.min_support, float) and self.min_support <= 1:
            return max(1, int(total * self.min_support + 0.999999))
        return max(1, int(self.min_support))

    @staticmethod
    def _top_k(patterns: list[Pattern], top_k: int) -> list[Pattern]:
        ordered = sorted(
            patterns,
            key=lambda pattern: (
                pattern.support,
                len(pattern.items),
                tuple(pattern.items),
                tuple(sorted(pattern.context.items())),
            ),
            reverse=True,
        )
        return ordered[:top_k]


class SequencePatternMiner:
    def __init__(self, min_support: int = 2, max_pattern_length: int = 5) -> None:
        self.min_support = min_support
        self.max_pattern_length = max_pattern_length

    def mine(self, sequences: list[list[str]]) -> list[SequencePattern]:
        if not sequences:
            return []

        if PrefixSpan is None:
            raw_patterns = self._contiguous_sequence_counts(sequences)
        else:
            raw_patterns = PrefixSpan(sequences).frequent(self.min_support)

        patterns: list[SequencePattern] = []
        for support, sequence in raw_patterns:
            if 1 < len(sequence) <= self.max_pattern_length:
                patterns.append(SequencePattern(sequence=sequence, support=support))

        return patterns

    def _contiguous_sequence_counts(self, sequences: list[list[str]]) -> list[tuple[int, list[str]]]:
        counts: Counter[tuple[str, ...]] = Counter()
        for sequence in sequences:
            seen: set[tuple[str, ...]] = set()
            max_length = min(self.max_pattern_length, len(sequence))
            for length in range(2, max_length + 1):
                for start in range(0, len(sequence) - length + 1):
                    seen.add(tuple(sequence[start : start + length]))
            counts.update(seen)
        return [
            (count, list(sequence))
            for sequence, count in counts.items()
            if count >= self.min_support
        ]
