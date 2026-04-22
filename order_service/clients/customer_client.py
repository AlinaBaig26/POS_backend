import requests
import os

CUSTOMER_SERVICE_URL = os.getenv("CUSTOMER_SERVICE_URL", "http://customer_service:8004")


def get_customer_by_name(customer_name: str, auth_header: str = None):
    headers = {}
    if auth_header:
        headers["Authorization"] = auth_header

    response = requests.get(
        f"{CUSTOMER_SERVICE_URL}/api/customers/{customer_name}",
        headers=headers,
        timeout=5
    )

    if response.status_code != 200:
        return None

    return response.json()