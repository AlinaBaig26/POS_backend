from sqlalchemy.exc import IntegrityError
# from sqlalchemy.orm import joinedload
from supplier_app.supplier_database.database import Supplier, get_session


class SupplierRepository:

    def getSupplierByName(self, name: str):
        session = get_session()
        try:
            supplier = session.query(Supplier).filter_by(name=name).first()
            return supplier
        finally:
            session.close()

    def getAllSuppliers(self):
        session = get_session()
        try:
            suppliers = session.query(Supplier).all()
            return suppliers
        finally:
            session.close()

    def addSupplier(self, name: str, phone: str):
        session = get_session()

        try:
            if session.query(Supplier).filter_by(name=name).first():
                session.close()
                raise ValueError(f"Supplier with name {name} already exists.")
            new_supplier = Supplier(name=name, phone=phone)
            session.add(new_supplier)
            session.commit()
            return new_supplier
        
        except IntegrityError:
            session.rollback()
            raise ValueError("Failed to add supplier due to integrity error.")
        
        finally:
            session.close()

    def deleteSupplier(self, name: str):
        session = get_session()
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
 
    def updateSupplier(self, name: str, phone: str = None, new_name: str = None):
        session = get_session()
        try:
            supplier = session.query(Supplier).filter_by(name=name).first()

            if not supplier:
                session.close()
                raise ValueError(f"Supplier with name {name} does not exist.")
            
            if new_name:
                supplier.name = new_name

            if phone:    
                supplier.phone = phone

            session.commit()
            return supplier

        except IntegrityError:
            session.rollback()
            raise ValueError("Failed to update supplier due to integrity error.")
        
        finally:
            session.close()