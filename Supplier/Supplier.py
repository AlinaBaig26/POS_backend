from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from Database.DatabaseOperations import DatabaseOperations as db_ops

supplier_bp = Blueprint("suppliers", __name__)

@supplier_bp.route("/<string:name>", methods=["GET"])
@jwt_required()
def get_supplier(name):

    # name = request.args.get("name")
    name = request.get_json().get("name")
    if not name:
        return jsonify({"error": "Supplier name is required"}), 400
    supplier = db_ops.get_supplier_by_name(name)
    if supplier:
        return jsonify({"name": supplier.name, "contact_info": supplier.contact_info}), 200
    else:
        return jsonify({"error": "Supplier not found.", "Name entered": name}), 404
    
@supplier_bp.route("/", methods=["GET"])
@jwt_required()
def get_all_supplier():
    suppliers = db_ops.get_all_suppliers()
    return jsonify([
        {"Supplier Name": supplier.name , "Contact Info": supplier.contact_info}
        for supplier in suppliers])

@supplier_bp.route("/", methods=["POST"])
@jwt_required()
def add_supplier():
    data = request.get_json()

    name = data.get("name")
    contact_info = data.get("contact_info")

    if not name or not contact_info:
        return jsonify({"error": "Missing fields"}), 400

    added = db_ops.add_supplier(name, contact_info)
    if added:
        return jsonify({"message": "Supplier added", "Supplier Name": name}), 201

@supplier_bp.route("/", methods=["DELETE"])
@jwt_required()
def delete_supplier():

    # name = request.args.get("name")
    name = request.get_json().get("name")

    if not name:
        return jsonify({"error": "Supplier name required"}), 400

    deleted = db_ops.delete_supplier(name)
    
    if deleted:
        return jsonify({"message": "Supplier deleted", "Supplier Name": name}), 200

    else:
        return jsonify({"error": "Supplier not found"}), 404
    
@supplier_bp.route("/", methods=["PUT"])
@jwt_required()
def update_supplier():

    data = request.get_json()

    name = data.get("name")
    contact_info = data.get("contact_info")
    new_name = data.get("new_name")

    if not name:
        return jsonify({"error": "Missing fields"}), 400

    updated = db_ops.update_supplier(name, contact_info, new_name)
    
    if updated:
        return jsonify({"message": "Supplier updated", "Supplier Name": name}), 200

    else:
        return jsonify({"error": "Supplier not found"}), 404
