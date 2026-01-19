from __future__ import annotations

import json
from argparse import Namespace

from sklearn.feature_extraction.text import CountVectorizer

from .duckdb_source import DuckDBMessageSource
from .reporting import SubjectDeltaReporter
from .setup import configure_logging
from .subjects import SubjectsAnalyzer


def run_analysis(args: Namespace) -> None:
    logger = configure_logging(args.log_level)
    logger.info("analysing trends in telegram db")

    source = DuckDBMessageSource(
        database_path=args.database,
        table_name=args.table,
        limit=args.limit,
    )
    vectorizer = CountVectorizer(
        stop_words="english",
        ngram_range=(1, args.ngram_max),
        min_df=args.min_df,
        max_df=args.max_df,
    )
    analyzer = SubjectsAnalyzer(source=source, vectorizer=vectorizer)
    results = analyzer.run()

    reporter = SubjectDeltaReporter()
    subject_trends = reporter.compare(
        results=results,
        month_a=args.month_a,
        month_b=args.month_b,
        month_a_label=args.label_a,
        month_b_label=args.label_b,
        top_n=args.top_n,
        bottom_n=args.bottom_n,
    )
    logger.info("%d trends", len(subject_trends))
    output_payload = json.dumps(subject_trends, indent=2, sort_keys=False, default=int)
    with open("trends.json", "w", encoding="utf-8") as outfile:
        outfile.write(output_payload)
    logger.info("Saved trends to trends.json")
