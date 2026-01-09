from fastapi import FastAPI

from app.routers.products import router as products_router
from app.routers.orders import router as orders_router

from app.db.database import engine, Base

#temp stuff
from app.models.product import Product
from app.models.order import Order


Base.metadata.create_all(bind=engine)

app = FastAPI(title="Distributed E-Commerce Order System - Chronicle Backend Techincal Test")

@app.get("/health")
def health_check():
    return {"status": "ok"}

app.include_router(products_router)  
app.include_router(orders_router)