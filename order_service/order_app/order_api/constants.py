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
            "ID": order.product_id,
            "Name": order.product_name,
            "SKU": order.product_sku,
            "Price": order.product_price,
            "Cost Price": order.product_cost,
        },
        "Customer Details": {
            "ID": order.customer_id,
            "Name": order.customer_name,
            "Contact": order.customer_phone,
        },
    }
