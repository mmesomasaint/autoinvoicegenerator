# tests/test_api.py
import pytest
from app.config import settings

@pytest.mark.asyncio
async def test_create_invoice_unauthorized(client):
    """Verifies that requests without a valid API Key header are rejected."""
    response = await client.post("/api/v1/invoices", json={})
    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid or missing X-API-Key security header."

@pytest.mark.asyncio
async def test_create_invoice_success(client, monkeypatch):
    """Tests complete invoice payload acceptance and calculation accuracy."""
    
    # Mock external email sending during automated test execution
    async def mock_send_email(*args, **kwargs):
        return True
    
    monkeypatch.setattr("app.services.email_service.send_invoice_email", mock_send_email)

    payload = {
        "client_name": "Test Enterprise",
        "client_email": "billing@test.com",
        "tax_rate": 0.10,
        "items": [
            {"description": "Cloud Hosting", "quantity": 2, "unit_price": 50.0},
            {"description": "Domain Name", "quantity": 1, "unit_price": 20.0}
        ]
    }
    
    headers = {"X-API-Key": settings.API_KEY}
    response = await client.post("/api/v1/invoices", json=payload, headers=headers)
    
    assert response.status_code == 202
    data = response.json()
    assert data["client_name"] == "Test Enterprise"
    assert data["subtotal"] == 120.0  # (2*50) + (1*20)
    assert data["tax"] == 12.0        # 10% of 120
    assert data["total"] == 132.0      # 120 + 12
    assert data["status"] == "PENDING"
