import pytest
from fastapi.testclient import TestClient
from app.main import app, USERS, CONVERSATIONS, DOCUMENTS
from app.security.rate_limit import reset_rate_limits

@pytest.fixture(autouse=True)
def reset_state():
    USERS.clear(); CONVERSATIONS.clear(); reset_rate_limits()
    DOCUMENTS[:] = [
        {"document_id": "doc-a", "tenant_id": "tenant-a", "owner_id": "user-a", "access_level": "shared", "created_at": "2026-01-01", "content": "Company A policy support hours"},
        {"document_id": "doc-b", "tenant_id": "tenant-b", "owner_id": "user-b", "access_level": "shared", "created_at": "2026-01-01", "content": "Company B internal policy"},
    ]
    yield

@pytest.fixture
def client():
    return TestClient(app)

def register(client, email="user@example.com", tenant_id="tenant-a", password="StrongPassword123!"):
    response = client.post("/api/v1/auth/register", json={"name": "Test", "email": email, "tenant_id": tenant_id, "password": password})
    assert response.status_code == 201
    return response.json()

def token(client, email="user@example.com", password="StrongPassword123!"):
    return client.post("/api/v1/auth/login", json={"email": email, "password": password}).json()["access_token"]
