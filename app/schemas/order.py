from pydantic import BaseModel
from datetime import datetime  

class OrderCreate(BaseModel):
    product_id: int
    quantity: int

class OrderResponse(BaseModel):
    id: int
    product_id: int
    quantity: int
    created_at: datetime
    model_config = {
        "from_attributes": True
    }
