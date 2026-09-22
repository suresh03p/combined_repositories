from app.agents.tool_permissions import execute_tool

def run_agent_tool(user, tool: str, argument: str = ""):
    """Keep tool authorization in application code before any tool runs."""
    return execute_tool(user, tool, argument)
