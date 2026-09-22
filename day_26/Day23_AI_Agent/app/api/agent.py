from fastapi import APIRouter
from pydantic import BaseModel, Field

from app.agents.agent import Agent

router = APIRouter(tags=["agent"])
agent = Agent()


class AgentRequest(BaseModel):
    message: str = Field(min_length=1)
    conversation_id: str | None = None


class AgentResponse(BaseModel):
    conversation_id: str
    response: str
    steps: int


@router.post("/agent", response_model=AgentResponse)
def run_agent(request: AgentRequest) -> AgentResponse:
    result = agent.run(request.message, request.conversation_id)
    return AgentResponse(**result)
