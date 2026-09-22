import pytest
from app.security.output_validation import validate_ai_output

def test_valid_output_is_accepted(): assert validate_ai_output({"answer":"ok", "sources":[], "confidence":.9}).confidence == .9
def test_empty_output_is_rejected():
    with pytest.raises(Exception): validate_ai_output({"answer":"", "sources":[], "confidence":.9})
def test_invalid_confidence_is_rejected():
    with pytest.raises(Exception): validate_ai_output({"answer":"ok", "sources":[], "confidence":2})
def test_sensitive_output_is_rejected():
    with pytest.raises(ValueError): validate_ai_output({"answer":"FAKE_API_KEY_12345", "sources":[], "confidence":.9})
def test_invalid_json_shape_is_rejected():
    with pytest.raises(Exception): validate_ai_output({"answer":"ok"})
