from flask import Flask
from supplier_app.supplier_api.routes import register_api_routes
from supplier_app.config import Config
from supplier_app.extensions import jwt, cors
from werkzeug.middleware.proxy_fix import ProxyFix


def create_app():
    app = Flask(__name__)

    app.config.from_object(Config)

    app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1)

    jwt.init_app(app)
    cors.init_app(app)

    register_api_routes(app)

    return app


