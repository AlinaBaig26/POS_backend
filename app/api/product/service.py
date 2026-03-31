from sqlalchemy.exc import IntegrityError
# from sqlalchemy.orm import joinedload
# from database.Database import Product
from app.database.session import getSession
from .repository import ProductRepository

class ProductService:
    # SRP Single Resposibility Principle

    def __init__(self, repo: ProductRepository | None = None):
        self.repo = repo or ProductRepository()

    def getProductBySku(self, sku: str):
        product = self.repo.getProductBySku(sku)
        return product

    def getAllProducts(self):
        products = self.repo.getAllProducts()
        return products

    def addProduct(self, name: str, description: str, SKU: str, price: float, cost_price: float):
        new_product = self.repo.addProduct(name, description, SKU, price, cost_price)
        return new_product

    def deleteProduct(self, sku: str):
        product = self.repo.deleteProduct(sku)
        return product

    def updateProduct(self, sku: str, name: str = None, description: str = None, price: float = None, cost_price: float = None, new_sku: str = None):
        product = self.repo.updateProduct(sku, name, description, price, cost_price, new_sku)
        return product