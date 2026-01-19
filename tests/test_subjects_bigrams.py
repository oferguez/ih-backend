from __future__ import annotations

from innohives.datasource import InMemoryMessageSource, MessageRow
from sklearn.feature_extraction.text import CountVectorizer

from innohives.subjects import SubjectsAnalyzer


def test_subjects_per_month_includes_bigrams() -> None:
    rows = (
        MessageRow(
            message_id=1,
            dt_published="2025-09-03 06:35:42",
            translated_content="Alpha beta gamma",
            channel_name="chan",
            channel_id=10,
        ),
        MessageRow(
            message_id=2,
            dt_published="2025-09-15 12:35:42",
            translated_content="Alpha beta delta",
            channel_name="chan",
            channel_id=10,
        ),
    )
    source = InMemoryMessageSource(rows=rows)

    vectorizer = CountVectorizer(
        stop_words="english",
        ngram_range=(1, 2),
        min_df=0.0,
        max_df=1.0,
    )
    analyzer = SubjectsAnalyzer(source=source, vectorizer=vectorizer)
    results = analyzer.run()

    september = results[0].subjects
    assert september["alpha beta"] == 2
    assert september["beta gamma"] == 1
    assert september["beta delta"] == 1
