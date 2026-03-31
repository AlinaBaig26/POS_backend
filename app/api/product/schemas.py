from pydantic import BaseModel, Field, model_validator
from typing import Optional

class AddProduct(BaseModel):
    name: str = Field(..., min_length=3)
    sku: str = Field(..., min_length=3)
    description: Optional[str] = None
    price: float
    cost_price: float
    @model_validator(mode="after")
    def validate_price(self):
        # price = values.get("price")
        # cost_price = values.get("cost_price")
        if self.price <= self.cost_price:
            raise ValueError("Price must be greater than cost price.")
        return self
    
class UpdateProduct(BaseModel):
    name: str = Field(min_length=3)
    sku: str = Field(..., min_length=3)
    description: Optional[str] = None
    price: Optional[float] = None
    cost_price: Optional[float] = None
    new_sku: Optional[str] = None
    @model_validator(mode="after")
    def validate_price(self):
        if self.price is not None and self.cost_price is not None and self.price <= self.cost_price:
            raise ValueError("Price must be greater than cost price.")
        return self
    @model_validator(mode="after")
    def check_at_least_one_field(self):
        if not any([self.description, self.price, self.cost_price, self.new_sku]):
            raise ValueError(
                "At least one of 'description', 'price', 'cost price' or 'sku' must be provided."
            )
        return self