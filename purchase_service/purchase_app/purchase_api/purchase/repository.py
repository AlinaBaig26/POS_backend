from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import joinedload
from purchase_app.purchase_database.database import Purchase, get_session


class PurchaseRepository:
    
    def getPurchaseBySupplierName(self, name: str):
        session = get_session()
        try:
            purchase = session.query(Purchase).filter_by(supplier_name = name).all()
            return purchase
        finally:
            session.close()
    
    def getPurchaseByNumber(self, purchase_number: str):
        session = get_session()

        try:
            purchase = session.query(Purchase).filter_by(purchase_number=purchase_number).first()
            return purchase
        finally:
            session.close()
    
    def getAllPurchases(self):
        session = get_session()

        try:
            purchase = session.query(Purchase).all()
            return purchase
        finally:
            session.close()

    def addPurchase(self, purchase_number: str, product_id: int, product_name: str, product_sku: str, product_price: float,             product_cost:float, supplier_id: int, supplier_name: str, supplier_phone: str):
        session = get_session()

        try:
            existing = session.query(Purchase).filter_by(purchase_number=purchase_number).first()
            if existing:
                raise ValueError(f"Purchase with number {purchase_number} already exists.")

            new_purchase = Purchase(
                purchase_number=purchase_number,
                product_id=product_id,
                product_name=product_name,
                product_sku=product_sku,
                product_price=product_price,
                product_cost=product_cost,
                supplier_id=supplier_id,
                supplier_name=supplier_name,
                supplier_phone=supplier_phone
            )
            session.add(new_purchase)
            session.commit()
            session.refresh(new_purchase)
            session.expunge(new_purchase)
            return new_purchase
        
        except IntegrityError:
            session.rollback()
            raise ValueError("Failed to add purchase due to integrity error.")
        
        finally:
            session.close()
    
    def deletePurchase(self, purchase_number: str):
        session = get_session()
        try:
            purchase = session.query(Purchase).filter_by(purchase_number=purchase_number).first()
            if not purchase:
                session.close()
                raise ValueError(f"Purchase with number {purchase_number} does not exist.")
            
            session.delete(purchase)
            session.commit()
            return True
        finally:
            session.close()
    
    def updatePurchase(self, db_purchase, updates: dict):
        session = get_session()

        try:
            purchase_number = db_purchase.purchase_number
            purchase = session.query(Purchase).filter_by(purchase_number=purchase_number).first()
            if not purchase:
                raise ValueError(f"Purchase with number {purchase_number} does not exist.")
            
            for field, value in updates.items():
                setattr(purchase, field, value)

            session.commit()
            session.refresh(purchase)
            session.expunge(purchase)
            return purchase

        except IntegrityError:
            session.rollback()
            raise ValueError("Failed to update purchase due to integrity error.")

        finally:
            session.close()