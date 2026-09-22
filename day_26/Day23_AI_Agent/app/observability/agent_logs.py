import logging

from app.agents.state import AgentState

logger = logging.getLogger("day23.agent")


class AgentLogger:
    def record(self, state: AgentState) -> None:
        logger.info(
            "agent_run conversation_id=%s steps=%s plan=%s",
            state.conversation_id,
            state.steps,
            state.plan,
        )
