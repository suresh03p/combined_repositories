from tests.conftest import register, token
from app.rag.access_control import filter_documents
from app.auth.models import User, Role

def test_retrieval_filters_other_tenant():
    user=User("a", "A", "a@example.com", "hash", "tenant-a", Role.USER)
    assert [d["document_id"] for d in filter_documents(user, [{"document_id":"a", "tenant_id":"tenant-a", "owner_id":"a", "access_level":"shared"}, {"document_id":"b", "tenant_id":"tenant-b", "owner_id":"b", "access_level":"shared"}])] == ["a"]

def test_private_document_requires_owner():
    user=User("a", "A", "a@example.com", "hash", "tenant-a", Role.USER)
    assert filter_documents(user, [{"document_id":"private", "tenant_id":"tenant-a", "owner_id":"other", "access_level":"private"}]) == []

def test_conversation_cannot_cross_tenant(client):
    register(client, tenant_id="tenant-a"); headers={"Authorization": f"Bearer {token(client)}"}; conversation=client.post("/api/v1/chat", headers=headers, json={"message":"hello"}).json()["conversation_id"]
    register(client, email="b@example.com", tenant_id="tenant-b"); token_b=token(client, "b@example.com"); headers_b={"Authorization": f"Bearer {token_b}"}
    assert client.get(f"/api/v1/conversations/{conversation}", headers=headers_b).status_code == 404

def test_document_tenant_ids_exist():
    from app.main import DOCUMENTS
    assert all("tenant_id" in document for document in DOCUMENTS)
