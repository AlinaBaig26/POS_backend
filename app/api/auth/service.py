# from datetime import timedelta
# from sqlalchemy.exc import IntegrityError
# from flask import current_app
from flask_jwt_extended import create_access_token, create_refresh_token
from .repository import AuthRepository

class AuthService:
    def __init__(self, repo: AuthRepository | None = None):
        self.repo = repo or AuthRepository()

    def signup(self, first_name: str, last_name: str, email: str, password: str):
        
        user = self.repo.createUser(first_name, last_name, email, password)
        return user
        

    def login(self, email: str, password: str):
        is_valid = self.repo.validateCredentials(email, password)
        if not is_valid:
            return None
        
        # access_expires = current_app.config["ACCESS_EXPIRES"]
        # refresh_expires = current_app.config["REFRESH_EXPIRES"]

        access_token = create_access_token(identity=email)
        refresh_token = create_refresh_token(identity=email)

        return {"access_token": access_token, "refresh_token": refresh_token}

    def refreshTokens(self, identity: str):
        # access_expires = current_app.config["ACCESS_EXPIRES"]
        # refresh_expires = current_app.config["REFRESH_EXPIRES"]

        new_access = create_access_token(identity=identity)
        new_refresh = create_refresh_token(identity=identity)

        return {"access_token": new_access, "refresh_token": new_refresh}

    def listUsers(self):
        list = self.repo.listUsers()
        return list

    def deleteUser(self, email: str) -> bool:
        deleted = self.repo.deleteByEmail(email)
        if not deleted:
            return False
        return True
        
