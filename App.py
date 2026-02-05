from flask import Flask, request, jsonify
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity, get_jwt
from flask_cors import CORS

from Auth.Login import login_bp
from Product.Product import product_bp
from Customer.Customer import customer_bp
from Supplier.Supplier import supplier_bp
# from Orders.Order import order_bp


def create_app():
    app = Flask(__name__)

    app.config["JWT_SECRET_KEY"] = "super-secret-key"

    CORS(
        app,
        origins=[
            "http://localhost:5173",   # Vite dev
            "http://localhost:3000",   # React dev,
            "http://192.168.1.146:5000",
            "https://your-frontend.vercel.app"
            
        ],
        supports_credentials=True,
        methods=["GET", "POST", "PUT", "DELETE"],
        allow_headers=["Content-Type", "Authorization"]
    )

    jwt = JWTManager(app)

    app.register_blueprint(login_bp, url_prefix="/auth")
    app.register_blueprint(product_bp, url_prefix="/products")
    app.register_blueprint(customer_bp, url_prefix="/customers")
    app.register_blueprint(supplier_bp, url_prefix="/suppliers")
    # app.register_blueprint(order_bp, url_prefix="/orders")
    

    return app

app = create_app()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80)

    # app.run()