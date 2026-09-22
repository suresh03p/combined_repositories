from app.security.output_validation import validate_ai_output

def test_fake_password_is_not_returned():
    try: validate_ai_output({"answer":"FAKE_PASSWORD_123", "sources":[], "confidence":.5})
    except ValueError: pass
    else: raise AssertionError("sensitive value escaped output validation")
def test_health_endpoint_is_available(client): assert client.get("/health").json() == {"status":"ok"}
def test_auth_header_is_not_logged_by_audit_module():
    from app.core.logging import audit_event
    event=audit_event("/api/v1/chat", "success", "user-1", "tenant-a")
    assert "Authorization" not in event and "token" not in event
