from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
# from .repository import SupplierRepository as SR
from .service import SupplierService
from pydantic import ValidationError
from .schemas import AddSupplier, UpdateSupplier
from supplier_app.supplier_api.constants import parse_body

supplier_bp = Blueprint("suppliers", __name__)
service = SupplierService()

@supplier_bp.route("/<string:name>", methods=["GET"])
def get_supplier(name):

    supplier = service.getSupplierByName(name)
    if supplier:
        return jsonify({
            "id": supplier.id,
            "name": supplier.name,
            "phone": supplier.phone
        }), 200
    else:
        return jsonify({"error": "Supplier not found.", "Name entered": name}), 404
    
@supplier_bp.route("/", methods=["GET"])
def get_all_supplier():
    suppliers = service.getAllSuppliers()
    return jsonify([
        {"Supplier Name": supplier.name , "Contact Info": supplier.phone}
        for supplier in suppliers])

@supplier_bp.route("/", methods=["POST"])
def add_supplier():
    data = request.get_json(silent=True) or {}
    body, error = parse_body(AddSupplier, data)
    if error:
        return jsonify({
            "success": False,
            "message": "Validation failed.",
            "errors": error
        }), 400

    name = body.name
    phone = body.phone

    if not name or not phone:
        return jsonify({"error": "Missing fields"}), 400

    added = service.addSupplier(name, phone)
    if added:
        return jsonify({"message": "Supplier added", "Supplier Name": name}), 201

@supplier_bp.route("/", methods=["DELETE"])
def delete_supplier():

    # name = request.args.get("name")
    data = request.get_json(silent=True) or {}
    name = data.get("name")

    if not name:
        return jsonify({"error": "Supplier name required"}), 400

    deleted = service.deleteSupplier(name)
    
    if deleted:
        return jsonify({"message": "Supplier deleted", "Supplier Name": name}), 200

    else:
        return jsonify({"error": "Supplier not found"}), 404
    
@supplier_bp.route("/", methods=["PUT"])
def update_supplier():

    data = request.get_json(silent=True) or {}
    body, error = parse_body(UpdateSupplier, data)
    if error:
        return jsonify({
            "success": False,
            "message": "Validation failed.",
            "errors": error,
        }), 400

    name = body.name
    phone = body.phone
    new_name = body.new_name

    if not name:
        return jsonify({"error": "Missing fields"}), 400

    updated = service.updateSupplier(name, phone, new_name)
    
    if updated:
        return jsonify({"message": "Supplier updated", "Supplier Name": name}), 200

    else:
        return jsonify({"error": "Supplier not found"}), 404
