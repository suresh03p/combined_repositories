import pytest
from fastapi.testclient import TestClient

from app.core.config import get_settings
from app.main import app


@pytest.fixture(autouse=True)
def test_settings(monkeypatch):
    monkeypatch.setenv("AUTH_USERNAME", "admin")
    monkeypatch.setenv("AUTH_PASSWORD", "change-me")
    monkeypatch.setenv("JWT_SECRET", "test-secret")
    get_settings.cache_clear()


@pytest.fixture
def client():
    with TestClient(app) as test_client:
        yield test_client


def auth_headers(client):
    response = client.post("/auth/login", json={"username": "admin", "password": "change-me"})
    return {"Authorization": f"Bearer {response.json()['access_token']}"}
