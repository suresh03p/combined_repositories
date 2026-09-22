import pytest
from app.auth.models import User, Role
from app.agents.tool_permissions import execute_tool

def test_user_can_calculate(): assert execute_tool(User("u","U","u@e","h","t",Role.USER), "calculator")["tool"] == "calculator"
def test_user_cannot_query_database():
    with pytest.raises(Exception): execute_tool(User("u","U","u@e","h","t",Role.USER), "database_query")
def test_admin_can_query_database(): assert execute_tool(User("a","A","a@e","h","t",Role.ADMIN), "database_query")["tool"] == "database_query"
def test_operator_cannot_query_database():
    with pytest.raises(Exception): execute_tool(User("o","O","o@e","h","t",Role.AI_OPERATOR), "database_query")
