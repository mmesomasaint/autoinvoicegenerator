# app/models/invoice.py
from sqlalchemy import Column, String, Float, DateTime, JSON, Enum
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import DeclarativeBase
from datetime import datetime, timezone
import uuid
import enum

class Base(AsyncAttrs, DeclarativeBase):
    pass

class InvoiceStatus(str, enum.Enum):
    PENDING = "PENDING"
    GENERATED = "GENERATED"
    SENT = "SENT"
    FAILED = "FAILED"

class InvoiceModel(Base):
    __tablename__ = "invoices"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    client_name = Column(String, nullable=False)
    client_email = Column(String, nullable=False)
    items = Column(JSON, nullable=False)
    subtotal = Column(Float, nullable=False)
    tax = Column(Float, nullable=False)
    total = Column(Float, nullable=False)
    status = Column(String, default=InvoiceStatus.PENDING.value)
    pdf_path = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
