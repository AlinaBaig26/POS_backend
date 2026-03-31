from pydantic import BaseModel, Field
from typing import Optional

class AddPurchase(BaseModel):
    purchase_number: str = Field(..., min_length=1)
    supplier_name: str = Field(..., min_length=3)
    product_sku: str = Field(..., min_length=3)

class UpdatePurchase(BaseModel):
    purchase_number: str = Field(..., min_length=1)
    new_purchase_number: Optional[str] = Field(default=None, min_length=1)
    new_supplier_name: Optional[str] = Field(default=None, min_length=3)
    new_product_sku: Optional[str] = Field(default=None, min_length=3)