from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

engine = create_engine("sqlite:///customers.db", echo=False)
SessionLocal = sessionmaker(bind=engine)

Base = declarative_base()


Base.metadata.create_all(engine)
def getSession():
    return SessionLocal()
