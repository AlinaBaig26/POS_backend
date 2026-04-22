from sqlalchemy.exc import IntegrityError

from customer_app.customer_database.session import getSession
from .repository import CustomerRepository

class CustomerService:
    def __init__(self, repo: CustomerRepository | None = None):
        self.repo = repo or CustomerRepository()

    def getCustomerByName(self, name: str):
        customer = self.repo.getCustomerByName(name)
        return customer
    
    def getAllCustomers(self):
        customers = self.repo.getAllCustomers()
        return customers

    def addCustomer(self,name: str, phone: str):
        new_customer = self.repo.addCustomer(name, phone)
        if not new_customer:
            return False
        return new_customer

    def deleteCustomer(self, name: str):
        deleted = self.repo.deleteCustomer(name)
        if not deleted:
            return False
        return True
    
    def updateCustomer(self, name: str, phone: str, new_name: str = None):
        customer = self.repo.updateCustomer(name, phone, new_name)
        if not customer:
            return False
        return customer