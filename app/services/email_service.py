# app/services/email_service.py
import aiosmtplib
from email.message import EmailMessage
import os

async def send_invoice_email(
    client_email: str, 
    invoice_id: str, 
    pdf_path: str = None,
    sender_name: Optional[str] = None,
    sender_email: Optional[str] = None,
    copy_to_email: Optional[str] = None,
):
    """Sends an email over local SMTP to be caught by Mailpit/MailHog"""
    
    message = EmailMessage()
    # Resolve dynamic values vs system fallbacks
    from_name = sender_name or settings.EMAILS_FROM_NAME
    from_address = sender_email or settings.EMAILS_FROM_EMAIL
    
    message["From"] = f"{from_name} <{from_address}>"
    message["To"] = client_email
    
    if copy_to_email:
        message["Bcc"] = copy_to_email

    message["Subject"] = f"Invoice #{invoice_id} from {from_name} is Ready"

   # Body formatted cleanly using runtime variables
    message.set_content(
        f"Hello {client_name},\n\n"
        f"Please find attached Invoice #{invoice_id}.\n\n"
        f"Thank you for your business!\n\n"
        f"Best regards,\n"
        f"{from_name}"
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
