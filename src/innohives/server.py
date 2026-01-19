from __future__ import annotations

import json

import duckdb
from flask import Flask, Response, make_response

DEFAULT_TRENDS_TABLE = "trend_deltas"


def create_app(*, database_path: str, trends_table: str = DEFAULT_TRENDS_TABLE) -> Flask:
    app = Flask(__name__)

    @app.get("/trends")
    def get_trends() -> Response:
        connection = duckdb.connect(database=database_path, read_only=True)
        try:
            rows = connection.execute(
                f"""
                SELECT subject, month_a_label, month_b_label, month_a_count, month_b_count, delta
                FROM {trends_table}
                ORDER BY delta DESC, subject ASC
                """
            ).fetchall()
        except duckdb.CatalogException:
            return Response(
                f"{trends_table} not found\n",
                status=404,
                mimetype="text/plain",
            )
        finally:
            connection.close()

        payload_rows: list[dict[str, int | str]] = []
        for row in rows:
            subject = str(row[0])
            month_a_label = str(row[1])
            month_b_label = str(row[2])
            count_a = int(row[3])
            count_b = int(row[4])
            delta = int(row[5])
            payload_rows.append(
                {
                    "subject": subject,
                    month_a_label: count_a,
                    month_b_label: count_b,
                    "delta": delta,
                }
            )
        payload = json.dumps(payload_rows, indent=2, sort_keys=False, default=int)

        resp = make_response(payload, 200)
        resp.headers["Content-Type"] = "application/json"
        resp.headers["Access-Control-Allow-Origin"] = "http://localhost:5173"  # or "*" for any
        return resp

    return app
