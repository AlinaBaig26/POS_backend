from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from pydantic import ValidationError
from .repository import OrderRepository as OR
from .service import OrderService
from order_app.order_api.constants import parse_body, order_to_dict
from .schemas import AddOrder, UpdateOrder
# from .schemas import AddCustomer

order_bp = Blueprint("orders", __name__)
service = OrderService()

@order_bp.route("/", methods=["GET"])
def get_order():

    customer_name = request.args.get("customer_name")
    order_number = request.args.get("order_number")
    
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
def get_all_orders():
    orders = service.getAllOrders()
    return jsonify([order_to_dict(order)for order in orders])

@order_bp.route("/",methods=["POST"])
def add_order():
    data = request.get_json(silent=True) or {}
    body, err = parse_body(AddOrder, data)

    if err:
        return jsonify({"success": False, "errors": err}), 400

    auth_header = request.headers.get("Authorization")

    try:
        new_order = service.addOrder(
            body.order_number,
            body.product_sku,
            body.customer_name,
            auth_header
        )
        if new_order:
            return jsonify({
                "message": "Order added",
                "order_number": body.order_number
            }), 201

    except ValueError as e:
        msg = str(e)

        if "already exists" in msg:
            return jsonify({"error": msg}), 409
        if "does not exist" in msg:
            return jsonify({"error": msg}), 404

        return jsonify({"error": msg}), 400

@order_bp.route("/",methods=["DELETE"])
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
def update_order():

    data = request.get_json(silent=True) or {}

    body, err = parse_body(UpdateOrder, data)
    if err:
        return jsonify({"success": False, "errors": err}), 400
    auth_header = request.headers.get("Authorization")

    try:
        updated = service.updateOrder(body.order_number, body.new_order_number, body.new_product_sku, body.new_customer_name, auth_header)
        if updated:
            return jsonify({"message": "Order updated", "order_number": updated.order_number}), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 404