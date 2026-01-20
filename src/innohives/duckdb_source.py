from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

import duckdb

from .datasource import MessageRow, MessageSource


@dataclass(frozen=True)
class DuckDBMessageSource(MessageSource):
    """Reads messages from a DuckDB table as a message source."""

    database_path: str
    table_name: str
    limit: int | None = None
    months: tuple[str, ...] | None = None

    def iter_messages(self) -> Iterable[MessageRow]:
        query = (
            "SELECT id, dt_published, translated_content, channel_name, channel_id "
            f"FROM {self.table_name}"
        )
        params: list[object] = []
        if self.months:
            placeholders = ", ".join("?" for _ in self.months)
            query += (
                " WHERE strftime(dt_published, '%Y-%m') "
                f"IN ({placeholders})"
            )
            params.extend(self.months)
        if self.limit is not None:
            query += " LIMIT ?"
            params.append(self.limit)

        connection = duckdb.connect(database=self.database_path, read_only=True)
        try:
            if params:
                rows = connection.execute(query, params).fetchall()
            else:
                rows = connection.execute(query).fetchall()
        finally:
            connection.close()

        for row in rows:
            yield MessageRow(
                message_id=int(row[0]),
                dt_published=str(row[1]),
                translated_content=str(row[2]),
                channel_name=str(row[3]),
                channel_id=int(row[4]),
            )
