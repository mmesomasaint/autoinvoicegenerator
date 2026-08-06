# app/main.py
from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.config import settings
from app.core.database import engine, Base
from app.api.v1.router import api_router
from app.models.invoice import InvoiceModel

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Initialize database tables
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    # Shutdown: Dispose engine connections
    await engine.dispose()

app = FastAPI(
    title=settings.PROJECT_NAME,
    lifespan=lifespan,
    version="1.0.0"
)

# Mount the V1 API router with the /api/v1 prefix
app.include_router(api_router, prefix="/api/v1")

@app.get("/health", tags=["Health"])
async def global_health_check():
    return {"status": "healthy", "service": settings.PROJECT_NAME}
