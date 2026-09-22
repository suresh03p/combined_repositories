from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_health_is_public():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}


def test_ready_reports_environment():
    response = client.get("/ready")

    assert response.status_code == 200
    assert response.json()["status"] == "ready"


def test_chat_accepts_a_message():
    response = client.post("/chat", json={"message": "Hello"})

    assert response.status_code == 200
    assert "Hello" in response.json()["response"]


def test_rag_returns_sources():
    response = client.post("/rag/query", json={"query": "deployment"})

    assert response.status_code == 200
    assert response.json()["sources"] == []


def test_job_status_is_available():
    response = client.get("/jobs/example-job")

    assert response.status_code == 200
    assert response.json() == {"job_id": "example-job", "status": "completed"}
