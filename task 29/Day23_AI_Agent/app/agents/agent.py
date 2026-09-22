from uuid import uuid4

from app.agents.executor import Executor
from app.agents.limits import AgentLimits
from app.agents.planner import Planner
from app.agents.state import AgentState
from app.memory.conversation import ConversationMemory
from app.observability.agent_logs import AgentLogger
from app.tools.registry import ToolRegistry


class Agent:
    def __init__(self) -> None:
        self.memory = ConversationMemory()
        self.planner = Planner()
        self.executor = Executor(ToolRegistry.default(), AgentLimits())
        self.logger = AgentLogger()

    def run(self, message: str, conversation_id: str | None = None) -> dict[str, str | int]:
        conversation_id = conversation_id or str(uuid4())
        state = AgentState(conversation_id=conversation_id, user_message=message)
        state.plan = self.planner.create_plan(state)
        result = self.executor.execute(state)
        self.memory.add(conversation_id, "user", message)
        self.memory.add(conversation_id, "assistant", result.response)
        self.logger.record(result)
        return {"conversation_id": conversation_id, "response": result.response, "steps": result.steps}
