from pydantic import BaseModel, ConfigDict, EmailStr, Field
from .models import Role

class RegisterRequest(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)
    tenant_id: str = Field(default="tenant-demo", min_length=1, max_length=100)

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: str
    name: str
    email: str
    tenant_id: str
    role: Role

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
