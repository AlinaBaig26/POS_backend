from flask import Blueprint
# from . import api_bp




def register_api_routes(app):
    api_bp = Blueprint("api", __name__, url_prefix="/api")

    from order_app.order_api.orders.routes import order_bp
    
    api_bp.register_blueprint(order_bp, url_prefix="/orders")

    app.register_blueprint(api_bp)
