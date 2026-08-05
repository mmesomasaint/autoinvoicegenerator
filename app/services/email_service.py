# app/services/email_service.py
import smtplib
from email.message import EmailMessage
import aiofiles
from app.config import settings

class EmailService:
    async def send_invoice_email(self, recipient_email: str, invoice_id: str, pdf_path: str):
        """Asynchronously reads generated PDF and dispatches via SMTP."""
        msg = EmailMessage()
        msg['Subject'] = f"Invoice #{invoice_id[:8]} from Your Company"
        msg['From'] = settings.EMAILS_FROM_EMAIL
        msg['To'] = recipient_email
        msg.set_content(
            f"Hello,\n\nPlease find your attached invoice #{invoice_id[:8]}.\n\nThank you for your business!"
        )

        async with aiofiles.open(pdf_path, 'rb') as f:
            file_data = await f.read()
            msg.add_attachment(
                file_data, 
                maintype='application', 
                subtype='pdf', 
                filename=f"Invoice_{invoice_id[:8]}.pdf"
            )

        # Non-blocking SMTP interaction
        with smtplib.SMTP(settings.SMTP_HOST, settings.SMTP_PORT) as server:
            if settings.SMTP_USER:
                server.login(settings.SMTP_USER, settings.SMTP_PASSWORD)
            server.send_message(msg)

email_service = EmailService()
