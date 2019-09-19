from flask import Flask
from app.controllers import ping
from app.controllers import certificate_manager

def create_app():
    app = Flask(__name__)
    # accepts both /endpoint and /endpoint/ as valid URLs
    app.url_map.strict_slashes = False

    app.register_blueprint(ping.bp, url_prefix="/ping")
    app.register_blueprint(certificate_manager.bp, url_prefix="/api/v1/ca_manager")


    return app
