from __future__ import annotations

import json
import logging
from argparse import Namespace

from sklearn.feature_extraction.text import CountVectorizer

from .duckdb_source import DuckDBMessageSource
from .reporting import SubjectDeltaReporter
from .setup import configure_logging
from .subjects import SubjectsAnalyzer
from .trend_storage import DuckDBTrendStorage


class TrendAnalysisRunner:
    """Runs the trend analysis pipeline with injected dependencies."""

    def __init__(
        self,
        *,
        analyzer: SubjectsAnalyzer,
        reporter: SubjectDeltaReporter,
        trend_storage: DuckDBTrendStorage,
        logger: logging.Logger,
        output_path: str = "trends.json",
    ) -> None:
        self._analyzer = analyzer
        self._reporter = reporter
        self._trend_storage = trend_storage
        self._logger = logger
        self._output_path = output_path

    def run(
        self,
        *,
        month_a: str,
        month_b: str,
        month_a_label: str,
        month_b_label: str,
        top_n: int,
        bottom_n: int,
    ) -> None:
        self._logger.info("analysing trends in telegram db")
        results = self._analyzer.run()

        subject_trends = self._reporter.compare(
            results=results,
            month_a=month_a,
            month_b=month_b,
            month_a_label=month_a_label,
            month_b_label=month_b_label,
            top_n=top_n,
            bottom_n=bottom_n,
        )
        self._trend_storage.replace_trend_deltas(
            subject_trends,
            month_a=month_a,
            month_b=month_b,
            month_a_label=month_a_label,
            month_b_label=month_b_label,
        )
        self._logger.info("Saved trends to DuckDB table trend_deltas")
        self._logger.info("%d trends", len(subject_trends))


def run_analysis(args: Namespace) -> None:
    logger = configure_logging(args.log_level)

    months = tuple(dict.fromkeys((args.month_a, args.month_b)))
    source = DuckDBMessageSource(
        database_path=args.database,
        table_name=args.table,
        limit=args.limit,
        months=months,
    )
    vectorizer = CountVectorizer(
        stop_words="english",
        ngram_range=(1, args.ngram_max),
        min_df=args.min_df,
        max_df=args.max_df,
    )
    analyzer = SubjectsAnalyzer(source=source, vectorizer=vectorizer)
    runner = TrendAnalysisRunner(
        analyzer=analyzer,
        reporter=SubjectDeltaReporter(),
        trend_storage=DuckDBTrendStorage(database_path=args.database),
        logger=logger,
    )
    runner.run(
        month_a=args.month_a,
        month_b=args.month_b,
        month_a_label=args.label_a,
        month_b_label=args.label_b,
        top_n=args.top_n,
        bottom_n=args.bottom_n,
    )
