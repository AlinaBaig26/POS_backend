from sqlalchemy import Column, Integer, String, ForeignKey, Sequence, create_engine
from sqlalchemy.orm import declarative_base, relationship, sessionmaker

engine = create_engine('sqlite:///orders.db', echo=False)

Session = sessionmaker(bind=engine)
# session = Session()
def get_session():
    return Session()

Base = declarative_base()

class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True)
    order_number = Column(String(50), nullable=False, unique=True)

    product_id = Column(Integer, nullable=False)
    product_name = Column(String(100), nullable=False)
    product_sku = Column(String(30), nullable=False)
    product_price = Column(Integer, nullable=False)
    product_cost = Column(Integer, nullable=False)

    customer_id = Column(Integer, nullable=False)
    customer_name = Column(String(100), nullable=False)
    customer_phone = Column(String(20), nullable=False)

    
def seed_data():
    session = get_session()
    try:
        if session.query(Order).first():
            session.close()
            return
        
        orders = [
                Order(order_number="12",
                      product_id=1,product_name="Laptop",product_sku="LAP123",product_price=1200,product_cost=1000,
                      customer_id=1,customer_name='Javed Iqbal',customer_phone='555-1234-2482'),
                Order(order_number="13",
                      product_id=2,product_name="Smartphone",product_sku="SMP456",product_price=800,product_cost=600,
                      customer_id=1,customer_name='Javed Iqbal',customer_phone='555-1234-2482'),
                Order(order_number="14",
                      product_id=3,product_name="Tablet",product_sku="TAB789",product_price=600,product_cost=400,
                      customer_id=2,customer_name='Faiza Abdullah', customer_phone='555-5678-1234'),
                Order(order_number="15",
                      product_id=4,product_name="Headphones",product_sku="HDP012",product_price=200,product_cost=100,
                      customer_id=3,customer_name='Ayesha Khan', customer_phone='555-8765-4321')
            ]

        session.add_all(orders)
        session.commit()

    finally:
        session.close()


Base.metadata.create_all(engine)
seed_data()
# if not session.query(Customer).first():
    # session.add_all([Customer1, Customer2, Customer3, Order1, Order2, Order3, Order4, Product1, Product2, Product3, Product4, Supplier1, Supplier2, Supplier3, Credential1])
    # session.commit()