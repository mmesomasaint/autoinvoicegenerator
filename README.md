# AutoInvoiceGenerator (InvoiceForge)

An enterprise-grade, asynchronous REST API microservice built with **FastAPI**, **SQLAlchemy**, **PostgreSQL**, **Jinja2**, and **WeasyPrint**. The platform automates corporate billing workflows by processing structured invoice payloads, computing monetary values, compiling HTML/CSS templates into PDF documents, and dispatching transactional emails via background execution queues.

---

## Key Features

* **Non-Blocking Architecture:** Offloads CPU/IO-intensive operations (PDF rendering and SMTP mail dispatch) to asynchronous background workers, returning an immediate `202 Accepted` response.
* **Dynamic PDF Templating:** Utilizes Jinja2 and HTML/CSS templates to generate pixel-perfect, custom-branded corporate invoices.
* **Header-Based Authentication:** Protects production endpoints via strict `X-API-Key` middleware verification.
* **Multi-Environment Persistence:** Native support for persistent PostgreSQL (Production/Docker) and lightweight SQLite (Local Development).
* **Containerized Deployment:** Includes multi-stage production `Dockerfile` configurations and `docker-compose` orchestration for local and remote environments.
* **Comprehensive Test Suite:** Fully automated unit and integration tests powered by `pytest` and `httpx`.

---

## System Architecture & Flow

```text
[ Client Application ] ──► HTTP POST /api/v1/invoices (with X-API-Key Header)
                                    │
                                    ▼
                         [ FastAPI Gateway / Router ]
                                    │
               ┌────────────────────┴────────────────────┐
               ▼                                         ▼
   [ Save Invoice Record ]                    [ Return 202 Accepted ]
   Persists to PostgreSQL/SQLite              Immediate HTTP Response
               │
               ▼
   [ Async Background Worker ]
               │
               ├──────► [ PDF Engine ] ──► Compiles Jinja2 HTML -> PDF -> Disk Storage
               │
               └──────► [ SMTP Mailer ] ──► Dispatches Email + Attached PDF -> Client

```
## Local Development Setup (Without Docker)

Prerequisites
* Python 3.11+
* System dependencies for WeasyPrint (`cairo, pango, gdk-pixbuf`):
   * macOS: `brew install cairo pango gdk-pixbuf libffi`
   * Linux (Ubuntu/Debian): `sudo apt install python3-pip pango1.0-tools libcairo2 libpango-1.0-0`

Step 1: Environment Setup
Clone the repository and prepare a Python virtual environment:
```bash
git clone [https://github.com/mmesomasaint/autoinvoicegenerator.git](https://github.com/mmesomasaint/autoinvoicegenerator.git)
cd autoinvoicegenerator

python3 -m venv venv
source venv/bin/activate  # On Windows: .\venv\Scripts\activate
pip install -r requirements.txt
```

Step 2: Configuration
Create a `.env` file in the root directory by copying the template:
```bash
cp .env.example .env
```

Ensure your `.env` contains valid development configurations:
```bash
PROJECT_NAME="InvoiceForge Microservice"
ENVIRONMENT="development"
API_KEY="dev_secret_api_key_12345"
DATABASE_URL="sqlite+aiosqlite:///./dev_invoices.db"
SMTP_HOST="localhost"
SMTP_PORT=1025
EMAILS_FROM_EMAIL="billing@optima.local"
STORAGE_DIR="storage/invoices"
```

## Running & Testing locally

Step 1: Start Local Services
Open two separate terminal windows in your project root with your virtual environment activated (`source venv/bin/activate`):

* Terminal 1 (Mock SMTP Server):
  ```bash
  python3 -m aiosmtpd -n -l localhost:1025
  ```

* Terminal 2 (FastAPI Application Server):
  ```bash
  uvicorn app.main:app --reload --port 8000
  ```

Step 2: Interactive Testing via Swagger UI
1. Open your browser and navigate to `http://localhost:8000/docs`.
2. Click the green Authorize button in the top-right corner.
3. In the `X-API-Key` text box, enter your development key (`dev_secret_api_key_12345`) and click Authorize.
4. Expand the `POST /api/v1/invoices` endpoint and click Try it out.
5. Input a sample JSON request body:
   ```bash
   {
     "client_name": "Acme Enterprises",
     "client_email": "finance@acme.com",
     "tax_rate": 0.075,
     "sender_company_name": "Optima Logic Studio",
     "sender_email": "billing@optima.local",
     "items": [
       {
         "description": "Backend Architecture & Systems Design",
         "quantity": 10,
         "unit_price": 150.0
       }
     ]
   }
   ```
6. Click Execute.

Expected Verification:
* HTTP Response: Returns status `202` Accepted along with calculated monetary totals (`subtotal, tax, total`) and a generated UUID.
* Terminal 1 (SMTP Log): Displays the raw outgoing email dispatch payload.
* File System: Confirms creation of a compiled PDF document inside `storage/invoices/Invoice_<UUID>.pdf.`

Step 3: Testing via Terminal (cURL)
Execute a request directly using `curl`:

```bash
curl -X POST "http://localhost:8000/api/v1/invoices" \
     -H "Content-Type: application/json" \
     -H "X-API-Key: dev_secret_api_key_12345" \
     -d '{
           "client_name": "Global Tech Ltd",
           "client_email": "billing@globaltech.com",
           "tax_rate": 0.1,
           "items": [
             {"description": "API Integration Service", "quantity": 1, "unit_price": 500.0}
           ]
         }'
```

Step 4: Running Automated Tests
Run the full automated test suite (`unit and integration tests`):

```bash
pytest -v
```

## Docker Deployment
To spin up the complete production container stack (`API, PostgreSQL, and Mailpit SMTP UI`):

```bash
docker-compose -f devops/docker-compose.yml up --build
```
* API Docs: `http://localhost:8000/docs`
* Mailpit Web Dashboard: `http://localhost:8025`

## Project Structure

```Plaintext
autoinvoicegenerator/
├── app/
│   ├── api/             # API v1 route controllers & endpoints
│   ├── core/            # Database initialization & security middleware
│   ├── models/          # SQLAlchemy ORM entities
│   ├── schemas/         # Pydantic request/response validation schemas
│   ├── services/        # PDF generation, storage, & SMTP mail services
│   ├── templates/       # Jinja2 HTML/CSS invoice templates
│   ├── config.py        # Environment variables loader
│   └── main.py          # FastAPI application entry point & lifespan
├── devops/              # Dockerfile, docker-compose, and server configs
├── storage/             # Local file store for generated PDF artifacts
├── tests/               # Pytest suite & async client fixtures
├── .env.example         # Template environment settings
├── pytest.ini           # Pytest runner configuration
└── requirements.txt     # Python project dependencies

```
