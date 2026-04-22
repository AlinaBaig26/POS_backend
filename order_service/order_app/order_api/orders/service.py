from sqlalchemy.exc import IntegrityError
from .repository import OrderRepository
# from clients.product_client import get_product_by_sku
# from clients.customer_client import get_customer_by_name
from order_app.rpc_client.rpc_client import RpcClient

class OrderService:

    def __init__(self, repo: OrderRepository | None = None):
        self.repo = repo or OrderRepository()
        # self.rpc = RpcClient()

    def getOrdersByCustomerName(self, name: str):
        order = self.repo.getOrdersByCustomerName(name)
        return order
        
  
    def getOrderByNumber(self, order_number: str):
        order = self.repo.getOrderByNumber(order_number)
        return order
        

    def getAllOrders(self):
        orders = self.repo.getAllOrders()
        return orders
        

    def addOrder(self, order_number: str, product_sku: str, customer_name: str, auth_header: str | None):
        existing = self.repo.getOrderByNumber(order_number)
        if existing:
            raise ValueError(f"Order with number {order_number} already exists.")

        rpc = RpcClient()
        try:
            product = rpc.call(
                "product.rpc.queue",
                {"action": "get_product_by_sku", "sku": product_sku}
            )
            if product.get("error"):
                raise ValueError(product["error"])

            customer = rpc.call(
                "customer.rpc.queue",
                {"action": "get_customer_by_name", "name": customer_name}
            )
            if customer.get("error"):
                raise ValueError(customer["error"])

            return self.repo.addOrder(
                order_number=order_number,
                product_id=product["id"],
                product_name=product["name"],
                product_sku=product["sku"],
                product_price=product["price"],
                product_cost=product["cost_price"],
                customer_id=customer["id"],
                customer_name=customer["name"],
                customer_phone=customer["phone"]
            )
        finally:
            try:
                rpc.close()
            except Exception:
                pass

    def deleteOrder(self, order_number: str):
        order = self.repo.deleteOrder(order_number)
        return order

    def updateOrder(self, order_number: str, new_order_number: str, new_product_sku: str, new_customer_name: str, auth_header: str):
        existing = self.repo.getOrderByNumber(order_number)
        if not existing:
            raise ValueError(f"Order with number {order_number} does not exist.")

        updates = {}
        rpc = RpcClient()

        try:
            if new_order_number is not None and new_order_number != existing.order_number:
                updates["order_number"] = new_order_number

            if new_product_sku is not None:
                product = rpc.call(
                    "product.rpc.queue",
                    {"action": "get_product_by_sku", "sku": new_product_sku}
                )
                if product.get("error"):
                    raise ValueError(product["error"])

                updates["product_id"] = product["id"]
                updates["product_name"] = product["name"]
                updates["product_sku"] = product["sku"]
                updates["product_price"] = product["price"]
                updates["product_cost"] = product["cost_price"]

            if new_customer_name is not None:
                customer = rpc.call(
                    "customer.rpc.queue",
                    {"action": "get_customer_by_name", "name": new_customer_name}
                )
                if customer.get("error"):
                    raise ValueError(customer["error"])

                updates["customer_id"] = customer["id"]
                updates["customer_name"] = customer["name"]
                updates["customer_phone"] = customer["phone"]

            if not updates:
                raise ValueError("At least one valid change is required.")

            return self.repo.updateOrder(existing, updates)

        finally:
            try:
                rpc.close()
            except Exception:
                pass