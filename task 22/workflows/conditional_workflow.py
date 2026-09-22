"""
Conditional Routing
Routes tasks to appropriate agents based on task type.
"""

import json
from enum import Enum
from typing import Dict, Any
from agents.researcher import ResearchAgent
from agents.calculator import CalculatorAgent
from agents.writer import WriterAgent
from core.agent_state import AgentState


class TaskType(Enum):
    """Types of tasks that can be routed."""
    RESEARCH = "research"
    CALCULATION = "calculation"
    WRITING = "writing"
    COMPLEX = "complex"
    UNKNOWN = "unknown"


class TaskRouter:
    """
    Routes tasks to appropriate agents based on task type.
    
    Example:
    Question
       ↓
    Router
       │
       ├── "What is the leave policy?" → Research Agent
       ├── "What is 250 * 8?" → Calculator Agent
       ├── "Summarize this policy" → Writer Agent
       └── Complex queries → Multiple Agents
    """
    
    def __init__(self):
        """Initialize the router."""
        self.research_agent = ResearchAgent()
        self.calculator_agent = CalculatorAgent()
        self.writer_agent = WriterAgent()
        
        # Keywords for each task type
        self.research_keywords = [
            "find", "search", "look up", "policy", "document",
            "information", "what is", "definition", "explain", "describe"
        ]
        
        self.calculation_keywords = [
            "calculate", "compute", "add", "subtract", "multiply",
            "divide", "percentage", "total", "remaining", "math",
            "+", "-", "*", "/", "="
        ]
        
        self.writing_keywords = [
            "summarize", "summary", "write", "format", "generate",
            "report", "document", "create", "prepare"
        ]
    
    def classify_task(self, question: str) -> TaskType:
        """
        Classify a task based on its content.
        
        Args:
            question: The task/question to classify
            
        Returns:
            TaskType enum value
        """
        question_lower = question.lower()
        
        # Count keyword matches for each type
        research_score = sum(1 for kw in self.research_keywords if kw in question_lower)
        calculation_score = sum(1 for kw in self.calculation_keywords if kw in question_lower)
        writing_score = sum(1 for kw in self.writing_keywords if kw in question_lower)
        
        scores = {
            TaskType.RESEARCH: research_score,
            TaskType.CALCULATION: calculation_score,
            TaskType.WRITING: writing_score
        }
        
        # Check for complex task (multiple types)
        non_zero_scores = sum(1 for s in scores.values() if s > 0)
        if non_zero_scores > 1:
            return TaskType.COMPLEX
        
        # Find the highest scoring task type
        if research_score > calculation_score and research_score > writing_score:
            if research_score > 0:
                return TaskType.RESEARCH
        elif calculation_score > research_score and calculation_score > writing_score:
            if calculation_score > 0:
                return TaskType.CALCULATION
        elif writing_score > research_score and writing_score > calculation_score:
            if writing_score > 0:
                return TaskType.WRITING
        
        return TaskType.UNKNOWN
    
    def route_task(self, question: str) -> Dict[str, Any]:
        """
        Route a task to the appropriate agent.
        
        Args:
            question: The task/question to route
            
        Returns:
            Dict with routing decision and result
        """
        print(f"\n[Router] Classifying task: {question}")
        
        task_type = self.classify_task(question)
        
        print(f"[Router] Task type identified: {task_type.value}")
        
        state = AgentState(question)
        
        if task_type == TaskType.RESEARCH:
            return self._handle_research_task(question, state)
        elif task_type == TaskType.CALCULATION:
            return self._handle_calculation_task(question, state)
        elif task_type == TaskType.WRITING:
            return self._handle_writing_task(question, state)
        elif task_type == TaskType.COMPLEX:
            return self._handle_complex_task(question, state)
        else:
            return {
                "status": "error",
                "message": "Unable to classify task",
                "task": question,
                "conversation_id": state.conversation_id
            }
    
    def _handle_research_task(self, question: str, state: AgentState) -> Dict[str, Any]:
        """Handle a research task."""
        print(f"[Router] → Routing to Research Agent")
        
        result = self.research_agent.research(question)
        state.add_research_result(result)
        state.record_step("Research Agent")
        
        return {
            "status": "success",
            "task_type": TaskType.RESEARCH.value,
            "agent_used": "ResearchAgent",
            "result": result,
            "conversation_id": state.conversation_id
        }
    
    def _handle_calculation_task(self, question: str, state: AgentState) -> Dict[str, Any]:
        """Handle a calculation task."""
        print(f"[Router] → Routing to Calculator Agent")
        
        # Extract expression from question
        # Simple extraction: take numbers and operators
        import re
        expression = re.findall(r'[0-9+\-*/(). ]+', question)
        
        if expression:
            expr_str = expression[0].strip()
            result = self.calculator_agent.calculate(expr_str)
        else:
            result = {
                "status": "error",
                "message": "No valid expression found"
            }
        
        state.add_calculation_result(result)
        state.record_step("Calculator Agent")
        
        return {
            "status": "success",
            "task_type": TaskType.CALCULATION.value,
            "agent_used": "CalculatorAgent",
            "result": result,
            "conversation_id": state.conversation_id
        }
    
    def _handle_writing_task(self, question: str, state: AgentState) -> Dict[str, Any]:
        """Handle a writing task."""
        print(f"[Router] → Routing to Writer Agent")
        
        context = {
            "task": question,
            "notes": "Writing task processed by Writer Agent"
        }
        
        result = self.writer_agent.write_summary(context)
        state.add_writing_result(result)
        state.record_step("Writer Agent")
        
        return {
            "status": "success",
            "task_type": TaskType.WRITING.value,
            "agent_used": "WriterAgent",
            "result": result,
            "conversation_id": state.conversation_id
        }
    
    def _handle_complex_task(self, question: str, state: AgentState) -> Dict[str, Any]:
        """Handle a complex task requiring multiple agents."""
        print(f"[Router] → Complex task detected, routing to multiple agents")
        
        results = {
            "research": self.research_agent.research(question),
            "writing": self.writer_agent.write_summary({"task": question})
        }
        
        state.agent_results = results
        state.record_step("Multiple Agents")
        
        return {
            "status": "success",
            "task_type": TaskType.COMPLEX.value,
            "agents_used": ["ResearchAgent", "WriterAgent"],
            "results": results,
            "conversation_id": state.conversation_id
        }


def test_router():
    """Test the task router with various examples."""
    router = TaskRouter()
    
    test_cases = [
        "What is the leave policy?",
        "What is 250 * 8?",
        "Summarize this policy.",
        "Find the leave policy and calculate remaining leave."
    ]
    
    print(f"\n{'='*60}")
    print(f"TASK ROUTER TEST CASES")
    print(f"{'='*60}\n")
    
    for test in test_cases:
        result = router.route_task(test)
        print(f"\nQuestion: {test}")
        print(f"Task Type: {result.get('task_type', 'unknown')}")
        print(f"Agent Used: {result.get('agent_used', result.get('agents_used', 'unknown'))}")
        print("-" * 60)


if __name__ == "__main__":
    test_router()
