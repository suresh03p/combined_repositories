from datetime import datetime, timedelta, timezone
import jwt
from app.auth.security import SECRET, ALGORITHM
from tests.conftest import register, token

def test_register_hashes_password(client):
    register(client)
    from app.main import USERS
    assert USERS["user-1"].password_hash != "StrongPassword123!"

def test_login_returns_bearer_token(client):
    register(client); response = client.post("/api/v1/auth/login", json={"email": "user@example.com", "password": "StrongPassword123!"})
    assert response.status_code == 200 and response.json()["token_type"] == "bearer"

def test_wrong_password_is_rejected(client):
    register(client); assert client.post("/api/v1/auth/login", json={"email": "user@example.com", "password": "WrongPassword123!"}).status_code == 401

def test_missing_token_is_rejected(client):
    assert client.get("/api/v1/auth/me").status_code == 401

def test_invalid_token_is_rejected(client):
    assert client.get("/api/v1/auth/me", headers={"Authorization": "Bearer invalid"}).status_code == 401

def test_expired_token_is_rejected(client):
    register(client)
    expired = jwt.encode({"sub": "user-1", "tenant_id": "tenant-a", "role": "USER", "exp": datetime.now(timezone.utc) - timedelta(minutes=1)}, SECRET, algorithm=ALGORITHM)
    assert client.get("/api/v1/auth/me", headers={"Authorization": f"Bearer {expired}"}).status_code == 401

def test_me_returns_authenticated_user(client):
    register(client); assert client.get("/api/v1/auth/me", headers={"Authorization": f"Bearer {token(client)}"}).json()["email"] == "user@example.com"
