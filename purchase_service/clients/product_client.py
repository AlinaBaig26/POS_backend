import requests
import os

PRODUCT_SERVICE_URL = os.getenv("PRODUCT_SERVICE_URL", "http://product_service:8002")


def get_product_by_sku(product_sku: str, auth_header: str):
    headers = {}
    if auth_header:
        headers["Authorization"] = auth_header

    response = requests.get(
        f"{PRODUCT_SERVICE_URL}/api/products/sku/{product_sku}",
        headers=headers,
        timeout=5
    )

    if response.status_code != 200:
        return None

    return response.json()