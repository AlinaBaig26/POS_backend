from pydantic import BaseModel, Field
from typing import Optional

class AddOrder(BaseModel):
    order_number: str = Field(..., min_length=1)
    customer_name: str = Field(..., min_length=3)
    product_sku: str = Field(..., min_length=3)

class UpdateOrder(BaseModel):
    order_number: str = Field(..., min_length=1)
    new_order_number: Optional[str] = Field(default=None, min_length=1)
    new_customer_name: Optional[str] = Field(default=None, min_length=3)
    new_product_sku: Optional[str] = Field(default=None, min_length=3)