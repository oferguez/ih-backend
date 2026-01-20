from __future__ import annotations

import logging
from dataclasses import dataclass
from datetime import datetime
from typing import Iterable

from .datasource import MessageRow, MessageSource
from .vectorizer import Vectorizer

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class MonthlySubjectsResult:
    """Holds subject frequencies for a single month."""

    month: str
    subjects: dict[str, int]


def _month_key(dt_value: str) -> str:
    parsed = datetime.fromisoformat(dt_value)
    return parsed.strftime("%Y-%m")


@dataclass(frozen=True)
class SubjectsAnalyzer:
    """Analyze subject document frequencies per month.

    Args:
        source: Provides message rows via dependency injection.
        vectorizer: Preconfigured CountVectorizer.
    """

    source: MessageSource
    vectorizer: Vectorizer

    def run(self) -> list[MonthlySubjectsResult]:
        """Compute subject document frequencies per month."""

        grouped = self._group_by_month(self.source.iter_messages())
        logger.info("Grouped messages into %d month buckets", len(grouped))
        results: list[MonthlySubjectsResult] = []
        for month, rows in sorted(grouped.items()):
            logger.info("Processing month %s with %d messages", month, len(rows))
            frequencies = self._doc_frequencies(rows)
            logger.info("Month %s produced %d subjects", month, len(frequencies))
            results.append(MonthlySubjectsResult(month=month, subjects=frequencies))
        return results

    def _group_by_month(self, rows: Iterable[MessageRow]) -> dict[str, list[MessageRow]]:
        grouped: dict[str, list[MessageRow]] = {}
        for row in rows:
            month = _month_key(row.dt_published)
            grouped.setdefault(month, []).append(row)
        return grouped

    def _doc_frequencies(self, rows: list[MessageRow]) -> dict[str, int]:
        documents = [row.translated_content for row in rows]
        if not documents:
            return {}
        matrix = self.vectorizer.fit_transform(documents)
        vocab = self.vectorizer.get_feature_names_out()
        frequencies = (matrix > 0).sum(axis=0).A1
        return dict(zip(vocab, frequencies, strict=True))
