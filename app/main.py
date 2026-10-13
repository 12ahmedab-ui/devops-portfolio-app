"""A small Flask web app used to demonstrate a DevOps CI/CD pipeline."""

import os
import platform
from datetime import datetime, timezone

from flask import Flask, jsonify

APP_VERSION = os.getenv("APP_VERSION", "dev")


def create_app() -> Flask:
    app = Flask(__name__)

    @app.get("/")
    def index():
        return jsonify(message="Hello from the DevOps portfolio app!", version=APP_VERSION)

    @app.get("/health")
    def health():
        # Used by Docker HEALTHCHECK, the pipeline smoke test and load balancers.
        return jsonify(status="ok"), 200

    @app.get("/api/info")
    def info():
        return jsonify(
            version=APP_VERSION,
            python=platform.python_version(),
            hostname=platform.node(),
            time_utc=datetime.now(timezone.utc).isoformat(),
        )

    return app


app = create_app()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", "5000")))
