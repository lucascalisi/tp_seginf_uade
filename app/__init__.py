from flask import Flask
from app.controllers import ping


def create_app():
    app = Flask(__name__)
    # accepts both /endpoint and /endpoint/ as valid URLs
    app.url_map.strict_slashes = False

    app.register_blueprint(ping.bp, url_prefix="/ping")

    return app
