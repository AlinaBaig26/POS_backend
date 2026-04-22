from sqlalchemy.exc import IntegrityError
# from sqlalchemy.orm import joinedload
from product_app.product_database.database import Product, get_session

class ProductRepository:

    def getProductBySku(self, sku: str):
        session = get_session()
        try:
            product = session.query(Product).filter_by(sku=sku).first()
            return product
        finally:
            session.close()

    def getAllProducts(self):
        session = get_session()
        try:
            products = session.query(Product).all()
            return products
        finally:
            session.close()

    def addProduct(self, name: str, description: str, sku: str, price: float, cost_price: float):
        session = get_session()

        try:
            if session.query(Product).filter_by(sku=sku).first():
                raise ValueError(f"Product with sku {sku} already exists.")
            new_product = Product(name=name, description=description, sku=sku, price=price, cost_price=cost_price)
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
        session = get_session()
        try:
            product = session.query(Product).filter_by(sku=sku).first()
            if not product:
                session.close()
                raise ValueError(f"Product with sku {sku} does not exist.")
            
            session.delete(product)
            session.commit()
            return True
        
        except IntegrityError:
            session.rollback()
            raise ValueError("Failed to delete product due to integrity error.")
        
        finally:
            session.close()

    def updateProduct(self, sku: str, name: str = None, description: str = None, price: float = None, cost_price: float = None, new_sku: str = None):
        session = get_session()
        try:
            product = session.query(Product).filter_by(sku=sku).first()

            if not product:
                session.close()
                raise ValueError(f"Product with sku {sku} does not exist.")
            
            if new_sku:
                product.sku = new_sku
            
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