from app.agents.state import AgentState


class Planner:
    def create_plan(self, state: AgentState) -> list[str]:
        message = state.user_message.lower()
        if any(operator in message for operator in ("+", "-", "*", "/")):
            return ["calculator"]
        if "date" in message or "today" in message or "time" in message:
            return ["date"]
        return ["respond"]
