from sqlalchemy.exc import IntegrityError
from supplier_app.supplier_database.session import getSession
from .repository import SupplierRepository

class SupplierService:

    def __init__(self, repo: SupplierRepository | None = None):
        self.repo = repo or SupplierRepository()

    def getSupplierByName(self, name: str):
        supplier = self.repo.getSupplierByName(name)
        return supplier

    def getAllSuppliers(self):
        suppliers = self.repo.getAllSuppliers()
        return suppliers

    def addSupplier(self, name: str, phone: str):
        new_supplier = self.repo.addSupplier(name, phone)
        return new_supplier

    def deleteSupplier(self, name: str):
        supplier = self.repo.deleteSupplier(name)
        return supplier

    def updateSupplier(self, name: str = None, phone: str = None, new_name: str = None):
        supplier = self.repo.updateSupplier(name, phone, new_name)
        return supplier