"""Supervisor-driven sequential workflow and failure recovery."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import Any

from src.agent_registry import AgentRegistry
from src.agents.analyst import AnalystAgent
from src.agents.common import AgentError, InvalidAgentResponse, MissingContextError
from src.agents.rag_agent import RAGAgent
from src.agents.researcher import ResearchAgent
from src.agents.validator import ValidatorAgent
from src.agents.writer import WriterAgent
from src.memory.shared_state import SharedState
from src.tools.registry import ToolRegistry, create_default_tool_registry


class Supervisor:
    _STAGES = (
        ("research", "researcher"),
        ("retrieval", "rag"),
        ("analysis", "analyst"),
        ("validation", "validator"),
        ("writing", "writer"),
    )

    def __init__(
        self,
        tools: ToolRegistry | None = None,
        max_retries: int = 1,
    ) -> None:
        self.tools = tools or create_default_tool_registry()
        self.max_retries = max(0, max_retries)
        self.researcher = ResearchAgent(self.tools)
        self.registry = AgentRegistry()
        self.registry.register("researcher", self.researcher, {"research"})
        self.registry.register("rag", RAGAgent(self.tools), {"retrieval"})
        self.registry.register("analyst", AnalystAgent(self.tools), {"analysis"})
        self.registry.register("validator", ValidatorAgent(self.tools), {"validation"})
        self.registry.register("writer", WriterAgent(), {"writing"})
        self._faults: dict[str, str | list[str]] = {}
        self._decisions: list[dict[str, str]] = []
        self._trace: list[dict[str, Any]] = []

    def assign_task(self, task: str) -> str:
        """Choose the registered agent that owns a task capability."""
        return self.registry.assign(task)

    def _next_fault(self, agent_name: str) -> str | None:
        fault = self._faults.get(agent_name)
        if isinstance(fault, list):
            return fault.pop(0) if fault else None
        return fault

    def _run_once(self, agent_name: str, state: SharedState) -> dict[str, Any]:
        fault = self._next_fault(agent_name)
        if fault in {"fail", "research_failure", "rag_failure"}:
            raise AgentError(f"Simulated {agent_name} failure")
        if fault == "timeout":
            raise TimeoutError(f"Simulated {agent_name} timeout")
        if fault == "missing_context":
            raise MissingContextError(f"Simulated missing context for {agent_name}")
        if fault == "invalid_response":
            response: Any = {"agent": agent_name, "status": "invalid"}
        else:
            response = self.registry.get(agent_name).run(state)
        if (
            not isinstance(response, dict)
            or response.get("agent") != agent_name
            or response.get("status") != "success"
        ):
            raise InvalidAgentResponse(f"{agent_name} returned an invalid response")
        return response

    def _execute_stage(self, agent_name: str, state: SharedState) -> dict[str, Any] | None:
        for attempt in range(1, self.max_retries + 2):
            try:
                response = self._run_once(agent_name, state)
                self._trace.append(
                    {"agent": agent_name, "status": "success", "attempt": attempt}
                )
                return response
            except (AgentError, TimeoutError, ValueError) as error:
                self._trace.append(
                    {
                        "agent": agent_name,
                        "status": "retrying" if attempt <= self.max_retries else "failed",
                        "attempt": attempt,
                        "error": str(error),
                    }
                )
                if attempt <= self.max_retries:
                    self._decisions.append(
                        {"agent": agent_name, "decision": "retry", "reason": str(error)}
                    )
                    continue
                return self._recover(agent_name, state, error)
        return None

    def _recover(
        self,
        agent_name: str,
        state: SharedState,
        error: Exception,
    ) -> dict[str, Any] | None:
        if agent_name == "researcher":
            self._decisions.append(
                {"agent": agent_name, "decision": "skip", "reason": str(error)}
            )
            state.write("supervisor", "research", {
                "agent": "researcher", "status": "skipped", "sources": [], "findings": []
            })
            return {"agent": agent_name, "status": "skipped"}
        if agent_name == "rag":
            try:
                delegated = self.researcher.provide_retrieval(
                    state.read("supervisor", "question"),
                    state.read("supervisor", "research"),
                )
                state.write("supervisor", "retrieval", delegated)
                self._decisions.append(
                    {"agent": agent_name, "decision": "delegate", "to": "researcher", "reason": str(error)}
                )
                self._trace.append(
                    {"agent": "researcher", "status": "delegated_retrieval", "attempt": 1}
                )
                return {"agent": "researcher", "status": "success", **delegated}
            except MissingContextError as delegation_error:
                error = delegation_error
        self._decisions.append(
            {"agent": agent_name, "decision": "stop", "reason": str(error)}
        )
        return None

    def run(
        self,
        question: str,
        failure_plan: Mapping[str, str | Sequence[str]] | None = None,
    ) -> dict[str, Any]:
        if not question.strip():
            raise ValueError("question must not be empty")
        self._faults = {
            name: list(fault) if not isinstance(fault, str) else fault
            for name, fault in (failure_plan or {}).items()
        }
        self._decisions = []
        self._trace = []
        state = SharedState(question)

        for task, fallback_agent in self._STAGES:
            agent_name = self.assign_task(task) if task != "writing" else fallback_agent
            response = self._execute_stage(agent_name, state)
            if response is None:
                return {
                    "status": "failed",
                    "question": question,
                    "failed_agent": agent_name,
                    "decisions": self._decisions,
                    "trace": self._trace,
                }
            if task == "validation" and not response.get("validated"):
                self._decisions.append(
                    {"agent": agent_name, "decision": "stop", "reason": "Validation rejected the result"}
                )
                return {
                    "status": "failed",
                    "question": question,
                    "failed_agent": agent_name,
                    "validation": response,
                    "decisions": self._decisions,
                    "trace": self._trace,
                }

        draft = state.read("supervisor", "draft")
        result = {
            "status": "success",
            "question": question,
            "research": state.read("supervisor", "research"),
            "sources": state.read("supervisor", "retrieval")["citations"],
            "analysis": state.read("supervisor", "analysis"),
            "validation": state.read("supervisor", "validation"),
            "answer": draft["answer"],
            "decisions": self._decisions,
            "trace": self._trace,
        }
        state.write("supervisor", "result", result)
        return state.read("supervisor", "result")