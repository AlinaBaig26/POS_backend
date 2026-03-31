from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from pydantic import ValidationError
from .repository import OrderRepository as OR
from .service import OrderService
from app.api.constants import parse_body, order_to_dict
from .schemas import AddOrder, UpdateOrder
# from .schemas import AddCustomer

order_bp = Blueprint("orders", __name__)
service = OrderService()

@order_bp.route("/", methods=["GET"])
@jwt_required()
def get_order():

    data = request.get_json(silent=True) or {}
    customer_name = data.get("customer_name")
    order_number = data.get("order_number")
    
    if not customer_name and not order_number:
        return jsonify({"error": "Customer name or Order Number is required"}), 400
    if order_number:
        order = service.getOrderByNumber(order_number)
        if order:
            return jsonify(order_to_dict(order)), 200
        else:
            return jsonify({"error": "Order not found.", "Order Number entered": order_number}), 404
        
    if customer_name:
        orders = service.getOrdersByCustomerName(customer_name)
        if orders:
            return jsonify([order_to_dict(order)for order in orders]), 200
        else:
            return jsonify({"error": "Order not found.", "Name entered": customer_name}), 404
        
@order_bp.route("/all",methods=["GET"])
@jwt_required()
def get_all_orders():
    orders = service.getAllOrders()
    return jsonify([order_to_dict(order)for order in orders])

@order_bp.route("/",methods=["POST"])
@jwt_required()
def add_order():
    data = request.get_json(silent=True) or {}
    body, err = parse_body(AddOrder, data)
    if err:
        return jsonify({"success": False, "errors": err}), 400

    try:
        service.addOrder(body.order_number, body.product_sku, body.customer_name)
        return jsonify({"message": "Order added", "order_number": body.order_number}), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 409

@order_bp.route("/",methods=["DELETE"])
@jwt_required()
def delete_order():
    data = request.get_json(silent=True) or {}
    order_number = data.get("order_number")

    if not order_number:
        return jsonify({"error": "Order number required"}), 400
    
    try:
        deleted = service.deleteOrder(order_number)
        if deleted:
            return jsonify({"message": "Order deleted", "Order Number": order_number}), 200
        return jsonify({"error": "Order not found"}), 404

    except ValueError as e:
        return jsonify({"error": str(e)}), 404

@order_bp.route("/",methods=["PUT"])
@jwt_required()
def update_order():

    data = request.get_json(silent=True) or {}

    body, err = parse_body(UpdateOrder, data)
    if err:
        return jsonify({"success": False, "errors": err}), 400
    if not body.new_order_number and not body.new_customer_name and not body.new_product_sku:
        return jsonify({"error": "Provide at least one of: new_order_number, new_customer_name, new_product_sku"}), 400

    try:
        updated = service.updateOrder(
            body.order_number,
            body.new_order_number,
            body.new_customer_name,
            body.new_product_sku,
        )
        return jsonify({"message": "Order updated", "order_number": updated.order_number}), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 404