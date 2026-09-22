import os
from datetime import datetime, timedelta, timezone
import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from .models import User

SECRET = os.getenv("JWT_SECRET", "development-only-change-me")
ALGORITHM = "HS256"
_bearer = HTTPBearer(auto_error=False)

def create_access_token(user: User, expires_minutes: int = 30) -> str:
    now = datetime.now(timezone.utc)
    payload = {"sub": user.id, "tenant_id": user.tenant_id, "role": user.role.value, "iat": now, "exp": now + timedelta(minutes=expires_minutes)}
    return jwt.encode(payload, SECRET, algorithm=ALGORITHM)

def get_current_user(credentials: HTTPAuthorizationCredentials | None = Depends(_bearer)) -> User:
    if not credentials:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Missing bearer token", headers={"WWW-Authenticate": "Bearer"})
    try:
        payload = jwt.decode(credentials.credentials, SECRET, algorithms=[ALGORITHM])
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Invalid or expired token", headers={"WWW-Authenticate": "Bearer"})
    from app.main import USERS
    user = USERS.get(payload.get("sub"))
    if not user or payload.get("tenant_id") != user.tenant_id or payload.get("role") != user.role.value:
        raise HTTPException(status_code=401, detail="Invalid token subject")
    return user
