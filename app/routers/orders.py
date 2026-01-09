from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.deps import get_db

from app.models.product import Product
from app.models.order import Order
from app.schemas.order import OrderCreate, OrderResponse

router = APIRouter(prefix="/orders", tags=["orders"])

@router.post("/", response_model=OrderResponse)
def create_order(payload: OrderCreate, db: Session = Depends(get_db)):
    try:
        with db.begin():
            product = db.query(Product).filter(Product.id == payload.product_id).with_for_update().first()


            if not product:
                raise HTTPException(status_code=404, detail="Product not found")
            if product.stock < payload.quantity:
                raise HTTPException(status_code=400, detail="Insufficient stock")

            #TODO: Concurrency control
            product.stock -= payload.quantity

            order = Order(product_id=payload.product_id, quantity=payload.quantity)
            db.add(order)



        return order
    except HTTPException:
        raise
