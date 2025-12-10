from __future__ import annotations

from flask import Flask
from flask_restful import Api

from .resources.routes import register_routes


def create_app() -> Flask:
    app = Flask(__name__)
    api = Api(app)

    @app.get("/healthcheck")
    def healthcheck():
        return {"status": "ok"}

    register_routes(api)
    return app
