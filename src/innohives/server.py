from __future__ import annotations

from flask import Flask, Response, make_response

def create_app() -> Flask:
    app = Flask(__name__)

    @app.get("/trends")
    def get_trends() -> Response:
        try:
            with open("trends.json", "r", encoding="utf-8") as infile:
                payload = infile.read()
        except FileNotFoundError:
            return Response("trends.json not found\n", status=404, mimetype="text/plain")

        resp = make_response(payload, 200)
        resp.headers["Content-Type"] = "application/json"
        resp.headers["Access-Control-Allow-Origin"] = "http://localhost:5173"  # or "*" for any
        return resp

    return app
