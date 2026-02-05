from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from pydantic import ValidationError
from Database.DatabaseOperations import DatabaseOperations as db_ops

product_bp = Blueprint("products", __name__)

def parse_body(model, contacts):

    try:
        return model.model_validate(contacts), None
    
    except ValidationError as e:
        return None, e.errors()

@product_bp.route("/<string:sku>", methods=["GET"])
@jwt_required()
def get_product(sku):

    # name = request.args.get("name")
    sku = request.get_json().get("sku")
    if not sku:
        return jsonify({"error": "Product SKU is required"}), 400
    product = db_ops.get_product_by_sku(sku)
    if product:
        return jsonify({"name": product.name, "description": product.description, "SKU": product.SKU, "Price": product.price, "Cost Price": product.cost_price}), 200
    else:
        return jsonify({"error": "Product not found.", "SKU entered": sku}), 404

@product_bp.route("/", methods=["GET"])
@jwt_required()
def get_all_products():
    products = db_ops.get_all_products()
    return jsonify([
        {"Product Name": product.name , "Description": product.description, "SKU": product.SKU, "Price": product.price, "Cost Price": product.cost_price}
        for product in products])

@product_bp.route("/", methods=["POST"])
@jwt_required()
def add_product():

    data = request.get_json()

    name = data.get("name")
    description = data.get("description")
    sku = data.get("sku")
    price = data.get("price")
    cost_price = data.get("cost_price")

    if not name or not sku:
        return jsonify({"error": "Missing fields"}), 400

    added = db_ops.add_product(name, description, sku, price, cost_price)
    if added:
        return jsonify({"message": "Product added", "Product Name": name, "Product SKU": sku}), 201

@product_bp.route("/", methods=["DELETE"])
@jwt_required()
def delete_product():

    # name = request.args.get("name")
    sku = request.get_json().get("sku")

    if not sku:
        return jsonify({"error": "Product sku required"}), 400

    deleted = db_ops.delete_product(sku)
    
    if deleted:
        return jsonify({"message": "Product deleted", "Product sku": sku}), 200

    else:
        return jsonify({"error": "Product not found"}), 404
    
@product_bp.route("/", methods=["PUT"])
@jwt_required()
def update_product():

    data = request.get_json()

    sku = data.get("sku")
    name = data.get("name")
    description = data.get("description")
    price = data.get("price")
    cost_price = data.get("cost_price")
    new_sku = data.get("new_sku")

    if not sku:
        return jsonify({"error": "Product SKU required"}), 400

    updated = db_ops.update_product(sku, name, description, price, cost_price, new_sku)
    
    if updated:
        return jsonify({"message": "Product updated", "Product SKU": sku}), 200

    else:
        return jsonify({"error": "Product not found"}), 404
