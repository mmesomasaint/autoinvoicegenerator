# app/api/v1/endpoints.py
from fastapi import APIRouter, Depends, BackgroundTasks, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
import os

from app.schemas.invoice import InvoiceCreate, InvoiceResponse
from app.models.invoice import InvoiceModel, InvoiceStatus
from app.core.database import get_db
from app.core.security import verify_api_key
from app.services.pdf_service import pdf_service
from app.services.email_service import send_invoice_email
from app.config import settings

router = APIRouter()

async def process_invoice_background(invoice_id: str, db_factory):
    """Async background worker routine to execute PDF creation & emailing."""
    async with db_factory() as db:
        result = await db.execute(select(InvoiceModel).filter(InvoiceModel.id == invoice_id))
        invoice = result.scalars().first()
        if not invoice:
            return

        try:
            pdf_filename = f"Invoice_{invoice.id}.pdf"
            pdf_path = os.path.join(settings.STORAGE_DIR, pdf_filename)
            
            # Compile PDF
            pdf_service.generate_invoice_pdf({
                "id": invoice.id,
                "client_name": invoice.client_name,
                "client_email": invoice.client_email,
                "items": invoice.items,
                "subtotal": invoice.subtotal,
                "tax": invoice.tax,
                "total": invoice.total,
                "created_at": invoice.created_at
            }, pdf_path)
            
            invoice.pdf_path = pdf_path
            invoice.status = InvoiceStatus.GENERATED.value

            # Dispatch Email
            await email_service.send_invoice_email(
                client_email=payload.client_email, 
                invoice_id=invoice_id,
                pdf_path=pdf_path
            )
            invoice.status = InvoiceStatus.SENT.value
            
        except Exception as e:
            invoice.status = InvoiceStatus.FAILED.value
        
        await db.commit()

@router.post("/invoices", response_model=InvoiceResponse, status_code=status.HTTP_202_ACCEPTED, dependencies=[Depends(verify_api_key)])
async def create_invoice(
    payload: InvoiceCreate, 
    background_tasks: BackgroundTasks, 
    db: AsyncSession = Depends(get_db)
):
    # Compute monetary math
    subtotal = sum(item.quantity * item.unit_price for item in payload.items)
    tax = subtotal * payload.tax_rate
    total = subtotal + tax

    db_invoice = InvoiceModel(
        client_name=payload.client_name,
        client_email=payload.client_email,
        items=[item.model_dump() for item in payload.items],
        subtotal=subtotal,
        tax=tax,
        total=total,
        status=InvoiceStatus.PENDING.value
    )
    
    db.add(db_invoice)
    await db.commit()
    await db.refresh(db_invoice)

    from app.core.database import AsyncSessionLocal
    background_tasks.add_task(process_invoice_background, db_invoice.id, AsyncSessionLocal)

    return db_invoice
