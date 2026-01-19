from __future__ import annotations

import argparse
import logging


def build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Analyze subject changes by month.")
    parser.add_argument(
        "--database",
        default="data/telegram.duckdb",
        help="Path to DuckDB database file.",
    )
    parser.add_argument(
        "--table",
        default="telegram",
        help="Table name containing message rows.",
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=100,
        help="Maximum number of rows to read.",
    )
    parser.add_argument(
        "--month-a",
        default="2025-09",
        help="Month A in YYYY-MM format.",
    )
    parser.add_argument(
        "--month-b",
        default="2025-12",
        help="Month B in YYYY-MM format.",
    )
    parser.add_argument(
        "--label-a",
        default="sept",
        help="Label to use for Month A in output JSON.",
    )
    parser.add_argument(
        "--label-b",
        default="dec",
        help="Label to use for Month B in output JSON.",
    )
    parser.add_argument(
        "--min-df",
        type=float,
        default=0.0,
        help="Minimum document frequency (fraction or count).",
    )
    parser.add_argument(
        "--max-df",
        type=float,
        default=1.0,
        help="Maximum document frequency (fraction).",
    )
    parser.add_argument(
        "--ngram-max",
        type=int,
        default=2,
        help="Maximum n-gram size (minimum is fixed at 1).",
    )
    parser.add_argument(
        "--top-n",
        type=int,
        default=10,
        help="Number of highest delta subjects to include.",
    )
    parser.add_argument(
        "--bottom-n",
        type=int,
        default=10,
        help="Number of lowest delta subjects to include.",
    )
    parser.add_argument(
        "--log-level",
        default="DEBUG",
        help="Logging level (e.g., DEBUG, INFO).",
    )
    return parser


def configure_logging(level: str) -> logging.Logger:
    logging.basicConfig(level=level.upper(), format="%(message)s")
    return logging.getLogger(__name__)
