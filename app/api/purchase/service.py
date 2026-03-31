from sqlalchemy.exc import IntegrityError
from app.database.session import getSession
from .repository import PurchaseRepository

class PurchaseService:

    def __init__(self, repo: PurchaseRepository | None = None):
        self.repo = repo or PurchaseRepository()

    def getPurchaseBySupplierName(self, name: str):
        order = self.repo.getPurchaseBySupplierName(name)
        return order
        
  
    def getPurchaseByNumber(self, purchase_number: str):
        purchase = self.repo.getPurchaseByNumber(purchase_number)
        return purchase
        

    def getAllPurchases(self):
        orders = self.repo.getAllPurchases()
        return orders
        

    def addPurchase(self, purchase_number: str, product_sku: str, supplier_name: str):
        new_purchase = self.repo.addPurchase(purchase_number, product_sku, supplier_name)
        return new_purchase

    def deletePurchase(self, purchase_number: str):
        session = getSession()
        try:
            purchase = self.repo.getPurchaseByNumber(purchase_number)
            if not purchase:
                session.close()
                raise ValueError(f"Purchase with number {purchase_number} does not exist.")
            
            session.delete(purchase)
            session.commit()
            return True
        
        finally:
            session.close()

    def updatePurchase(self, purchase_number: str, new_purchase_number: str, new_supplier_name: str, new_product_sku: str):
        purchase = self.repo.updatePurchase(purchase_number, new_purchase_number, new_supplier_name, new_product_sku)
        return purchase