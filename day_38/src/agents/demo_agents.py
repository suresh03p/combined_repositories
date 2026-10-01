"""Deterministic demo workers; all facts are illustrative, not research."""

import asyncio
from dataclasses import dataclass
from typing import Protocol

from src.orchestration.models import AgentResult


class Agent(Protocol):
    name: str

    async def run(self) -> AgentResult: ...


@dataclass
class DemoAgent:
    name: str
    category: str
    claim_name: str
    claim_value: object
    task: str
    delay_seconds: float = 0.05
    calculation: dict[str, float] | None = None

    async def run(self) -> AgentResult:
        await asyncio.sleep(self.delay_seconds)
        calculations = {self.claim_name: self.calculation} if self.calculation else {}
        return AgentResult(
            agent_name=self.name,
            category=self.category,
            claims={self.claim_name: self.claim_value},
            sources=["Synthetic demo fixture"],
            evidence=[self.task],
            citations=[f"DEMO:{self.name}"],
            calculations=calculations,
            tool_calls=[f"demo.lookup({self.claim_name})"],
        )


def build_demo_agents() -> list[Agent]:
    """Create workers with distinct tasks and a deliberate revenue conflict."""
    return [
        DemoAgent(
            "research_1_revenue", "research", "revenue_inr_crore", 20,
            "Research task 1: inspect the illustrative revenue figure.",
        ),
        DemoAgent(
            "research_2_market", "research", "market_growth_percent", 8.2,
            "Research task 2: inspect the illustrative market growth figure.",
        ),
        DemoAgent(
            "research_3_sources", "research", "source_count", 3,
            "Research task 3: count the synthetic supporting source records.",
        ),
        DemoAgent(
            "rag_agent", "rag", "revenue_inr_crore", 25,
            "Retrieve the illustrative revenue figure from the demo knowledge base.",
        ),
        DemoAgent(
            "document_agent", "document", "reporting_period", "FY2025",
            "Extract the reporting period from the synthetic document.",
        ),
        DemoAgent(
            "analytics_agent", "analytics", "revenue_growth_percent", 10.0,
            "Calculate illustrative growth from 100 to 110.",
            calculation={"expected": 10.0, "actual": 10.0, "tolerance": 0.000001},
        ),
    ]