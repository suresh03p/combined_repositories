from fastapi import HTTPException
from app.auth.models import User
from app.auth.permissions import can_use_tool

def execute_tool(user: User, tool: str, argument: str = "") -> dict:
    if not can_use_tool(user, tool):
        raise HTTPException(403, f"Tool not allowed for role {user.role.value}")
    if tool == "calculator":
        return {"tool": tool, "result": "calculator execution approved"}
    return {"tool": tool, "result": "execution approved", "argument": argument}
