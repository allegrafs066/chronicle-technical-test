from fastapi import FastAPI

from app.routers.products import router as products_router

from app.db.database import engine, Base

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Distributed E-Commerce Order System - Chronicle Backend Techincal Test")

@app.get("/health")
def health_check():
    return {"status": "ok"}

app.include_router(products_router)  