from pydantic import BaseModel, Field, model_validator
from typing import Optional

class AddCustomer(BaseModel):
    name: str = Field(..., min_length=3)
    phone: str = Field(..., min_length=6)

class UpdateCustomer(BaseModel):
    name: str = Field(..., min_length=3)
    phone: str = Field(default=None, min_length=6)
    new_name: str = Field(default=None, min_length=3)
    @model_validator(mode="after")
    def check_at_least_one_field(self):
        if not self.phone and not self.new_name:
            raise ValueError(
                "At least one of 'phone' or 'new_name' must be provided."
            )
        return self

# class AddCustomer(BaseModel):
#     name: str = Field(min_length=3)
#     contact: str = Field(min_length=6)

# class CustomerResponse(BaseModel):
#     name: str = Field(min_length=3)
#     contact: str = Field(min_length=6)
