from pydantic import ValidationError

def parse_body(model, data):

    try:
        return model.model_validate(data), None

    except ValidationError as e:
        return None, e.errors()
    
def order_to_dict(order):
    return {
        "Order Number": order.order_number,
        "Product Details": {
            "Name": order.product.name,
            "Description": order.product.description,
            "SKU": order.product.SKU,
            "Price": order.product.price,
            "Cost Price": getattr(order.product, "cost_price", None),
        },
        "Customer Details": {
            "Name": order.customer.name,
            "Contact": order.customer.phone,
        },
    }

def purchase_to_dict(purchase):
    return {
        "Purchase Number": purchase.purchase_number,
        "Product Details": {
            "Name": purchase.product.name,
            "Description": purchase.product.description,
            "SKU": purchase.product.SKU,
            "Price": purchase.product.price,
            "Cost Price": getattr(purchase.product, "cost_price", None),
        },
        "Supplier Details": {
            "Name": purchase.supplier.name,
            "Contact": purchase.supplier.contact_info,
        },
    }