# app/services/email_service.py
import aiosmtplib
from email.message import EmailMessage
import os

async def send_invoice_email(client_email: str, invoice_id: str, pdf_path: str = None):
    """Sends an email over local SMTP to be caught by Mailpit/MailHog"""
    
    message = EmailMessage()
    message["From"] = "billing@yourcompany.com"
    message["To"] = client_email
    message["Subject"] = f"Your Invoice #{invoice_id} is Ready"
    
    message.set_content(
        f"Hello,\n\nThank you for your business. "
        f"Your invoice #{invoice_id} has been generated."
    )

    # Attach the HTML/PDF file if it exists
    if pdf_path and os.path.exists(pdf_path):
        with open(pdf_path, 'rb') as f:
            file_data = f.read()
            message.add_attachment(
                file_data, 
                maintype='application', 
                subtype='pdf', 
                filename=os.path.basename(pdf_path)
            )

    try:
        # Port 1025 is the default SMTP port for Mailpit and MailHog
        await aiosmtplib.send(
            message,
            hostname="127.0.0.1",
            port=1025
        )
        print(f"Real email successfully dispatched to {client_email}")
    except Exception as e:
        print(f"Failed to send email: {e}")
