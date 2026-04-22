from flask import Blueprint
# from . import api_bp




def register_api_routes(app):
    api_bp = Blueprint("api", __name__, url_prefix="/api")

    from product_app.product_api.product.routes import product_bp
    
    api_bp.register_blueprint(product_bp, url_prefix="/products")

    app.register_blueprint(api_bp)
