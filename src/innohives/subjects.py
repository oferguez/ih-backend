from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Iterable

from sklearn.feature_extraction.text import CountVectorizer

from .datasource import MessageRow, MessageSource


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
        vectorizer: Preconfigured CountVectorizer. When omitted, a default one is built.
        min_df: Minimum document frequency within a month to keep a term.
        max_df: Maximum document frequency (fraction) within a month to keep a term.
        ngram_range: Inclusive n-gram sizes to consider (e.g., (1, 2) for uni/bi-grams).
    """

    source: MessageSource
    vectorizer: CountVectorizer | None = None
    min_df: float = 0.0
    max_df: float = 1.0
    ngram_range: tuple[int, int] = (1, 2)

    def __post_init__(self) -> None:
        if self.vectorizer is None:
            vectorizer = CountVectorizer(
                stop_words="english",
                ngram_range=self.ngram_range,
                min_df=self.min_df,
                max_df=self.max_df,
            )
            object.__setattr__(self, "vectorizer", vectorizer)

    def run(self) -> list[MonthlySubjectsResult]:
        """Compute subject document frequencies per month."""

        grouped = self._group_by_month(self.source.iter_messages())
        results: list[MonthlySubjectsResult] = []
        for month, documents in sorted(grouped.items()):
            frequencies = self._doc_frequencies(documents)
            results.append(MonthlySubjectsResult(month=month, subjects=frequencies))
        return results

    def _group_by_month(self, rows: Iterable[MessageRow]) -> dict[str, list[str]]:
        grouped: dict[str, list[str]] = {}
        for row in rows:
            month = _month_key(row.dt_published)
            grouped.setdefault(month, []).append(row.translated_content)
        return grouped

    def _doc_frequencies(self, documents: list[str]) -> dict[str, int]:
        vectorizer = self.vectorizer
        if vectorizer is None:
            raise ValueError("CountVectorizer is not configured.")
        matrix = vectorizer.fit_transform(documents)
        vocab = vectorizer.get_feature_names_out()
        frequencies = (matrix > 0).sum(axis=0).A1
        return dict(zip(vocab, frequencies, strict=True))
