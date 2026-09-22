from dataclasses import dataclass
from enum import Enum

class Role(str, Enum):
    USER = "USER"
    AI_OPERATOR = "AI_OPERATOR"
    ADMIN = "ADMIN"

@dataclass
class User:
    id: str
    name: str
    email: str
    password_hash: str
    tenant_id: str
    role: Role = Role.USER
