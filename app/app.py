from flask import Flask
from app.api.routes import register_api_routes
from app.config import Config
from app.extensions import jwt, cors


def create_app():
    app = Flask(__name__)

    app.config.from_object(Config)

    jwt.init_app(app)
    cors.init_app(app)

    register_api_routes(app)

    return app
