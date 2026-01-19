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


def _group_by_month(rows: Iterable[MessageRow]) -> dict[str, list[str]]:
    grouped: dict[str, list[str]] = {}
    for row in rows:
        month = _month_key(row.dt_published)
        grouped.setdefault(month, []).append(row.translated_content)
    return grouped


def _doc_frequencies(
    documents: list[str],
    min_df: int = 50,
    max_df: float = 0.3,
    ngram_range: tuple[int, int] = (1, 2),
) -> dict[str, int]:
    vectorizer = CountVectorizer(
        stop_words="english",
        ngram_range=ngram_range,
        min_df=min_df,
        max_df=max_df,
    )
    matrix = vectorizer.fit_transform(documents)
    vocab = vectorizer.get_feature_names_out()
    frequencies = (matrix > 0).sum(axis=0).A1
    return dict(zip(vocab, frequencies, strict=True))


def subjects_per_month(
    source: MessageSource,
    min_df: int = 50,
    max_df: float = 0.3,
    ngram_range: tuple[int, int] = (1, 2),
) -> list[MonthlySubjectsResult]:
    """Compute subject document frequencies per month from a message source."""

    grouped = _group_by_month(source.iter_messages())
    results: list[MonthlySubjectsResult] = []
    for month, documents in sorted(grouped.items()):
        frequencies = _doc_frequencies(
            documents,
            min_df=min_df,
            max_df=max_df,
            ngram_range=ngram_range,
        )
        results.append(MonthlySubjectsResult(month=month, subjects=frequencies))
    return results
