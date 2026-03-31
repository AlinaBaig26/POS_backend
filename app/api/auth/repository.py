from sqlalchemy.exc import IntegrityError
from app.database.database import Credentials
from app.database.session import getSession

class AuthRepository:

    def validateCredentials(self, email: str, password: str) -> bool:
        session = getSession()
        try:
            credential = session.query(Credentials).filter_by(email=email, password=password).first()
            return credential is not None
        
        finally:
            session.close()

    def getByEmail(self, email: str):
        session = getSession()
        try:
            user = session.query(Credentials).filter_by(email=email).first()
            return user
        finally:
            session.close()
    
    def listUsers(self):
        session = getSession()
        try:
            return session.query(Credentials).all()
        finally:
            session.close()
    
    def createUser(self, first_name: str, last_name: str, email: str, password: str):
        session = getSession()
        try:
            existing = session.query(Credentials).filter_by(email=email).first()
            if existing:
                raise ValueError(f"User with email {email} already exists.")

            # TODO (recommended): hash password here before saving
            new_user = Credentials(first_name=first_name, last_name=last_name, email=email, password=password)
            session.add(new_user)
            session.commit()
            # return True
            return new_user
        
        except IntegrityError:
            session.rollback()
            raise ValueError("Failed to add user due to integrity error.")
        
        finally:
            session.close()
    
    def deleteByEmail(self, email: str):
        session = getSession()
        try:
            user = session.query(Credentials).filter_by(email=email).first()
            if not user:
                return False
            session.delete(user)
            session.commit()
            return True
        finally:
            session.close()