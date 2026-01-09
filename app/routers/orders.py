from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.deps import get_db
from app.core.redis import redis_client

from app.models.product import Product
from app.models.order import Order
from app.schemas.order import OrderCreate, OrderResponse
from app.tasks.order_task import process_order

router = APIRouter(prefix="/orders", tags=["orders"])

@router.post("/", response_model=OrderResponse)
def create_order(payload: OrderCreate, db: Session = Depends(get_db)):

    product = db.query(Product).filter(Product.id == payload.product_id).with_for_update().first()


    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    if product.stock < payload.quantity:
        raise HTTPException(status_code=400, detail="Insufficient stock")

    product.stock -= payload.quantity

    order = Order(product_id=payload.product_id, quantity=payload.quantity)
    db.add(order)
    db.commit()
    db.refresh(order)
    redis_client.delete(f"product:{payload.product_id}")

    process_order.delay(order.id)

    
    return order
