from tests.conftest import auth_headers


def test_health(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}


def test_readiness(client):
    response = client.get("/ready")
    assert response.status_code == 200
    assert response.json()["status"] == "ready"


def test_login_and_protected_chat(client):
    headers = auth_headers(client)
    response = client.post("/chat", json={"message": "hello"}, headers=headers)
    assert response.status_code == 200
    assert "hello" in response.json()["answer"]
    assert response.headers["X-Request-ID"].startswith("req-")


def test_unauthorized_chat(client):
    assert client.post("/chat", json={"message": "hello"}).status_code == 401


def test_rag(client):
    response = client.post("/rag/query", json={"question": "What?", "documents": ["A fact"]}, headers=auth_headers(client))
    assert response.status_code == 200
    assert "A fact" in response.json()["answer"]


def test_invalid_and_oversized_requests(client):
    assert client.post("/chat", json={"message": ""}, headers=auth_headers(client)).status_code == 422
    oversized = "x" * 1_100_000
    assert client.post("/chat", content=oversized, headers={**auth_headers(client), "content-type": "application/json"}).status_code == 413
