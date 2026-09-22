from app.agents.tool_permissions import execute_tool

TOOLS = {
    "calculator": "low",
    "search_documents": "medium",
    "database_query": "high",
    "send_email": "high",
}

# The agent must call execute_tool after the user's role is authenticated.
