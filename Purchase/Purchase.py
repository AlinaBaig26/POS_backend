from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from pydantic import ValidationError
from Database.DatabaseOperations import DatabaseOperations as db_ops

purchase_bp = Blueprint("purchases", __name__)

def parse_body(model, contacts):

    try:
        return model.model_validate(contacts), None
    
    except ValidationError as e:
        return None, e.errors()

@purchase_bp.route("/<string:name>", methods=["GET"])
@jwt_required()
def get_purchase(name):

    name = request.get_json().get("name")
    purchase_number = request.get_json().get("purchase_number")
    if not name and not purchase_number:
        return jsonify({"error": "Supplier name or Purchase Number is required"}), 400
    if purchase_number:
        purchase = db_ops.get_purchase_by_number(purchase_number)
        if purchase:
            return jsonify({
                "Purchase Number": purchase.purchase_number,
                "product details": {
                    "name": purchase.product.name,
                    "description": purchase.product.description,
                    "SKU": purchase.product.SKU,
                    "Price": purchase.product.price
                }, 
                "Supplier details": {
                    "Name": purchase.supplier.name,
                    "Contact": purchase.supplier.contact_info
                }}), 200
        else:
            return jsonify({"error": "Purchase not found.", "Purchase Number entered": purchase_number}), 404
        
    if name:
        purchases = db_ops.get_purchase_by_supplier_name(name)
        if name:
            return jsonify([{
                "Purchase Number": purchase.order_number,
                "product details": {
                    "Name": purchase.product.name,
                    "Description": purchase.product.description,
                    "SKU": purchase.product.SKU,
                    "Price": purchase.product.price,
                    "Cost Price": purchase.product.cost_price
                },
                "Supplier details": {
                    "Name": purchase.supplier.name,
                    "Contact": purchase.supplier.contact_info
                }
                }for purchase in purchases]), 200
        else:
            return jsonify({"error": "Purchase not found.", "Name entered": name}), 404
        
@purchase_bp.route("/",methods=["GET"])
@jwt_required()
def get_all_purchases():
    purchases = db_ops.get_all_purchases()
    return jsonify([{
        "Purchase Number": purchase.purchase_number,
        "Product Details": {
            "Name": purchase.product.name,
            "Description": purchase.product.description,
            "SKU": purchase.product.SKU,
            "Price": purchase.product.price,
            "Cost Price": purchase.product.cost_price
        },
        "Supplier Details": {
            "Name": purchase.supplier.name,
            "Contact": purchase.supplier.contact_info
        }
        }for purchase in purchases])

@purchase_bp.route("/",methods=["POST"])
@jwt_required()
def add_purchase():
    data = request.get_json()
    purchase_number = data.get("purchase_number")
    supplier_name = data.get("supplier_name")
    product_sku = data.get("product_sku")

    if not purchase_number or not supplier_name or not product_sku:
        return jsonify({"error": "Missing fields"}), 400
    
    added = db_ops.add_purchase(purchase_number,product_sku,supplier_name)
    if added:
        return jsonify({"message": "Purchase added", "Purchase Number": purchase_number}), 201
    
    return jsonify({"error": "Failed to add purchase"}), 400

@purchase_bp.route("/",methods=["DELETE"])
@jwt_required()
def delete_purchase():
    purchase_number = request.get_json().get("purchase_number")

    if not purchase_number:
        return jsonify({"error": "Purchase number required"}), 400
    
    deleted = db_ops.delete_purchase(purchase_number)
    
    if deleted:
        return jsonify({"message": "Purchase deleted", "Purchase Number": purchase_number}), 200

    else:
        return jsonify({"error": "Purchase not found"}), 404

@purchase_bp.route("/",methods=["PUT"])
@jwt_required()
def update_purchase():

    data = request.get_json()

    purchase_number = data.get("purchase_number")
    new_supplier_name = data.get("new_customer_name")
    new_product_sku = data.get("new_product_sku")
    new_purchase_number = data.get("new_purchase_number")

    if not purchase_number:
        return jsonify({"error": "Missing fields"}), 400

    updated = db_ops.update_purchase(purchase_number, new_purchase_number, new_supplier_name, new_product_sku)
    
    if updated:
        if not new_purchase_number:
            new_purchase_number = purchase_number
        return jsonify({"message": "Purchase updated", "Purchase Number": new_purchase_number}), 200

    else:
        return jsonify({"error": "Purchase not found"}), 404