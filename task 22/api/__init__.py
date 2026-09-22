"""
API Package
FastAPI integration for multi-agent system.
"""

from .agent_api import MultiAgentAPI, create_fastapi_app

__all__ = ['MultiAgentAPI', 'create_fastapi_app']
