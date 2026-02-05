from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from pydantic import ValidationError
from Database.DatabaseOperations import DatabaseOperations as db_ops

customer_bp = Blueprint("customers", __name__)

@customer_bp.route("/<string:name>", methods=["GET"])
@jwt_required()
def get_customer(name):

    # name = request.args.get("name")
    name = request.get_json().get("name")
    if not name:
        return jsonify({"error": "Customer name is required"}), 400
    customer = db_ops.get_customer_by_name(name)
    if customer:
        return jsonify({"name": customer.name, "Contact Info": customer.phone}), 200
    else:
        return jsonify({"error": "Customer not found.", "Name entered": name}), 404
    
@customer_bp.route("/", methods=["GET"])
@jwt_required()
def get_all_customers():
    customers = db_ops.get_all_customers()
    return jsonify([
        {"Customer Name": customer.name , "Contact Info": customer.phone}
        for customer in customers])

@customer_bp.route("/", methods=["POST"])
@jwt_required()
def add_customer():
    data = request.get_json()

    name = data.get("name")
    contact_info = data.get("contact_info")

    if not name or not contact_info:
        return jsonify({"error": "Missing fields"}), 400

    added = db_ops.add_customer(name, contact_info)
    if added:
        return jsonify({"message": "Customer added", "Customer Name": name}), 201

@customer_bp.route("/", methods=["DELETE"])
@jwt_required()
def delete_customer():

    # name = request.args.get("name")
    name = request.get_json().get("name")

    if not name:
        return jsonify({"error": "Customer name required"}), 400

    deleted = db_ops.delete_customer(name)
    
    if deleted:
        return jsonify({"message": "Customer deleted", "Customer Name": name}), 200

    else:
        return jsonify({"error": "Customer not found"}), 404
    
@customer_bp.route("/", methods=["PUT"])
@jwt_required()
def update_customer():

    data = request.get_json()

    name = data.get("name")
    contact_info = data.get("contact_info")
    new_name = data.get("new_name")

    if not name:
        return jsonify({"error": "Missing fields"}), 400

    updated = db_ops.update_customer(name, contact_info, new_name)
    if updated:
        return jsonify({"message": "Customer updated", "Customer Name": name}), 200

    else:
        return jsonify({"error": "Customer not found"}), 404
