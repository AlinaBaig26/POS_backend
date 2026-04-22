from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from pydantic import ValidationError
from .repository import PurchaseRepository as PR
from purchase_app.purchase_api.constants import parse_body, purchase_to_dict
from .service import PurchaseService
from .schemas import AddPurchase, UpdatePurchase

purchase_bp = Blueprint("purchases", __name__)
service = PurchaseService()


@purchase_bp.route("/", methods=["GET"])
def get_purchase():

    supplier_name = request.args.get("supplier_name")
    purchase_number = request.args.get("purchase_number")

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
        if purchases:
            return jsonify([purchase_to_dict(purchase)for purchase in purchases]), 200
        else:
            return jsonify({"error": "Purchase not found.", "Name entered": supplier_name}), 404
        
@purchase_bp.route("/all",methods=["GET"])
def get_all_purchases():
    purchases = service.getAllPurchases()
    return jsonify([purchase_to_dict(purchase)for purchase in purchases])

@purchase_bp.route("/",methods=["POST"])
def add_purchase():
    
    data = request.get_json(silent=True) or {}
    body, err = parse_body(AddPurchase, data)

    if err:
        return jsonify({"success": False, "errors": err}), 400

    auth_header = request.headers.get("Authorization")

    try:
        new_purchase = service.addPurchase(
            body.purchase_number,
            body.product_sku,
            body.supplier_name,
            auth_header
        )
        if new_purchase:
            return jsonify({
                "message": "Purchase added",
                "purchase_number": body.purchase_number
            }), 201

    except ValueError as e:
        msg = str(e)

        if "already exists" in msg:
            return jsonify({"error": msg}), 409
        if "does not exist" in msg:
            return jsonify({"error": msg}), 404

        return jsonify({"error": msg}), 400

@purchase_bp.route("/",methods=["DELETE"])
def delete_purchase():
    data = request.get_json(silent=True) or {}
    purchase_number = data.get("purchase_number")

    if not purchase_number:
        return jsonify({"error": "Purchase number required"}), 400
    
    try:
        deleted = service.deletePurchase(purchase_number)
        
        if deleted:
            return jsonify({"message": "Purchase deleted", "Purchase Number": purchase_number}), 200
        return jsonify({"error": "Purchase not found"}), 404

    except ValueError as e:
        return jsonify({"error": str(e)}), 404

@purchase_bp.route("/",methods=["PUT"])
def update_purchase():

    data = request.get_json(silent=True) or {}

    body, err = parse_body(UpdatePurchase, data)
    if err:
        return jsonify({"success": False, "errors": err}), 400
    
    auth_header = request.headers.get("Authorization")

    try:
        updated = service.updatePurchase(body.purchase_number, body.new_purchase_number, body.new_product_sku, body.new_supplier_name, auth_header)
    
        if updated:
            return jsonify({"message": "Purchase updated", "Purchase Number": updated.purchase_number}), 200

    except ValueError as e:
        msg = str(e)

        if "already exists" in msg:
            return jsonify({"error": msg}), 409
        if "does not exist" in msg:
            return jsonify({"error": msg}), 404

        return jsonify({"error": msg}), 400