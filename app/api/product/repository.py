from sqlalchemy.exc import IntegrityError
# from sqlalchemy.orm import joinedload
from app.database.database import Product
from app.database.session import getSession

class ProductRepository:


    

    def getProductBySku(self, sku: str):
        session = getSession()
        try:
            product = session.query(Product).filter_by(SKU=sku).first()
            return product
        finally:
            session.close()

    def getAllProducts(self):
        session = getSession()
        try:
            products = session.query(Product).all()
            return products
        finally:
            session.close()

    def addProduct(self, name: str, description: str, SKU: str, price: float, cost_price: float):
        session = getSession()

        try:
            if session.query(Product).filter_by(SKU=SKU).first():
                raise ValueError(f"Product with SKU {SKU} already exists.")
            new_product = Product(name=name, description=description, SKU=SKU, price=price, cost_price=cost_price)
            session.add(new_product)
            session.commit()
            return new_product
        
        except IntegrityError:
            session.rollback()
            raise ValueError("Failed to add product due to integrity error.")

        finally:
            session.close()
    

    # Upsert
    # Update - Up
    # Insert - sert
    

    def deleteProduct(self, sku: str):
        session = getSession()
        try:
            product = session.query(Product).filter_by(SKU=sku).first()
            if not product:
                session.close()
                raise ValueError(f"Product with SKU {sku} does not exist.")
            
            session.delete(product)
            session.commit()
            return True
        
        except IntegrityError:
            session.rollback()
            raise ValueError("Failed to delete product due to integrity error.")
        
        finally:
            session.close()

    def updateProduct(self, sku: str, name: str = None, description: str = None, price: float = None, cost_price: float = None, new_sku: str = None):
        session = getSession()
        try:
            product = session.query(Product).filter_by(SKU=sku).first()

            if not product:
                session.close()
                raise ValueError(f"Product with SKU {sku} does not exist.")
            
            if new_sku:
                product.SKU = new_sku
            
            if name:
                product.name = name

            if description:
                product.description = description

            if price is not None:
                product.price = price

            if cost_price is not None:
                product.cost_price = cost_price
                
            session.commit()
            return product
        
        except IntegrityError:
            session.rollback()
            raise ValueError("Failed to update product due to integrity error.")
        
        finally:
            session.close()