from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from pydantic import ValidationError
from Database.DatabaseOperations import DatabaseOperations as db_ops

order_bp = Blueprint("orders", __name__)

def parse_body(model, contacts):

    try:
        return model.model_validate(contacts), None
    
    except ValidationError as e:
        return None, e.errors()

@order_bp.route("/<string:name>", methods=["GET"])
@jwt_required()
def get_order(name):

    name = request.get_json().get("name")
    order_number = request.get_json().get("order_number")
    if not name and not order_number:
        return jsonify({"error": "Customer name or Order Number is required"}), 400
    if order_number:
        order = db_ops.get_order_by_number(order_number)
        if order:
            return jsonify({
                "Order Number": order.order_number,
                "product details": {
                    "name": order.product.name,
                    "description": order.product.description,
                    "SKU": order.product.SKU,
                    "Price": order.product.price
                }, 
                "Customer details": {
                    "name": order.customer.name,
                    "contact_info": order.customer.phone
                }}), 200
        else:
            return jsonify({"error": "Order not found.", "Order Number entered": order_number}), 404
        
    if name:
        orders = db_ops.get_orders_by_customer_name(name)
        if name:
            return jsonify([{
                "Order Number": order.order_number,
                "product details": {
                    "Product Name": order.product.name,
                    "Product Description": order.product.description,
                    "SKU": order.product.SKU,
                    "Price": order.product.price,
                    "Cost Price": order.product.cost_price
                },
                "Customer Name": {
                    "Customer Name": order.customer.name,
                    "Customer Contact": order.customer.phone
                }
                }for order in orders]), 200
        else:
            return jsonify({"error": "Order not found.", "Name entered": name}), 404
        
@order_bp.route("/",methods=["GET"])
@jwt_required
def get_all_orders():
    orders = db_ops.get_all_orders()
    return jsonify([{
        "Order Number": order.order_number,
        "Product Details": {
            "Product Name": order.product.name,
            "Product Description": order.product.description,
            "Product SKU": order.product.SKU,
            "Price": order.product.price,
            "Cost Price": order.product.cost_price
        },
        "Customer Details": {
            "Customer Name": order.customer.name,
            "Customer Contact": order.customer.phone
        }
        }for order in orders])

@order_bp.route("/",methods=["POST"])
@jwt_required
def add_order():
    data = request.get_json()
    order_number = data.get("order_number")
    customer_name = data.get("customer_name")
    product_sku = data.get("product_sku")

    if not order_number or not customer_name or not product_sku:
        return jsonify({"error": "Missing fields"}), 400
    
    added = db_ops.add_order(order_number,customer_name,product_sku)
    if added:
        return jsonify({"message": "Order added", "Order Number": order_number}), 201

@order_bp.route("/",methods=["DELETE"])
@jwt_required
def delete_order():
    order_number = request.get_json().get("order_number")

    if not order_number:
        return jsonify({"error": "Order number required"}), 400

@order_bp.route("/",methods=["PUT"])
@jwt_required
def update_order():

    data = request.get_json()

    order_number = data.get("order_number")
    new_customer_name = data.get("new_customer_name")
    new_product_sku = data.get("new_product_sku")
    new_order_number = data.get("new_order_number")

    if not order_number:
        return jsonify({"error": "Missing fields"}), 400

    updated = db_ops.update_order(order_number, new_customer_name, new_product_sku, new_order_number)
    
    if updated:
        return jsonify({"message": "Order updated", "Order Number": new_order_number}), 200

    else:
        return jsonify({"error": "Order not found"}), 404