# app/schemas/invoice.py
from pydantic import BaseModel, EmailStr, Field, ConfigDict
from typing import List, Optional
from datetime import datetime

class InvoiceItemSchema(BaseModel):
    description: str = Field(..., min_length=1, example="Backend Architecture Consulting")
    quantity: int = Field(..., gt=0, example=10)
    unit_price: float = Field(..., gt=0.0, example=150.00)

class InvoiceCreate(BaseModel):
    client_name: str = Field(..., min_length=2, example="Acme Enterprises")
    client_email: EmailStr = Field(..., example="finance@acme.com")
    items: List[InvoiceItemSchema] = Field(..., min_items=1)
    tax_rate: float = Field(default=0.075, ge=0.0, le=1.0, description="Tax percentage e.g. 0.075 for 7.5%")
    payment_due_days: int = Field(default=30, gt=0)

class InvoiceResponse(BaseModel):
    id: str
    client_name: str
    client_email: EmailStr
    subtotal: float
    tax: float
    total: float
    status: str
    pdf_url: Optional[str] = None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
