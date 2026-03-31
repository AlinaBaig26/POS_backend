from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from pydantic import ValidationError
from .repository import PurchaseRepository as PR
from app.api.constants import parse_body, purchase_to_dict
from .service import PurchaseService
from .schemas import AddPurchase, UpdatePurchase

purchase_bp = Blueprint("purchases", __name__)
service = PurchaseService()


@purchase_bp.route("/", methods=["GET"])
@jwt_required()
def get_purchase():

    data = request.get_json(silent=True) or {}
    supplier_name = data.get("supplier_name")
    purchase_number = data.get("purchase_number")

    if not supplier_name and not purchase_number:
        return jsonify({"error": "Supplier name or Purchase Number is required"}), 400
    if purchase_number:
        purchase = service.getPurchaseByNumber(purchase_number)
        if purchase:
            return jsonify(purchase_to_dict(purchase)), 200
        else:
            return jsonify({"error": "Purchase not found.", "Purchase Number entered": purchase_number}), 404
        
    if supplier_name:
        purchases = service.getPurchaseBySupplierName(supplier_name)
        if supplier_name:
            return jsonify([purchase_to_dict(purchase)for purchase in purchases]), 200
        else:
            return jsonify({"error": "Purchase not found.", "Name entered": supplier_name}), 404
        
@purchase_bp.route("/all",methods=["GET"])
@jwt_required()
def get_all_purchases():
    purchases = service.getAllPurchases()
    return jsonify([purchase_to_dict(purchase)for purchase in purchases])

@purchase_bp.route("/",methods=["POST"])
@jwt_required()
def add_purchase():
    data = request.get_json(silent=True) or {}
    body, err = parse_body(AddPurchase, data)
    if err:
        return jsonify({"success": False, "errors": err}), 400
    try:
        added = service.addPurchase(body.purchase_number,body.product_sku,body.supplier_name)
        if added:
            return jsonify({"message": "Purchase added", "Purchase Number": body.purchase_number}), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 409

@purchase_bp.route("/",methods=["DELETE"])
@jwt_required()
def delete_purchase():
    data = request.get_json(silent=True) or {}
    purchase_number = data.get("purchase_number")

    if not purchase_number:
        return jsonify({"error": "Purchase number required"}), 400
    
    try:
        deleted = service.deletePurchase(purchase_number)
        
        if deleted:
            return jsonify({"message": "Purchase deleted", "Purchase Number": purchase_number}), 200

    except ValueError as e:
        return jsonify({"error": str(e)}), 404

@purchase_bp.route("/",methods=["PUT"])
@jwt_required()
def update_purchase():

    data = request.get_json(silent=True) or {}

    body, err = parse_body(UpdatePurchase, data)
    if err:
        return jsonify({"success": False, "errors": err}), 400
    if not body.new_purchase_number and not body.new_supplier_name and not body.new_product_sku:
        return jsonify({"error": "Provide at least one of: new_order_number, new_customer_name, new_product_sku"}), 400

    try:
        updated = service.updatePurchase(body.purchase_number, body.new_purchase_number, body.new_supplier_name, body.new_product_sku)
    
        if updated:
            return jsonify({"message": "Purchase updated", "Purchase Number": updated.purchase_number}), 200

    except ValueError as e:
        return jsonify({"error": str(e)}), 404