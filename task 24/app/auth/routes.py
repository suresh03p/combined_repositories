from fastapi import APIRouter, Depends, HTTPException, status
from .models import User
from .schemas import LoginRequest, RegisterRequest, TokenResponse, UserResponse
from .security import create_access_token, get_current_user
from app.security.password_security import hash_password, verify_password
from app.main import USERS

router = APIRouter(prefix="/api/v1/auth", tags=["auth"])

@router.post("/register", response_model=UserResponse, status_code=201)
def register(data: RegisterRequest):
    email = str(data.email).lower()
    if any(existing.email == email for existing in USERS.values()):
        raise HTTPException(409, "Email already registered")
    try:
        password_hash = hash_password(data.password)
    except ValueError as exc:
        raise HTTPException(422, str(exc))
    user = User(id=f"user-{len(USERS) + 1}", name=data.name, email=email, password_hash=password_hash, tenant_id=data.tenant_id)
    USERS[user.id] = user
    return user

@router.post("/login", response_model=TokenResponse)
def login(data: LoginRequest):
    user = next((item for item in USERS.values() if item.email == str(data.email).lower()), None)
    if not user or not verify_password(data.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials", headers={"WWW-Authenticate": "Bearer"})
    return TokenResponse(access_token=create_access_token(user))

@router.get("/me", response_model=UserResponse)
def me(user: User = Depends(get_current_user)):
    return user
