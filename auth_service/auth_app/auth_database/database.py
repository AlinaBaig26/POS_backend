from sqlalchemy import Column, Integer, String, ForeignKey, Sequence, create_engine
from sqlalchemy.orm import declarative_base, relationship, sessionmaker

engine = create_engine('sqlite:///authorization.db', echo=False)

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
    
def seed_data():
    session = get_session()

    try:
        if session.query(Credentials).first():
            return

        credential_1 = Credentials(
            first_name="Alina",
            last_name="Baig",
            email="haideralina15@gmail.com",
            password="password123"
        )

        session.add(credential_1)
        session.commit()
    finally:
        session.close()


Base.metadata.create_all(engine)
seed_data()
# if not session.query(Customer).first():
    # session.add_all([Customer1, Customer2, Customer3, Order1, Order2, Order3, Order4, Product1, Product2, Product3, Product4, Supplier1, Supplier2, Supplier3, Credential1])
    # session.commit()