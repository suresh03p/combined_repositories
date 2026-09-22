"""
Sequential Workflow
Executes agents in sequence, passing results from one to the next.
"""

import json
from typing import Dict, Any
from agents.researcher import ResearchAgent
from agents.calculator import CalculatorAgent
from agents.writer import WriterAgent
from core.agent_state import AgentState, TaskStatus


class SequentialWorkflow:
    """
    Executes a workflow where agents run in sequence.
    
    Example:
    User Request → Research Agent → Calculator Agent → Writer Agent → Final Answer
    """
    
    def __init__(self):
        """Initialize the workflow."""
        self.research_agent = ResearchAgent()
        self.calculator_agent = CalculatorAgent()
        self.writer_agent = WriterAgent()
    
    def execute(self, user_request: str) -> Dict[str, Any]:
        """
        Execute the sequential workflow.
        
        Args:
            user_request: The user's request
            
        Returns:
            Dict with final answer and workflow state
        """
        print(f"\n{'='*60}")
        print(f"SEQUENTIAL WORKFLOW EXECUTION")
        print(f"{'='*60}\n")
        
        # Create state
        state = AgentState(user_request)
        state.set_pending_steps([
            "Research",
            "Calculator",
            "Writing"
        ])
        
        print(f"[Workflow] Request: {user_request}\n")
        
        # Step 1: Research
        print("[Workflow] → Step 1: Research Agent")
        research_result = self.research_agent.get_annual_leave_entitlement()
        state.add_research_result(research_result)
        state.record_step("Research Agent")
        
        # Get used leave
        used_leave_result = self.research_agent.get_employee_leave_used()
        used_leave = 6  # Example data
        
        # Step 2: Calculator
        print("\n[Workflow] → Step 2: Calculator Agent")
        annual_leave = research_result['annual_leave_days']
        calc_result = self.calculator_agent.calculate_remaining_leave(
            annual_leave, used_leave
        )
        state.add_calculation_result(calc_result)
        state.record_step("Calculator Agent")
        
        # Step 3: Writer
        print("\n[Workflow] → Step 3: Writer Agent")
        context = {
            "header": "LEAVE BALANCE REPORT",
            "annual_leave": annual_leave,
            "used_leave": used_leave,
            "remaining_leave": calc_result['remaining_leave'],
            "percentage_used": round((used_leave / annual_leave) * 100, 2),
            "percentage_remaining": round(100 - (used_leave / annual_leave) * 100, 2),
            "source": research_result['source']
        }
        
        writing_result = self.writer_agent.write_summary(context)
        state.add_writing_result(writing_result)
        state.record_step("Writer Agent")
        
        # Final state
        state.update_status(TaskStatus.COMPLETED)
        
        print(f"\n[Workflow] ✓ Workflow completed successfully\n")
        
        return {
            "status": "success",
            "conversation_id": state.conversation_id,
            "summary": writing_result['summary'],
            "state": state.to_dict()
        }


def run_sequential_example():
    """Run an example sequential workflow."""
    workflow = SequentialWorkflow()
    
    result = workflow.execute(
        "Find the annual leave allowance and calculate how many days "
        "remain if the employee has used 6 days."
    )
    
    print(result['summary'])
    
    return result


if __name__ == "__main__":
    run_sequential_example()
