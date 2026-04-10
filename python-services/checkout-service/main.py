"""
ShopSphere Platform — Checkout Service
Entry point for the Checkout microservice.
"""
from fastapi import FastAPI
from app.api.checkout_api import router
from app.core.logging_config import setup_logging

setup_logging()

app = FastAPI(
    title="ShopSphere Checkout Service",
    description="Handles customer checkout flow",
    version="2.4.1",
)

app.include_router(router, prefix="/api/v1")


@app.get("/health")
def health_check():
    return {"status": "ok", "service": "checkout-service", "version": "2.4.1"}
