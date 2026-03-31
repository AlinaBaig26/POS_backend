from sqlalchemy.exc import IntegrityError
from app.database.session import getSession
from .repository import OrderRepository

class OrderService:

    def __init__(self, repo: OrderRepository | None = None):
        self.repo = repo or OrderRepository()

    def getOrdersByCustomerName(self, name: str):
        order = self.repo.getOrdersByCustomerName(name)
        return order
        
  
    def getOrderByNumber(self, order_number: str):
        order = self.repo.getOrderByNumber(order_number)
        return order
        

    def getAllOrders(self):
        orders = self.repo.getAllOrders()
        return orders
        

    def addOrder(self, order_number: str, product_sku: str, customer_name: str):
        new_order = self.repo.addOrder(order_number, product_sku, customer_name)
        return new_order

    def deleteOrder(self, order_number: str):
        order = self.repo.deleteOrder(order_number)
        return order

    def updateOrder(self, order_number: str, new_order_number: str, new_customer_name: str, new_product_sku: str):
        order = self.repo.updateOrder(order_number, new_order_number, new_customer_name, new_product_sku)
        return order