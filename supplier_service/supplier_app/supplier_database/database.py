from sqlalchemy import Column, Integer, String, ForeignKey, Sequence, create_engine
from sqlalchemy.orm import declarative_base, relationship, sessionmaker

engine = create_engine('sqlite:///suppliers.db', echo=False)

Session = sessionmaker(bind=engine)
# session = Session()
def get_session():
    return Session()

Base = declarative_base()

class Supplier(Base):
    __tablename__ = 'suppliers'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False, unique=True)
    phone = Column(String(20), nullable=False)
    
def seed_data():
    session = get_session()

    try:
        if session.query(Supplier).first():
            session.close()
            return


        suppliers = [
            Supplier(name='Tech Supplies Co.', phone='567-890-1234'),
            Supplier(name='Gadget World', phone='678-901-2345'),
            Supplier(name='ElectroMart', phone='789-012-3456')]

        session.add_all(suppliers)
        session.commit()

    finally:
        session.close()


Base.metadata.create_all(engine)
seed_data()
# if not session.query(Customer).first():
    # session.add_all([Customer1, Customer2, Customer3, Order1, Order2, Order3, Order4, Product1, Product2, Product3, Product4, Supplier1, Supplier2, Supplier3, Credential1])
    # session.commit()