from sqlalchemy.exc import IntegrityError
# from sqlalchemy.orm import joinedload
from app.database.database import Supplier
from app.database.session import getSession


class SupplierRepository:

    def getSupplierByName(self, name: str):
        session = getSession()
        try:
            supplier = session.query(Supplier).filter_by(name=name).first()
            return supplier
        finally:
            session.close()

    def getAllSuppliers(self):
        session = getSession()
        try:
            suppliers = session.query(Supplier).all()
            return suppliers
        finally:
            session.close()

    def addSupplier(self, name: str, contact_info: str):
        session = getSession()

        try:
            if session.query(Supplier).filter_by(name=name).first():
                session.close()
                raise ValueError(f"Supplier with name {name} already exists.")
            new_supplier = Supplier(name=name, contact_info=contact_info)
            session.add(new_supplier)
            session.commit()
            return new_supplier
        
        except IntegrityError:
            session.rollback()
            raise ValueError("Failed to add supplier due to integrity error.")
        
        finally:
            session.close()

    def deleteSupplier(self, name: str):
        session = getSession()
        try:
            supplier = session.query(Supplier).filter_by(name=name).first()

            if not supplier:
                session.close()
                raise ValueError(f"Supplier with name {name} does not exist.")

            session.delete(supplier)
            session.commit()
            return True

        except IntegrityError:
            session.rollback()
            raise ValueError("Failed to delete supplier due to integrity error.")
        
        finally:
            session.close()
 
    def updateSupplier(self, name: str, contact_info: str = None, new_name: str = None):
        session = getSession()
        try:
            supplier = session.query(Supplier).filter_by(name=name).first()

            if not supplier:
                session.close()
                raise ValueError(f"Supplier with name {name} does not exist.")
            
            if new_name:
                supplier.name = new_name

            if contact_info:    
                supplier.contact_info = contact_info

            session.commit()
            return supplier

        except IntegrityError:
            session.rollback()
            raise ValueError("Failed to update supplier due to integrity error.")
        
        finally:
            session.close()