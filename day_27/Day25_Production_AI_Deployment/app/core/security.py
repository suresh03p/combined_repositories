import base64
import hashlib
import hmac
import time


def create_token(username: str, secret: str) -> str:
    payload = f"{username}:{int(time.time()) + 3600}"
    signature = hmac.new(secret.encode(), payload.encode(), hashlib.sha256).hexdigest()
    return base64.urlsafe_b64encode(f"{payload}:{signature}".encode()).decode()


def verify_token(token: str, secret: str) -> str | None:
    try:
        decoded = base64.urlsafe_b64decode(token.encode()).decode()
        username, expiry, signature = decoded.rsplit(":", 2)
        expected = hmac.new(secret.encode(), f"{username}:{expiry}".encode(), hashlib.sha256).hexdigest()
        if not hmac.compare_digest(signature, expected) or int(expiry) < time.time():
            return None
        return username
    except (ValueError, TypeError, UnicodeError):
        return None
