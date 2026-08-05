# app/services/pdf_service.py
import os
from jinja2 import Environment, FileSystemLoader
from weasyprint import HTML
from app.config import settings

class PDFService:
    def __init__(self):
        template_dir = os.path.join(os.path.dirname(__file__), "../templates")
        self.jinja_env = Environment(loader=FileSystemLoader(template_dir))

    def generate_invoice_pdf(self, invoice_data: dict, output_path: str) -> str:
        """Compiles Jinja2 template and writes compiled PDF file to disk."""
        template = self.jinja_env.get_template("invoice.html")
        rendered_html = template.render(invoice=invoice_data)
        
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        HTML(string=rendered_html).write_pdf(output_path)
        return output_path

pdf_service = PDFService()
