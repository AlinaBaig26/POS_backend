from flask import Blueprint
# from . import api_bp




def register_api_routes(app):
    api_bp = Blueprint("api", __name__, url_prefix="/api")

    from auth_app.auth_api.auth.routes import auth_bp
    
    api_bp.register_blueprint(auth_bp, url_prefix="/auth")

    app.register_blueprint(api_bp)
