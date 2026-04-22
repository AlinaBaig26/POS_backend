from flask import Blueprint
# from . import api_bp




def register_api_routes(app):
    api_bp = Blueprint("api", __name__, url_prefix="/api")

    from customer_app.customer_api.customer.routes import customer_bp
    
    api_bp.register_blueprint(customer_bp, url_prefix="/customers")

    app.register_blueprint(api_bp)
