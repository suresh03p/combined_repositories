from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health_api():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}


def test_readiness_api():
    response = client.get("/ready")
    assert response.status_code == 200
    assert response.json() == {"status": "ready"}


def test_authentication_success():
    response = client.post(
        "/auth/login",
        json={"username": "admin", "password": "secret123"},
    )
    assert response.status_code == 200
    assert response.json()["token"] == "demo-token"


def test_authentication_failure():
    response = client.post(
        "/auth/login",
        json={"username": "admin", "password": "wrongpass"},
    )
    assert response.status_code == 401


def test_chat_api():
    response = client.post(
        "/chat",
        json={"message": "hello from ci pipeline", "user_id": "u1"},
    )
    assert response.status_code == 200
    assert "reply" in response.json()


def test_rag_api():
    response = client.post(
        "/rag/query",
        json={"query": "what is ai?", "limit": 2},
    )
    assert response.status_code == 200
    assert len(response.json()["results"]) == 2


def test_redis_related_functionality():
    response = client.get("/redis/status")
    assert response.status_code == 200
    assert response.json()["redis"] == "working"


def test_input_validation():
    response = client.post("/chat", json={"message": ""})
    assert response.status_code == 400


def test_error_handling():
    response = client.get("/error-demo")
    assert response.status_code == 500
    assert "Simulated backend failure" in response.text
