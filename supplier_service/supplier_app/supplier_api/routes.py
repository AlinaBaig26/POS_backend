from flask import Blueprint
# from . import api_bp




def register_api_routes(app):
    api_bp = Blueprint("api", __name__, url_prefix="/api")

    from supplier_app.supplier_api.supplier.routes import supplier_bp
    
    api_bp.register_blueprint(supplier_bp, url_prefix="/suppliers")

    app.register_blueprint(api_bp)
