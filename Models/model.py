from Database.DatabaseOperations import DatabaseOperations as db_ops
from pydantic import BaseModel

class LoginRequest(BaseModel):
    name: str
    password: str

class SignupRequest(BaseModel):
    first_name: str
    last_name: str
    email: str
    password: str