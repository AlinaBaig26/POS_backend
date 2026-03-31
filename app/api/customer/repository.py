from sqlalchemy.exc import IntegrityError
# from sqlalchemy.orm import joinedload
from app.database.database import Customer
from app.database.session import getSession

class CustomerRepository:

    def getCustomerByName(self, name: str):
        session = getSession()
        try:
            customer = session.query(Customer).filter_by(name=name).first()
            return customer
        finally:
            session.close()
    
    def getAllCustomers(self):
        session = getSession()
        try:
            customers = session.query(Customer).all()
            return customers
        finally:
            session.close()

    def addCustomer(self, name: str, phone: str):
        session = getSession()

        try:
            existing = session.query(Customer).filter_by(name=name).first()
            if existing:
                raise ValueError(f"Customer with name {name} already exists.")

            new_customer = Customer(name=name, phone=phone)
            session.add(new_customer)
            session.commit()
            return new_customer.name

        except IntegrityError:
            session.rollback()
            raise ValueError("Failed to add customer due to integrity error.")
        finally:
            session.close()

    def deleteCustomer(self, name: str):
        session = getSession()
        try:
            customer = session.query(Customer).filter_by(name=name).first()
            if not customer:
                return False
            
            session.delete(customer)
            session.commit()
            return True
        
        finally:
            session.close()
    
    def updateCustomer(self, name: str, phone: str, new_name: str = None):
        session = getSession()
        customer = session.query(Customer).filter_by(name=name).first()
        try:
            if not customer:
                return False
            
            if new_name and new_name != name:
                customer.name = new_name

            if phone and phone != customer.phone:    
                customer.phone = phone
            session.commit()
            return customer
        finally:   
            session.close()