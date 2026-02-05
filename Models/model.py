from Database.DatabaseOperations import DatabaseOperations as db_ops
from pydantic import BaseModel

class LoginRequest(BaseModel):
    name: str
    password: str