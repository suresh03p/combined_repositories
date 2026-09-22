from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)
HEADERS = {"Authorization": "Bearer change-me"}

def test_health_is_public():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"

def test_upload_process_chat_list_delete():
    upload = client.post("/documents/upload", headers=HEADERS, files={"file": ("policy.txt", b"Employees can apply for leave through the HR portal.", "text/plain")})
    assert upload.status_code == 202
    document_id = upload.json()["document_id"]
    assert client.get(f"/documents/{document_id}/status", headers=HEADERS).json()["status"] == "completed"
    chat = client.post("/chat", headers=HEADERS, json={"conversation_id": "CONV-001", "question": "How do I apply for leave?"})
    assert chat.status_code == 200
    assert chat.json()["sources"]
    assert client.get("/documents", headers=HEADERS).status_code == 200
    assert client.delete(f"/documents/{document_id}", headers=HEADERS).status_code == 204

def test_protected_endpoint_requires_token():
    assert client.get("/documents").status_code == 401

def test_chat_validation():
    response = client.post("/chat", headers=HEADERS, json={"conversation_id": "", "question": ""})
    assert response.status_code == 422
