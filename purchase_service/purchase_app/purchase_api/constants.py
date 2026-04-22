from pydantic import ValidationError

def parse_body(model, data):

    try:
        return model.model_validate(data), None

    except ValidationError as e:
        return None, e.errors()
    
def purchase_to_dict(purchase):
    return {
        "Purchase Number": purchase.purchase_number,
        "Product Details": {
            "ID": purchase.product_id,
            "Name": purchase.product_name,
            "SKU": purchase.product_sku,
            "Price": purchase.product_price,
            "Cost Price": purchase.product_cost,
        },
        "Supplier Details": {
            "ID": purchase.supplier_id,
            "Name": purchase.supplier_name,
            "Contact": purchase.supplier_phone,
        },
    }