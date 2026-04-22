from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

engine = create_engine("sqlite:///products.db", echo=False)

Session = sessionmaker(bind=engine)

def get_session():
    return Session()

Base = declarative_base()


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False, unique=True)
    description = Column(String(1000), nullable=True)
    sku = Column(String(30), nullable=False, unique=True)
    price = Column(Integer, nullable=False)
    cost_price = Column(Integer, nullable=False)


def seed_data():
    session = get_session()

    try:
        if session.query(Product).first():
            return

        products = [
            Product(
                name="Laptop",
                description="A high-performance laptop",
                sku="LAP123",
                price=1200,
                cost_price=1000
            ),
            Product(
                name="Smartphone",
                description="A latest model smartphone",
                sku="SMP456",
                price=800,
                cost_price=600
            ),
            Product(
                name="Tablet",
                description="A lightweight tablet",
                sku="TAB789",
                price=600,
                cost_price=400
            ),
            Product(
                name="Headphones",
                description="Noise-cancelling headphones",
                sku="HDP012",
                price=200,
                cost_price=100
            ),
        ]

        session.add_all(products)
        session.commit()
    finally:
        session.close()


Base.metadata.create_all(engine)
seed_data()