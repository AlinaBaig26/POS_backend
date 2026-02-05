from sqlalchemy.exc import IntegrityError
from Database.Database import Credentials, Customer, Order, Product, Supplier, get_session

session = get_session()
class DatabaseOperations:

    @staticmethod
    def _session():
        return get_session()
    
    @staticmethod
    def check_credentials(name: str, password: str) -> bool:
        session = DatabaseOperations._session()
        credential = session.query(Credentials).filter_by(name=name, password=password).first()
        session.close()
        return credential is not None

    @staticmethod
    def get_customer_by_name(name: str):
        session = DatabaseOperations._session()
        customer = session.query(Customer).filter_by(name=name).first()
        session.close()
        return customer

    @staticmethod
    def get_orders_by_customer_name(name: str):
        session = DatabaseOperations._session()
        order = session.query(Order).join(Customer).filter(Customer.name == name).all()
        session.close()
        return order
    
    @staticmethod
    def get_order_by_number(order_number: str):
        session = DatabaseOperations._session()
        order = session.query(Order).filter_by(order_number=order_number).first()
        session.close()
        return order

    @staticmethod
    def get_product_by_sku(sku: str):
        session = DatabaseOperations._session()
        product = session.query(Product).filter_by(SKU=sku).first()
        session.close()
        return

    @staticmethod
    def get_supplier_by_name(name: str):
        session = DatabaseOperations._session()
        supplier = session.query(Supplier).filter_by(name=name).first()
        session.close()
        return supplier

    @staticmethod
    def get_all_customers():
        session = DatabaseOperations._session()
        customers = session.query(Customer).all()
        session.close()
        return customers

    @staticmethod
    def get_all_orders():
        session = DatabaseOperations._session()
        orders = session.query(Order).all()
        session.close()
        return orders

    @staticmethod
    def get_all_products():
        session = DatabaseOperations._session()
        products = session.query(Product).all()
        session.close()
        return products

    @staticmethod
    def get_all_suppliers():
        session = DatabaseOperations._session()
        suppliers = session.query(Supplier).all()
        session.close()
        return suppliers

    @staticmethod
    def add_customer(name: str, phone: str):
        session = DatabaseOperations._session()

        if DatabaseOperations.get_customer_by_name(name):
            session.close()
            raise ValueError(f"Customer with name {name} already exists.")
        
        try:
            new_customer = Customer(name=name, phone=phone)
            session.add(new_customer)
            session.commit()
            return new_customer
        
        except IntegrityError:
            session.rollback()
            raise ValueError("Failed to add customer due to integrity error.")
        
        finally:
            session.close()

    @staticmethod
    def add_order(order_number: str, product_sku: str, customer_name: str):
        session = DatabaseOperations._session()

        customer = DatabaseOperations.get_customer_by_name(customer_name)
        product = DatabaseOperations.get_product_by_sku(product_sku)
        if not customer:
            session.close()
            raise ValueError(f"Customer with name {customer_name} does not exist.")
        if not product:
            session.close()
            raise ValueError(f"Product with SKU {product_sku} does not exist.")
        
        try:
            new_order = Order(order_number=order_number,product=product, customer=customer)
            session.add(new_order)
            session.commit()
            return new_order
        
        except IntegrityError:
            session.rollback()
            raise ValueError("Failed to add order due to integrity error.")
        
        finally:
            session.close()

    @staticmethod
    def add_product(name: str, description: str, SKU: str, price: int, cost_price: int):
        session = DatabaseOperations._session()

        if DatabaseOperations.get_product_by_sku(SKU):
            session.close()
            raise ValueError(f"Product with SKU {SKU} already exists.")
        
        try:
            new_product = Product(name=name, description=description, SKU=SKU, price=price, cost_price=cost_price)
            session.add(new_product)
            session.commit()
            return new_product
        
        except IntegrityError:
            session.rollback()
            raise ValueError("Failed to add product due to integrity error.")
        
        finally:
            session.close()

    @staticmethod
    def add_supplier(name: str, contact_info: str):
        session = DatabaseOperations._session()

        if DatabaseOperations.get_supplier_by_name(name):
            session.close()
            raise ValueError(f"Supplier with name {name} already exists.")
        try:
            new_supplier = Supplier(name=name, contact_info=contact_info)
            session.add(new_supplier)
            session.commit()
            return new_supplier
        except IntegrityError:
            session.rollback()
            raise ValueError("Failed to add product due to integrity error.")
        
        finally:
            session.close()

    @staticmethod
    def delete_customer(name: str):
        session = DatabaseOperations._session()
        customer = DatabaseOperations.get_customer_by_name(name)
        if not customer:
            session.close()
            raise ValueError(f"Customer with name {name} does not exist.")
        
        session.delete(customer)
        session.commit()
        session.close()
        return True
    
    @staticmethod
    def delete_order(order_number: str):
        session = DatabaseOperations._session()
        order = session.query(Order).filter_by(id=order_number).first()
        if not order:
            session.close()
            raise ValueError(f"Order with number {order_number} does not exist.")
        
        session.delete(order)
        session.commit()
        session.close()
        return True

    @staticmethod
    def delete_product(sku: str):
        session = DatabaseOperations._session()
        product = DatabaseOperations.get_product_by_sku(sku)
        if not product:
            session.close()
            raise ValueError(f"Product with SKU {sku} does not exist.")
        
        session.delete(product)
        session.commit()
        session.close()
        return True
        
    @staticmethod
    def delete_supplier(name: str):
        session = DatabaseOperations._session()

        supplier = DatabaseOperations.get_supplier_by_name(name)

        if not supplier:
            session.close()
            raise ValueError(f"Supplier with name {name} does not exist.")

        session.delete(supplier)
        session.commit()
        session.close()
        return True
    
    @staticmethod
    def update_customer(name: str, phone: str, new_name: str = None):
        session = DatabaseOperations._session()

        customer = DatabaseOperations.get_customer_by_name(name)

        if not customer:
            session.close()
            raise ValueError(f"Customer with name {name} does not exist.")
        
        if new_name:
            customer.name = new_name

        if phone:    
            customer.phone = phone
            
        session.commit()
        session.close()
        return customer
    
    @staticmethod
    def update_product(sku: str, name: str = None, description: str = None, price: int = None, cost_price: int = None, new_sku: str = None):
        session = DatabaseOperations._session()
        product = DatabaseOperations.get_product_by_sku(sku)

        if not product:
            session.close()
            raise ValueError(f"Product with SKU {sku} does not exist.")
        
        if new_sku:
            product.SKU = new_sku
        
        if name:
            product.name = name

        if description:
            product.description = description

        if price is not None:
            product.price = price

        if cost_price is not None:
            product.cost_price = cost_price
            
        session.commit()
        session.close()
        return product
    
    @staticmethod
    def update_supplier(name: str, contact_info: str = None, new_name: str = None):
        session = DatabaseOperations._session()

        supplier = DatabaseOperations.get_supplier_by_name(name)

        if not supplier:
            session.close()
            raise ValueError(f"Supplier with name {name} does not exist.")
        
        if new_name:
            supplier.name = new_name

        if contact_info:    
            supplier.contact_info = contact_info
            
        session.commit()
        session.close()
        return supplier
    
    @staticmethod
    def update_order(order_number: str, new_order_number: str, new_customer_name: str, new_product_sku: str):
        session = DatabaseOperations._session()

        order = DatabaseOperations.get_order_by_number(order_number)
        if not order:
            session.close()
            raise ValueError(f"Order with number {order_number} does not exist.")

        if new_customer_name:
            new_customer = DatabaseOperations.get_customer_by_name(new_customer_name)
            if not new_customer:
                raise ValueError(f"Customer with name {new_customer_name} does not exist.")
            order.customer = new_customer

        if new_product_sku:
            new_product = DatabaseOperations.get_product_by_sku(new_product_sku)
            if not new_product:
                raise ValueError(f"Product with sku {new_product_sku} does not exist.")
            order.product = new_product

        if new_order_number:
            order.order_number = new_order_number

        session.commit()
        session.close()
        return order