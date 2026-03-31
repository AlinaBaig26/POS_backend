# from flask import Blueprint
from . import api_bp




def register_api_routes(app):

    from app.api.auth.routes import login_bp
    from app.api.product.routes import product_bp
    from app.api.customer.routes import customer_bp
    from app.api.supplier.routes import supplier_bp
    from app.api.purchase.routes import purchase_bp
    from app.api.orders.routes import order_bp
    
    api_bp.register_blueprint(login_bp, url_prefix="/auth")
    api_bp.register_blueprint(product_bp, url_prefix="/products")
    api_bp.register_blueprint(customer_bp, url_prefix="/customers")
    api_bp.register_blueprint(supplier_bp, url_prefix="/suppliers")
    api_bp.register_blueprint(purchase_bp, url_prefix="/purchases")
    api_bp.register_blueprint(order_bp, url_prefix="/orders")

    app.register_blueprint(api_bp)
