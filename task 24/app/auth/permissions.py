from fastapi import Depends, HTTPException
from .models import Role, User
from .security import get_current_user

ALLOWED_TOOLS = {
    Role.USER: {"search_documents", "calculator"},
    Role.AI_OPERATOR: {"search_documents", "calculator"},
    Role.ADMIN: {"search_documents", "calculator", "database_query"},
}

def require_roles(*roles: Role):
    def dependency(user: User = Depends(get_current_user)):
        if user.role not in roles:
            raise HTTPException(status_code=403, detail="Insufficient role")
        return user
    return dependency

def can_use_tool(user: User, tool: str) -> bool:
    return tool in ALLOWED_TOOLS.get(user.role, set())
