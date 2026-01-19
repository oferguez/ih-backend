from __future__ import annotations

from flask import Flask, Response


def create_app() -> Flask:
    app = Flask(__name__)

    @app.get("/trends")
    def get_trends() -> Response:
        try:
            with open("trends.json", "r", encoding="utf-8") as infile:
                payload = infile.read()
        except FileNotFoundError:
            return Response("trends.json not found\n", status=404, mimetype="text/plain")

        return Response(payload, status=200, mimetype="application/json")

    return app
