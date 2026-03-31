from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine("sqlite:///mydatabase.db", echo=False)
SessionLocal = sessionmaker(bind=engine)

def getSession():
    return SessionLocal()
