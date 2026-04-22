import os
from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
# from session import getSession

engine = create_engine('sqlite:///customers.db', echo=False)
Session = sessionmaker(bind=engine)
def get_session():
    return Session()

Base = declarative_base()

class Customer(Base):
    __tablename__ = 'customers'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False, unique=True)
    phone = Column(String(20), nullable=False)

def seed_data():
    session = get_session()
    try:
        if session.query(Customer).first():
            return

        customers = [
            Customer(name='Javed Iqbal', phone='555-1234-2482'),
            Customer(name='Faiza Abdullah', phone='555-5678-1234'),
            Customer(name='Ayesha Khan', phone='555-8765-4321')]

        session.add_all(customers)
        session.commit()
    finally:
        session.close()


Base.metadata.create_all(engine)
seed_data()
# if not session.query(Customer).first():
    # session.add_all([Customer1, Customer2, Customer3, Order1, Order2, Order3, Order4, Product1, Product2, Product3, Product4, Supplier1, Supplier2, Supplier3, Credential1])
    # session.commit()