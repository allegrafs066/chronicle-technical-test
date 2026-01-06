from fastapi import FastAPI

app =FastAPI(title="Distributed E-Commerce Order System - Chronicle Backend Techincal Test")

@app.get("/health")
def health_check():
    return {"status": "ok"}