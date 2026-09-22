def test_root(client):
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"status": "success", "message": "AI API is running"}


def test_health(client):
    assert client.get("/health").json()["api"] == "healthy"


def test_health_subroutes(client):
    assert client.get("/health/database").json()["database"] == "healthy"
    assert client.get("/health/redis").json()["redis"] == "healthy"
    assert client.get("/health/ai").json()["ai_service"] == "healthy"


def test_chat_leave_policy(client):
    response = client.post("/api/v1/chat", json={"conversation_id": "CONV-001", "message": "What is the leave policy?"})
    assert response.status_code == 200
    assert response.json()["answer"] == "Employees receive 18 annual leave days."
    assert response.json()["sources"] == ["leave_policy.pdf"]


def test_chat_general_question(client):
    response = client.post("/api/v1/chat", json={"conversation_id": "CONV-002", "message": "Hello"})
    assert response.status_code == 200
    assert response.json()["status"] == "success"


def test_chat_stores_history(client):
    client.post("/api/v1/chat", json={"conversation_id": "CONV-003", "message": "One"})
    client.post("/api/v1/chat", json={"conversation_id": "CONV-003", "message": "Two"})
    response = client.get("/api/v1/conversations/CONV-003")
    assert len(response.json()["messages"]) == 4


def test_unknown_history_is_empty(client):
    assert client.get("/api/v1/conversations/unknown").json() == {"conversation_id": "unknown", "messages": []}


def test_blank_message_rejected(client):
    response = client.post("/api/v1/chat", json={"conversation_id": "CONV-004", "message": " "})
    assert response.status_code == 422


def test_missing_fields_rejected(client):
    assert client.post("/api/v1/chat", json={}).status_code == 422


def test_invalid_conversation_id_rejected(client):
    response = client.post("/api/v1/chat", json={"conversation_id": "bad id", "message": "Hi"})
    assert response.status_code == 422


def test_long_message_rejected(client):
    response = client.post("/api/v1/chat", json={"conversation_id": "CONV-005", "message": "x" * 4001})
    assert response.status_code == 422


def test_invalid_json_rejected(client):
    response = client.post("/api/v1/chat", content="not-json", headers={"content-type": "application/json"})
    assert response.status_code == 422


def test_cache_response(client):
    payload = {"conversation_id": "CONV-006", "message": "What is the leave policy?"}
    first = client.post("/api/v1/chat", json=payload)
    second = client.post("/api/v1/chat", json=payload)
    assert first.json()["answer"] == second.json()["answer"]


def test_document_job_created(client):
    response = client.post("/api/v1/documents/process?document_name=handbook.pdf")
    assert response.status_code == 202
    assert response.json()["status"] == "queued"


def test_job_status(client):
    created = client.post("/api/v1/documents/process").json()
    response = client.get(f"/api/v1/jobs/{created['job_id']}")
    assert response.status_code == 200
    assert response.json()["status"] == "queued"


def test_unknown_job(client):
    assert client.get("/api/v1/jobs/missing").status_code == 404


def test_ten_messages(client):
    for index in range(5):
        client.post("/api/v1/chat", json={"conversation_id": "CONV-007", "message": f"Question {index}"})
    assert len(client.get("/api/v1/conversations/CONV-007").json()["messages"]) == 10


def test_docs_available(client):
    assert client.get("/docs").status_code == 200


def test_response_has_conversation_id(client):
    response = client.post("/api/v1/chat", json={"conversation_id": "CONV-008", "message": "Hi"})
    assert response.json()["conversation_id"] == "CONV-008"


def test_multiple_conversations_are_isolated(client):
    client.post("/api/v1/chat", json={"conversation_id": "CONV-A", "message": "A"})
    client.post("/api/v1/chat", json={"conversation_id": "CONV-B", "message": "B"})
    assert len(client.get("/api/v1/conversations/CONV-A").json()["messages"]) == 2
    assert len(client.get("/api/v1/conversations/CONV-B").json()["messages"]) == 2


def test_empty_document_name_uses_default(client):
    response = client.post("/api/v1/documents/process?document_name=")
    assert response.status_code == 202


def test_health_shape(client):
    assert set(client.get("/health").json()) == {"api", "database", "redis", "ai_service"}
