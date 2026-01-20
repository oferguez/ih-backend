from __future__ import annotations

import logging
from dataclasses import dataclass

import duckdb

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class DuckDBTrendStorage:
    """Stores compared trend deltas in DuckDB."""

    database_path: str

    def replace_trend_deltas(
        self,
        subject_trends: list[dict[str, int | str]],
        *,
        month_a: str,
        month_b: str,
        month_a_label: str,
        month_b_label: str,
    ) -> None:
        connection = duckdb.connect(database=self.database_path, read_only=False)
        try:
            connection.execute("DROP TABLE IF EXISTS trend_deltas")
            connection.execute(
                """
                CREATE TABLE trend_deltas (
                    subject VARCHAR NOT NULL,
                    month_a VARCHAR NOT NULL,
                    month_b VARCHAR NOT NULL,
                    month_a_label VARCHAR NOT NULL,
                    month_b_label VARCHAR NOT NULL,
                    month_a_count INTEGER NOT NULL,
                    month_b_count INTEGER NOT NULL,
                    delta INTEGER NOT NULL,
                    PRIMARY KEY (subject, month_a, month_b)
                )
                """
            )

            delta_rows: list[tuple[str, str, str, str, str, int, int, int]] = []
            for trend in subject_trends:
                subject = str(trend["subject"])
                count_a = int(trend[month_a_label])
                count_b = int(trend[month_b_label])
                delta = int(trend["delta"])
                delta_rows.append(
                    (
                        subject,
                        month_a,
                        month_b,
                        month_a_label,
                        month_b_label,
                        count_a,
                        count_b,
                        delta,
                    )
                )

            if delta_rows:
                batch_size = 5000
                total = len(delta_rows)
                logger.info("About to inserted %d trend delta rows", total)
                for start in range(0, total, batch_size):
                    end = min(start + batch_size, total)
                    connection.executemany(
                        "INSERT INTO trend_deltas VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                        delta_rows[start:end],
                    )
                    logger.info("Inserted %d/%d trend delta rows", end, total)
        finally:
            connection.close()
