from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from .repository import CustomerRepository as CR
from .service import CustomerService
from app.api.constants import parse_body
from .schemas import AddCustomer, UpdateCustomer

customer_bp = Blueprint("customers", __name__)
service = CustomerService()

@customer_bp.route("/<string:name>", methods=["GET"])
@jwt_required()
def getCustomer(name):

    # name = request.args.get("name")
    data = request.get_json(silent=True) or {}
    name = data.get("name")
    if not name:
        return jsonify({"error": "Customer name is required"}), 400
    customer = service.getCustomerByName(name)
    if customer:
        return jsonify({"name": customer.name, "Contact Info": customer.phone}), 200
    else:
        return jsonify({"error": "Customer not found.", "Name entered": name}), 404
    
@customer_bp.route("/", methods=["GET"])
@jwt_required()
def getAllCustomers():
    customers = service.getAllCustomers()
    return jsonify([
        {"Customer Name": customer.name , "Contact Info": customer.phone}
        for customer in customers])

@customer_bp.route("/", methods=["POST"])
@jwt_required()
def addCustomer():
    data = request.get_json(silent=True) or {}
    body, error = parse_body(AddCustomer, data)
    if error:
        return jsonify({
            "success": False,
            "message": "Validation failed.",
            "errors": error,
        }), 400

    name = body.name
    phone = body.phone

    if not name or not phone:
        return jsonify({"error": "Missing fields"}), 400
    try:
        added = service.addCustomer(name, phone)
        if added:
            return jsonify({"message": "Customer added", "Customer Name": name}), 201
    
    except ValueError as e:
        return jsonify({"error": str(e)}), 409

@customer_bp.route("/", methods=["DELETE"])
@jwt_required()
def deleteCustomer():

    # name = request.args.get("name")
    data = request.get_json(silent=True) or {}
    name = data.get("name")

    if not name:
        return jsonify({"error": "Customer name required"}), 400

    deleted = service.deleteCustomer(name)
    
    if deleted:
        return jsonify({"message": "Customer deleted", "Customer Name": name}), 200

    else:
        return jsonify({"error": "Customer not found"}), 404
    
@customer_bp.route("/", methods=["PUT"])
@jwt_required()
def updateCustomer():

    data = request.get_json(silent=True) or {}
    body, error = parse_body(UpdateCustomer, data)
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
        return jsonify({"error": "Customer name is required"}), 400

    updated = service.updateCustomer(name, phone, new_name)
    if updated:
        if new_name == name:
            return jsonify({"message": "Customer updated", "Customer Name": name}), 200
        if not new_name:
            return jsonify({"message": "Customer updated", "Customer Name": name}), 200
        return jsonify({"message": "Customer updated", "Customer Name": new_name}), 200

    else:
        return jsonify({"error": "Customer not found"}), 404
