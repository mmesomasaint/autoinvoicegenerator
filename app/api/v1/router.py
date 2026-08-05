# app/api/v1/router.py
from fastapi import APIRouter
from app.api.v1.endpoints import router as invoice_router

api_router = APIRouter()

# Include endpoint modules under the V1 router namespace
api_router.include_router(invoice_router, prefix="", tags=["Invoices"])
