from sqlalchemy.exc import IntegrityError
from order_app.order_database.database import Order, get_session

class OrderRepository:

    def getOrdersByCustomerName(self, customer_name: str):
        session = get_session()
        try:
            order = session.query(Order).filter_by(customer_name=customer_name).all()
            return order
        finally:
            session.close()
    
    def getOrderByNumber(self, order_number: str):
        session = get_session()
        try:
            order = session.query(Order).filter_by(order_number=order_number).first()
            return order
        finally:
            session.close()

    def getAllOrders(self):
        session = get_session()
        try:
            orders = session.query(Order).all()
            return orders
        finally:
            session.close()

    def addOrder(self, order_number: str, product_id: int, product_name: str, product_sku: str,
                 product_price: float, product_cost: float, customer_id: int,
                 customer_name: str, customer_phone: str):
        session = get_session()
        try:
            existing = session.query(Order).filter_by(order_number=order_number).first()
            if existing:
                raise ValueError(f"Order with number {order_number} already exists.")

            new_order = Order(
                order_number=order_number,
                product_id=product_id,
                product_name=product_name,
                product_sku=product_sku,
                product_price=product_price,
                product_cost=product_cost,
                customer_id=customer_id,
                customer_name=customer_name,
                customer_phone=customer_phone
            )

            session.add(new_order)
            session.commit()
            session.refresh(new_order)
            session.expunge(new_order)
            return new_order

        except IntegrityError:
            session.rollback()
            raise ValueError("Failed to add order due to integrity error.")
        finally:
            session.close()

    def deleteOrder(self, order_number: str):
        session = get_session()
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

    def updateOrder(self, db_order, updates: dict):
        session = get_session()
        try:
            order_number = db_order.order_number
            db_order = session.query(Order).filter_by(order_number=order_number).first()
            if not db_order:
                raise ValueError(f"Order with number {order_number} does not exist.")

            for field, value in updates.items():
                setattr(db_order, field, value)

            session.commit()
            session.refresh(db_order)
            session.expunge(db_order)
            return db_order

        except IntegrityError:
            session.rollback()
            raise ValueError("Failed to update order due to integrity error.")

        finally:
            session.close()