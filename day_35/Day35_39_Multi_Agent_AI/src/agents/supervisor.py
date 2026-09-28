from typing import Any

from src.agents.analyst import AnalysisAgent
from src.agents.rag_agent import RAGAgent
from src.agents.researcher import ResearchAgent
from src.agents.validator import ValidationAgent
from src.agents.writer import WriterAgent
from src.orchestration.state import AgentState


class SupervisorAgent:
    """Own the workflow, accept each result, then choose the next agent."""

    def __init__(
        self,
        researcher: ResearchAgent | None = None,
        rag_agent: RAGAgent | None = None,
        analyst: AnalysisAgent | None = None,
        validator: ValidationAgent | None = None,
        writer: WriterAgent | None = None,
    ) -> None:
        self.researcher = researcher or ResearchAgent()
        self.rag_agent = rag_agent or RAGAgent()
        self.analyst = analyst or AnalysisAgent()
        self.validator = validator or ValidationAgent()
        self.writer = writer or WriterAgent()
        self.handoffs: list[dict[str, Any]] = []

    def run(self, state: AgentState) -> AgentState:
        self.handoffs = []
        if not state.user_request.strip():
            state.task_status = "failed"
            state.errors.append("The user request must not be empty.")
            return state

        state.task_status = "running"
        try:
            next_agent = self._decide_next(state)
            while next_agent is not None:
                state.current_agent = next_agent
                self.handoffs.append({
                    "from": "supervisor",
                    "to": next_agent,
                    "decision": f"Run {next_agent} for the current workflow stage.",
                })

                result = self._run_agent(next_agent, state)
                self._accept_result(next_agent, result, state)
                state.current_agent = "supervisor"
                self.handoffs.append({
                    "from": next_agent,
                    "to": "supervisor",
                    "result_received": self._result_summary(next_agent, result),
                })

                # The next dispatch is chosen only after the result is in shared state.
                next_agent = self._decide_next(state)

            state.task_status = "completed"
        except Exception as error:
            state.current_agent = "supervisor"
            state.task_status = "failed"
            state.errors.append(f"{type(error).__name__}: {error}")
        return state

    def _decide_next(self, state: AgentState) -> str | None:
        completed_agents = {
            handoff["from"]
            for handoff in self.handoffs
            if handoff.get("to") == "supervisor"
        }
        if "researcher" not in completed_agents:
            return "researcher"
        if "rag_agent" not in completed_agents:
            return "rag_agent"
        if "analyst" not in completed_agents:
            return "analyst"
        if "validator" not in completed_agents:
            return "validator"
        if "writer" not in completed_agents:
            return "writer"
        return None

    def _run_agent(self, agent_name: str, state: AgentState) -> Any:
        if agent_name == "researcher":
            return self.researcher.run(state.user_request)
        if agent_name == "rag_agent":
            return self.rag_agent.run(state.user_request)
        if agent_name == "analyst":
            return self.analyst.run(state)
        if agent_name == "validator":
            return self.validator.run(state)
        if agent_name == "writer":
            return self.writer.run(state)
        raise ValueError(f"Unknown agent: {agent_name}")

    @staticmethod
    def _accept_result(agent_name: str, result: Any, state: AgentState) -> None:
        if agent_name == "researcher":
            state.research_results = result
        elif agent_name == "rag_agent":
            state.retrieved_documents = result
        elif agent_name == "analyst":
            state.analysis_results = result
        elif agent_name == "validator":
            state.validation_results = result
        elif agent_name == "writer":
            state.final_response = result
        else:
            raise ValueError(f"Unknown agent: {agent_name}")

    @staticmethod
    def _result_summary(agent_name: str, result: Any) -> str:
        if agent_name in {"researcher", "rag_agent"}:
            return f"{len(result)} evidence item(s)"
        if agent_name == "validator":
            return "passed" if result.get("is_valid") else "issues found"
        if agent_name == "writer":
            return "final response produced"
        return "analysis produced"
