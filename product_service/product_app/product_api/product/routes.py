from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from pydantic import ValidationError
from .repository import ProductRepository as PR
from .service import ProductService
from product_app.product_api.constants import parse_body
from .schemas import AddProduct, UpdateProduct

product_bp = Blueprint("products", __name__)
service = ProductService()

@product_bp.route("/sku/<string:product_sku>", methods=["GET"])
def getProductBySku(product_sku):
    product = service.getProductBySku(product_sku)

    if not product:
        return jsonify({"error": "Product not found"}), 404

    return jsonify({
        "id": product.id,
        "name": product.name,
        "description": product.description,
        "sku": product.sku,
        "price": product.price,
        "cost_price": product.cost_price
    }), 200

@product_bp.route("/<string:sku>", methods=["GET"])
def getProduct(sku):

    # name = request.args.get("name")
    
    data = request.get_json(silent=True) or {}
    sku = data.get("sku")
    if not sku:
        return jsonify({"error": "Product sku is required"}), 400
    product = service.getProductBySku(sku)
    if product:
        return jsonify({"name": product.name, "description": product.description, "sku": product.sku, "Price": product.price, "Cost Price": product.cost_price}), 200
    else:
        return jsonify({"error": "Product not found.", "sku entered": sku}), 404

@product_bp.route("/", methods=["GET"])
def getAllProducts():
    products = service.getAllProducts()
    return jsonify([
        {"Product Name": product.name , "Description": product.description, "sku": product.sku, "Price": product.price, "Cost Price": product.cost_price}
        for product in products])

@product_bp.route("/", methods=["POST"])
def addProduct():

    data = request.get_json(silent=True) or {}
    body, error = parse_body(AddProduct, data)
    if error:
        return jsonify({
            "success": False,
            "message": "Validation failed.",
            "errors": error
        }), 400

    name = body.name
    description = body.description
    sku = body.sku
    price = body.price
    cost_price = body.cost_price

    if not name or not sku:
        return jsonify({"error": "Missing fields"}), 400
    try:
        added = service.addProduct(name, description, sku, price, cost_price)
        if added:
            return jsonify({"message": "Product added", "Product Name": name, "Product sku": sku}), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 409

@product_bp.route("/", methods=["DELETE"])
def deleteProduct():

    # name = request.args.get("name")
    data = request.get_json(silent=True) or {}
    sku = data.get("sku")

    if not sku:
        return jsonify({"error": "Product sku required"}), 400

    deleted = service.deleteProduct(sku)
    
    if deleted:
        return jsonify({"message": "Product deleted", "Product sku": sku}), 200

    else:
        return jsonify({"error": "Product not found"}), 404
    
@product_bp.route("/", methods=["PUT"])
def updateProduct():

    data = request.get_json(silent=True) or {}
    body, error = parse_body(UpdateProduct, data)
    if error:
        return jsonify({
            "success": False,
            "message": "Validation failed.",
            "errors": error,
        }), 400

    sku = body.sku
    name = body.name
    description = body.description
    price = body.price
    cost_price = body.cost_price
    new_sku = body.new_sku

    if not sku:
        return jsonify({"error": "Product sku required"}), 400

    updated = service.updateProduct(sku, name, description, price, cost_price, new_sku)
    
    if updated:
        return jsonify({"message": "Product updated", "Product sku": sku}), 200

    else:
        return jsonify({"error": "Product not found"}), 404
