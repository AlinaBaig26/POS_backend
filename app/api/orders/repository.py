from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import joinedload
from app.database.database import Customer, Order, Product
from app.database.session import getSession

class OrderRepository:

    def getOrdersByCustomerName(self, name: str):
        session = getSession()
        try:
            order = session.query(Order).options(joinedload(Order.product),joinedload(Order.customer)).filter(Order.customer.has(Customer.name == name)).all()
            return order
        finally:
            session.close()
    
    def getOrderByNumber(self, order_number: str):
        session = getSession()
        try:
            order = session.query(Order).options(joinedload(Order.product), joinedload(Order.customer)).filter_by(order_number=order_number).first()
            return order
        finally:
            session.close()

    def getAllOrders(self):
        session = getSession()
        try:
            orders = session.query(Order).options(joinedload(Order.product), joinedload(Order.customer)).all()
            return orders
        finally:
            session.close()
    
    # def getCustomerByName(self, customer_name: str):
    #     session = getSession()
    #     try:
    #         return session.query(Customer).filter_by(name=customer_name).first()
    #     finally:
    #         session.close()

    # def getProductBySku(self, sku: str):
    #     session = getSession()
    #     try:
    #         return session.query(Product).filter_by(SKU=sku).first()
    #     finally:
    #         session.close()

    def addOrder(self, order_number: str, product_sku: str, customer_name: str):
        session = getSession()

        try:
            customer = session.query(Customer).filter_by(name=customer_name).first()
            if not customer:
                raise ValueError(f"Customer with name {customer_name} does not exist.")

            product = session.query(Product).filter_by(SKU=product_sku).first()
            if not product:
                raise ValueError(f"Product with SKU {product_sku} does not exist.")
            
            new_order = Order(order_number=order_number,product=product, customer=customer)
            session.add(new_order)
            session.commit()
            return new_order
        
        except IntegrityError:
            session.rollback()
            raise ValueError("Failed to add order due to integrity error.")
        
        finally:
            session.close()

    def deleteOrder(self, order_number: str):
        session = getSession()
        try:
            order = session.query(Order).filter_by(order_number=order_number).first()
            if not order:
                session.close()
                raise ValueError(f"Order with number {order_number} does not exist.")
            
            session.delete(order)
            session.commit()
            return True
        finally:
            session.close()

    def updateOrder(self, order_number: str, new_order_number: str, new_customer_name: str, new_product_sku: str):
        session = getSession()
        try:
            order = session.query(Order).filter_by(order_number=order_number).first()
            if not order:
                raise ValueError(f"Order with number {order_number} does not exist.")

            if new_customer_name:
                new_customer = session.query(Customer).filter_by(name=new_customer_name).first()
                if not new_customer:
                    raise ValueError(f"Customer with name {new_customer_name} does not exist.")
                order.customer = new_customer

            if new_product_sku:
                new_product = session.query(Product).filter_by(SKU=new_product_sku).first()
                if not new_product:
                    raise ValueError(f"Product with SKU {new_product_sku} does not exist.")
                order.product = new_product

            if new_order_number:
                order.order_number = new_order_number

            session.commit()
            session.refresh(order)
            session.expunge(order)
            return order

        except IntegrityError:
            session.rollback()
            raise ValueError("Failed to update order due to integrity error.")

        finally:
            session.close()