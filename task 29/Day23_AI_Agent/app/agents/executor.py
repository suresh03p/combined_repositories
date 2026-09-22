from app.agents.limits import AgentLimits, LimitExceededError
from app.agents.state import AgentState
from app.tools.registry import ToolRegistry


class Executor:
    def __init__(self, registry: ToolRegistry, limits: AgentLimits | None = None) -> None:
        self.registry = registry
        self.limits = limits or AgentLimits()

    def execute(self, state: AgentState) -> AgentState:
        for step in state.plan:
            if state.steps >= self.limits.max_steps:
                raise LimitExceededError("Agent step limit exceeded")
            state.steps += 1
            if step == "respond":
                state.observations.append(state.user_message)
            else:
                state.observations.append(self.registry.run(step, state.user_message))
        state.response = "\n".join(state.observations)
        return state
