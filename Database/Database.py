from sqlalchemy import Column, Integer, String, ForeignKey, Sequence, create_engine
from sqlalchemy.orm import declarative_base, relationship, sessionmaker

engine = create_engine('sqlite:///mydatabase.db', echo=False)

Session = sessionmaker(bind=engine)
# session = Session()
def get_session():
    return Session()

Base = declarative_base()

class Credentials(Base):
    __tablename__ = 'credentials'
    id = Column(Integer, primary_key=True)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    email = Column(String(100), nullable=False, unique=True)
    password = Column(String(100), nullable=False)

class Customer(Base):
    __tablename__ = 'customers'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False, unique=True)
    phone = Column(String(20), nullable=False)

    orders = relationship('Order', back_populates='customer', cascade='all, delete-orphan')

class Order(Base):
    __tablename__ = 'orders'
    id = Column(Integer, primary_key=True)
    order_number = Column(String(50), nullable=False, unique=True)

    product_id = Column(Integer, ForeignKey('products.id'))
    product = relationship('Product', back_populates='orders')

    customer_id = Column(Integer, ForeignKey('customers.id'))
    customer = relationship('Customer', back_populates='orders')

class Product(Base):
    __tablename__ = 'products'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False, unique=True)
    description = Column(String(1000),nullable=True)
    SKU = Column(String(30), nullable=False, unique=True)
    price = Column(Integer, nullable=False)
    cost_price = Column(Integer,nullable=False)

    orders = relationship('Order', back_populates='product', cascade='all, delete-orphan')

class Supplier(Base):
    __tablename__ = 'suppliers'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False, unique=True)
    contact_info = Column(String(20), nullable=False)
    
def seed_data():
    session = get_session()

    if session.query(Customer).first():
        session.close()
        return

    Customer1 = Customer(name='Javed Iqbal', phone='555-1234-2482')
    Customer2 = Customer(name='Faiza Abdullah', phone='555-5678-1234')
    Customer3 = Customer(name='Ayesha Khan', phone='555-8765-4321')

    Product1 = Product(name='Laptop', description='A high-performance laptop', SKU='LAP123', price=1200, cost_price = 1000)
    Product2 = Product(name='Smartphone', description='A latest model smartphone', SKU='SMP456', price=800, cost_price = 600)
    Product3 = Product(name='Tablet', description='A lightweight tablet', SKU='TAB789', price=600, cost_price=400)
    Product4 = Product(name='Headphones', description='Noise-cancelling headphones', SKU='HDP012', price=200, cost_price=100)

    Order1 = Order(order_number='12',product=Product1, customer=Customer1)
    Order2 = Order(order_number='13',product=Product2, customer=Customer1)
    Order3 = Order(order_number='14',product=Product3, customer=Customer2)
    Order4 = Order(order_number='15',product=Product4, customer=Customer3)

    Supplier1 = Supplier(name='Tech Supplies Co.', contact_info='567-890-1234')
    Supplier2 = Supplier(name='Gadget World', contact_info='678-901-2345')
    Supplier3 = Supplier(name='ElectroMart', contact_info='789-012-3456')

    Credential1 = Credentials(first_name = "Alina",last_name = "Baig", email='haideralina15@gmail.com', password='password123')
    # Credential1 = Credentials(first_name = "Ayesha",last_name = "Habib", email='ayeshahabib246@gmail.com', password='password123')

    session.add_all([Customer1, Customer2, Customer3, Order1, Order2, Order3, Order4, Product1, Product2, Product3, Product4, Supplier1, Supplier2, Supplier3, Credential1])
    session.commit()


Base.metadata.create_all(engine)
seed_data()
# if not session.query(Customer).first():
    # session.add_all([Customer1, Customer2, Customer3, Order1, Order2, Order3, Order4, Product1, Product2, Product3, Product4, Supplier1, Supplier2, Supplier3, Credential1])
    # session.commit()