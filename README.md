# AutoInvoiceGenerator - Automated Invoicing Microservice (aka InvoiceForge)

An asynchronous REST API built with FastAPI, PostgreSQL, Jinja2, and WeasyPrint that automates corporate billing by processing invoice payloads, generating PDF documents, and emailing clients.

## Key Features
- **Instant Response Latency:** Offloads PDF rendering and email delivery to async background workers (`202 Accepted`).
- **Template-Based Styling:** Uses HTML/CSS templates via Jinja2 to render clear corporate PDF invoices.
- **Secure by Default:** Enforces header-based API key authentication (`X-API-Key`).
- **DevOps Ready:** Full Docker, Docker Compose, and automated test suite included.

## Quick Start (Docker)

1. Clone repository:
   ```bash
   git clone https://github.com/mmesomasaint/autoinvoicegenerator.git
   cd autoinvoicegenerator
   ```
   
2. Run Docker:
   ```bash
   docker-compose -f devops/docker-compose.yml up --build
   ```
   
3. Submit a test invoice payload:
   ```bash
   curl -X POST "http://localhost:8000/api/v1/invoices" \
     -H "Content-Type: application/json" \
     -H "X-API-Key: prod_secure_api_key_8899" \
     -d '{
           "client_name": "Logistics Corp",
           "client_email": "accounting@logisticscorp.com",
           "tax_rate": 0.075,
           "items": [
             {"description": "Freight Service", "quantity": 1, "unit_price": 1200.00}
           ]
         }'
   ```
   
4. View sent emails and PDF attachments: Open http://localhost:8025 in your browser (Mailpit Web UI).
   
5. Running tests:
   ```bash
   pytest -v
   ```
