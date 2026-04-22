from sqlalchemy.exc import IntegrityError
from purchase_app.purchase_database.session import getSession
from .repository import PurchaseRepository
# from clients.product_client import get_product_by_sku
# from clients.supplier_client import get_supplier_by_name
from purchase_app.rpc_client.rpc_client import RpcClient

class PurchaseService:

    def __init__(self, repo: PurchaseRepository | None = None):
        self.repo = repo or PurchaseRepository()
        # self.rpc = RpcClient()

    def getPurchaseBySupplierName(self, name: str):
        purchase = self.repo.getPurchaseBySupplierName(name)
        return purchase
        
  
    def getPurchaseByNumber(self, purchase_number: str):
        purchase = self.repo.getPurchaseByNumber(purchase_number)
        return purchase
        

    def getAllPurchases(self):
        purchases = self.repo.getAllPurchases()
        return purchases
        

    def addPurchase(self, purchase_number: str, product_sku: str, supplier_name: str, auth_header: str | None):
        existing = self.repo.getPurchaseByNumber(purchase_number)
        if existing:
            raise ValueError(f"Purchase with number {purchase_number} already exists.")

        rpc = RpcClient()
        try:
            supplier = rpc.call(
                "supplier.rpc.queue",
                {"action": "get_supplier_by_name", "name": supplier_name}
            )
            if supplier.get("error"):
                raise ValueError(supplier["error"])

            product = rpc.call(
                "product.rpc.queue",
                {"action": "get_product_by_sku", "sku": product_sku}
            )
            if product.get("error"):
                raise ValueError(product["error"])

            return self.repo.addPurchase(
                purchase_number=purchase_number,
                product_id=product["id"],
                product_name=product["name"],
                product_sku=product["sku"],
                product_price=product["price"],
                product_cost=product["cost_price"],
                supplier_id=supplier["id"],
                supplier_name=supplier["name"],
                supplier_phone=supplier["phone"]
            )
        finally:
            try:
                rpc.close()
            except Exception:
                pass

    def deletePurchase(self, purchase_number: str):
        purchase = self.repo.deletePurchase(purchase_number)
        return purchase

    def updatePurchase(
        self,
        purchase_number: str,
        new_purchase_number: str,
        new_product_sku: str,
        new_supplier_name: str,
        auth_header: str | None
    ):
        existing = self.repo.getPurchaseByNumber(purchase_number)
        if not existing:
            raise ValueError(f"Purchase with number {purchase_number} does not exist.")

        updates = {}
        rpc = RpcClient()

        try:
            if new_purchase_number is not None and new_purchase_number != existing.purchase_number:
                updates["purchase_number"] = new_purchase_number

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

            if new_supplier_name is not None:
                supplier = rpc.call(
                    "supplier.rpc.queue",
                    {"action": "get_supplier_by_name", "name": new_supplier_name}
                )
                if supplier.get("error"):
                    raise ValueError(supplier["error"])

                updates["supplier_id"] = supplier["id"]
                updates["supplier_name"] = supplier["name"]
                updates["supplier_phone"] = supplier["phone"]

            if not updates:
                raise ValueError("At least one valid change is required.")

            return self.repo.updatePurchase(existing, updates)

        finally:
            try:
                rpc.close()
            except Exception:
                pass