from pydantic import BaseModel, Field, model_validator
from typing import Optional

class AddSupplier(BaseModel):
    name: str = Field(..., min_length=3)
    contact_info: str = Field(..., min_length=6)

class SupplierResponse(BaseModel):
    name: str = Field(min_length=3)
    contact_info: str = Field(min_length=6)

class UpdateSupplier(BaseModel):
    name: str = Field(..., min_length=3)
    contact_info: str = Field(default=None, min_length=6)
    new_name: str = Field(default=None, min_length=3)

    def check_at_least_one_field(self):
        if not (self.phone or self.new_name):
            raise ValueError("At least one field must be provided.")
        return self