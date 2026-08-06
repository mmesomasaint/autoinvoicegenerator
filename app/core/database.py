# app/core/database.py
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase
from app.config import settings

# Adjust sqlite database parameters if running locally
is_sqlite = settings.DATABASE_URL.startswith("sqlite")
connect_args = {"check_same_thread": False} if is_sqlite else {}

# Initialize non-blocking async engine
engine = create_async_engine(
    settings.DATABASE_URL,
    echo=True,
    future=True,
    connect_args=connect_args
)

# Async session factory for dependency injection & background workers
AsyncSessionLocal = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False
)

class Base(DeclarativeBase):
    """Base ORM class for SQLAlchemy models."""
    pass

async def get_db():
    """FastAPI dependency yielding a transactional async database session."""
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()
