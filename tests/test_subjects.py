from __future__ import annotations

from innohives.datasource import InMemoryMessageSource, MessageRow
from sklearn.feature_extraction.text import CountVectorizer

from innohives.subjects import SubjectsAnalyzer


def test_subjects_per_month_groups_and_counts() -> None:
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
        MessageRow(
            message_id=3,
            dt_published="2025-10-01 06:35:42",
            translated_content="Gamma delta epsilon",
            channel_name="chan",
            channel_id=10,
        ),
    )
    source = InMemoryMessageSource(rows=rows)

    vectorizer = CountVectorizer(
        stop_words="english",
        ngram_range=(1, 1),
        min_df=0.0,
        max_df=1.0,
    )
    analyzer = SubjectsAnalyzer(source=source, vectorizer=vectorizer)
    results = analyzer.run()

    assert [result.month for result in results] == ["2025-09", "2025-10"]
    september = results[0].subjects
    october = results[1].subjects

    assert september["alpha"] == 2
    assert september["beta"] == 2
    assert september["gamma"] == 1
    assert september["delta"] == 1
    assert october["gamma"] == 1
    assert october["delta"] == 1
    assert october["epsilon"] == 1
