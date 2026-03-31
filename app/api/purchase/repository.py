from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import joinedload
from app.database.database import Product, Supplier, Purchase
from app.database.session import getSession


class PurchaseRepository:
    
    def getPurchaseBySupplierName(self, name: str):
        session = getSession()
        try:
            purchase = session.query(Purchase).options(joinedload(Purchase.product),joinedload(Purchase.supplier)).filter(Supplier.name == name).all()
            return purchase
        finally:
            session.close()
    
    def getPurchaseByNumber(self, purchase_number: str):
        session = getSession()

        try:
            purchase = session.query(Purchase).options(joinedload(Purchase.product), joinedload(Purchase.supplier)).filter_by(purchase_number=purchase_number).first()
            return purchase
        finally:
            session.close()
    
    def getAllPurchases(self):
        session = getSession()

        try:
            orders = session.query(Purchase).options(joinedload(Purchase.product), joinedload(Purchase.supplier)).all()
            return orders
        finally:
            session.close()

    def addPurchase(self, purchase_number: str, product_sku: str, supplier_name: str):
        session = getSession()

        try:
            supplier = session.query(Supplier).filter_by(name=supplier_name).first()
            if not supplier:
                raise ValueError(f"Supplier with name {supplier_name} does not exist.")

            product = session.query(Product).filter_by(SKU=product_sku).first()
            if not product:
                raise ValueError(f"Product with SKU {product_sku} does not exist.")
            
            new_purchase = Purchase(purchase_number=purchase_number,product=product, supplier=supplier)
            session.add(new_purchase)
            session.commit()
            return new_purchase
        
        except IntegrityError:
            session.rollback()
            raise ValueError("Failed to add order due to integrity error.")
        
        finally:
            session.close()
        
    def getSupplierByName(self, session, name: str):
        session = getSession()

        supplier = session.query(Supplier).filter_by(name=name).first()
        return supplier
    
    def getProductBySku(self, session, sku: str):
        session = getSession()

        product = session.query(Product).filter_by(SKU=sku).first()
        return product
    
    def deletePurchase(self, purchase_number: str):
        session = getSession()
        purchase = session.query(Purchase).filter_by(purchase_number=purchase_number).first()
        if not purchase:
            session.close()
            raise ValueError(f"Purchase with number {purchase_number} does not exist.")
        
        session.delete(purchase)
        session.commit()
        session.close()
        return True
    
    def updatePurchase(self, purchase_number: str, new_purchase_number: str, new_supplier_name: str, new_product_sku: str):
        session = getSession()

        try:
            purchase = session.query(Purchase).filter_by(purchase_number=purchase_number).first()
            if not purchase:
                raise ValueError(f"Purchase with number {purchase_number} does not exist.")

            if new_supplier_name:
                new_supplier = session.query(Supplier).filter_by(name=new_supplier_name).first()
                if not new_supplier:
                    raise ValueError(f"Supplier with name {new_supplier_name} does not exist.")
                purchase.supplier = new_supplier

            if new_product_sku:
                new_product = session.query(Product).filter_by(SKU=new_product_sku).first()
                if not new_product:
                    raise ValueError(f"Product with SKU {new_product_sku} does not exist.")
                purchase.product = new_product

            if new_purchase_number:
                purchase.purchase_number = new_purchase_number

            session.commit()
            session.refresh(purchase)
            session.expunge(purchase)
            return purchase

        except IntegrityError:
            session.rollback()
            raise ValueError("Failed to update purchase due to integrity error.")

        finally:
            session.close()