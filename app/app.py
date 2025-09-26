from flask import Flask, jsonify
import os


def create_app() -> Flask:
    app = Flask(__name__)

    @app.get("/")
    def index():
        return jsonify({"app": "sample-app", "env": os.getenv("APP_ENV", "local")})

    @app.get("/healthz")
    def healthz():
        return jsonify({"status": "ok"}), 200

    @app.get("/livez")
    def livez():
        return jsonify({"alive": True}), 200

    return app


if __name__ == "__main__":
    port = int(os.getenv("PORT", "8080"))
    create_app().run(host="0.0.0.0", port=port)


