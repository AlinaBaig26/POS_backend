from sqlalchemy.exc import IntegrityError
from app.database.session import getSession
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

    def addSupplier(self, name: str, contact_info: str):
        new_supplier = self.repo.addSupplier(name, contact_info)
        return new_supplier

    def deleteSupplier(self, name: str):
        supplier = self.repo.deleteSupplier(name)
        return supplier

    def updateSupplier(self, name: str = None, contact_info: str = None, new_name: str = None):
        supplier = self.repo.updateSupplier(name, contact_info, new_name)
        return supplier