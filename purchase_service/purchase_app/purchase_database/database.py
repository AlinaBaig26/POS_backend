from sqlalchemy import Column, Integer, String, ForeignKey, Sequence, create_engine
from sqlalchemy.orm import declarative_base, relationship, sessionmaker

engine = create_engine('sqlite:///purchases.db', echo=False)

Session = sessionmaker(bind=engine)
# session = Session()
def get_session():
    return Session()

Base = declarative_base()

class Purchase(Base):
    __tablename__ = 'purchases'
    id = Column(Integer, primary_key=True)
    purchase_number = Column(String(50), nullable=False, unique=True)

    product_id = Column(Integer, nullable=False)
    product_name = Column(String(100), nullable=False)
    product_sku = Column(String(30), nullable=False)
    product_price = Column(Integer, nullable=False)
    product_cost = Column(Integer, nullable=False)

    supplier_id = Column(Integer, nullable=False)
    supplier_name = Column(String(100), nullable=False)
    supplier_phone = Column(String(20), nullable=False)
    
def seed_data():
    session = get_session()

    try:
        if session.query(Purchase).first():
            session.close()
            return

        purchases = [
            Purchase(purchase_number="123",
                    product_id=1,product_name="Laptop",product_sku="LAP123",product_price=1200,product_cost=1000,
                    supplier_id=1,supplier_name='Tech Supplies Co.',supplier_phone='567-890-1234'),
            Purchase(purchase_number="124",
                      product_id=2,product_name="Smartphone",product_sku="SMP456",product_price=800,product_cost=600,
                      supplier_id=1,supplier_name='Tech Supplies Co.',supplier_phone='567-890-1234'),
            Purchase(purchase_number="125",
                    product_id=3,product_name="Tablet",product_sku="TAB789",product_price=600,product_cost=400,
                    supplier_id=2,supplier_name='Gadget World', supplier_phone='678-901-2345'),
            Purchase(purchase_number="126",
                    product_id=4,product_name="Headphones",product_sku="HDP012",product_price=200,product_cost=100,
                    supplier_id=3,supplier_name='ElectroMart', supplier_phone='789-012-3456')
            ]

        session.add_all(purchases)
        session.commit()

    finally:
        session.close()


Base.metadata.create_all(engine)
seed_data()
# if not session.query(Customer).first():
    # session.add_all([Customer1, Customer2, Customer3, Order1, Order2, Order3, Order4, Product1, Product2, Product3, Product4, Supplier1, Supplier2, Supplier3, Credential1])
    # session.commit()