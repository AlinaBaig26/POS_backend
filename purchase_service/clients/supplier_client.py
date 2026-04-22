import requests
import os

SUPPLIER_SERVICE_URL = os.getenv("SUPPLIER_SERVICE_URL", "http://supplier_service:8003")


def get_supplier_by_name(supplier_name: str, auth_header: str = None):
    headers = {}
    if auth_header:
        headers["Authorization"] = auth_header

    response = requests.get(
        f"{SUPPLIER_SERVICE_URL}/api/suppliers/{supplier_name}",
        headers=headers,
        timeout=5
    )

    if response.status_code != 200:
        return None

    return response.json()