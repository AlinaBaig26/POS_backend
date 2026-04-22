from sqlalchemy import Column, Integer, String, Sequence
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class Credentials(Base):
    __tablename__ = "credentials"

    id = Column(Integer, Sequence("credentials_id_seq"), primary_key=True)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    email = Column(String(120), nullable=False, unique=True)
    password = Column(String(255), nullable=False)  # ideally store a hash
