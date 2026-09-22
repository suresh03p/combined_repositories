from app.auth.models import Role
from tests.conftest import register, token

def test_user_cannot_upload_documents(client):
    register(client); assert client.post("/api/v1/documents/process", headers={"Authorization": f"Bearer {token(client)}"}, json={"content": "hello"}).status_code == 403

def test_unauthenticated_upload_is_rejected(client):
    assert client.post("/api/v1/documents/process", json={"content": "hello"}).status_code == 401

def test_user_can_chat(client):
    register(client); assert client.post("/api/v1/chat", headers={"Authorization": f"Bearer {token(client)}"}, json={"message": "What are support hours?"}).status_code == 200

def test_user_can_read_own_conversation(client):
    register(client); headers={"Authorization": f"Bearer {token(client)}"}; conversation=client.post("/api/v1/chat", headers=headers, json={"message":"hello"}).json()["conversation_id"]
    assert client.get(f"/api/v1/conversations/{conversation}", headers=headers).status_code == 200

def test_unknown_job_is_rejected(client):
    register(client); assert client.get("/api/v1/jobs/nope", headers={"Authorization": f"Bearer {token(client)}"}).status_code == 404
