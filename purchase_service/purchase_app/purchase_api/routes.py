from flask import Blueprint
# from . import api_bp




def register_api_routes(app):
    api_bp = Blueprint("api", __name__, url_prefix="/api")

    from purchase_app.purchase_api.purchase.routes import purchase_bp
    
    api_bp.register_blueprint(purchase_bp, url_prefix="/purchases")

    app.register_blueprint(api_bp)
