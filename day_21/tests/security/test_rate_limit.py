import pytest
from fastapi import HTTPException
from app.security.rate_limit import check_rate_limit, reset_rate_limits

def test_first_ten_requests_allowed():
    reset_rate_limits()
    for _ in range(10): check_rate_limit("user")
def test_eleventh_request_blocked():
    reset_rate_limits()
    for _ in range(10): check_rate_limit("user")
    with pytest.raises(HTTPException) as error: check_rate_limit("user")
    assert error.value.status_code == 429
def test_users_have_separate_buckets():
    reset_rate_limits()
    for _ in range(10): check_rate_limit("user-a")
    check_rate_limit("user-b")
