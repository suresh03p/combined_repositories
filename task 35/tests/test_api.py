from fastapi.testclient import TestClient

from app.api.inference import app


client = TestClient(app)


def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_inference_success():
    response = client.post("/inference", json={"text": "I cannot log into my account."})
    assert response.status_code == 200
    body = response.json()
    assert "prediction" in body
    assert body["model_version"]


def test_invalid_input_rejected():
    response = client.post("/inference", json={"text": ""})
    assert response.status_code == 422
