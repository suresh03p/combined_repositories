"""
Supervisor Agent
Orchestrates all other agents and manages the workflow.
"""

import json
from typing import Dict, Any, List
from agents.researcher import ResearchAgent
from agents.calculator import CalculatorAgent
from agents.writer import WriterAgent
from workflows.conditional_workflow import TaskRouter
from core.agent_state import AgentState, TaskStatus


class SupervisorAgent:
    """
    Supervisor Agent is responsible for:
    - Understanding the request
    - Breaking tasks into steps
    - Selecting appropriate agents
    - Sending tasks to agents
    - Receiving and combining results
    - Deciding next steps
    - Providing final answers
    
    Example:
    User Request
         ↓
    Supervisor
         ↓
    Step 1: Understand Request
         ↓
    Step 2: Break into steps
         ↓
    Step 3: Select agents
         ↓
    Step 4-6: Execute steps
         ↓
    Final Answer
    """
    
    def __init__(self, name: str = "SupervisorAgent"):
        """Initialize the supervisor."""
        self.name = name
        self.research_agent = ResearchAgent()
        self.calculator_agent = CalculatorAgent()
        self.writer_agent = WriterAgent()
        self.router = TaskRouter()
    
    def process_request(self, user_request: str) -> Dict[str, Any]:
        """
        Process a user request end-to-end.
        
        Args:
            user_request: The user's request
            
        Returns:
            Dict with final answer and execution trace
        """
        print(f"\n{'='*70}")
        print(f"SUPERVISOR AGENT - PROCESSING REQUEST")
        print(f"{'='*70}\n")
        
        # Step 1: Understand Request
        state = AgentState(user_request)
        print(f"[Supervisor] Received request: {user_request}\n")
        
        # Step 2: Break task into steps
        steps = self._break_down_task(user_request)
        state.set_pending_steps(steps)
        print(f"[Supervisor] Task decomposed into {len(steps)} steps:")
        for i, step in enumerate(steps, 1):
            print(f"  Step {i}: {step}")
        
        # Step 3-N: Execute steps
        print(f"\n[Supervisor] Beginning execution...\n")
        
        for i, step in enumerate(steps, 1):
            print(f"[Supervisor] → Executing Step {i}: {step}")
            self._execute_step(step, state)
            print()
        
        # Final: Generate answer
        print(f"[Supervisor] → Generating final answer")
        final_answer = self._generate_final_answer(state)
        
        state.update_status(TaskStatus.COMPLETED)
        
        print(f"\n{'='*70}")
        print(f"SUPERVISOR - TASK COMPLETE")
        print(f"{'='*70}\n")
        
        return {
            "status": "success",
            "conversation_id": state.conversation_id,
            "final_answer": final_answer,
            "state": state.to_dict(),
            "execution_summary": self._create_execution_summary(state)
        }
    
    def _break_down_task(self, request: str) -> List[str]:
        """
        Break down a complex request into steps.
        
        Args:
            request: User request
            
        Returns:
            List of steps to execute
        """
        request_lower = request.lower()
        steps = []
        
        # Analyze request to determine steps
        if any(kw in request_lower for kw in ["policy", "find", "what", "get"]):
            steps.append("Research policy or information")
        
        if any(kw in request_lower for kw in ["calculate", "remaining", "how many"]):
            steps.append("Perform calculation")
        
        if any(kw in request_lower for kw in ["summarize", "prepare", "summary", "report"]):
            steps.append("Prepare summary or report")
        
        # If no steps detected, default to research
        if not steps:
            steps.append("Research and analyze")
        
        return steps if steps else ["Process request"]
    
    def _execute_step(self, step: str, state: AgentState):
        """Execute a single step."""
        step_lower = step.lower()
        
        if "research" in step_lower or "policy" in step_lower:
            result = self.research_agent.get_annual_leave_entitlement()
            state.add_research_result(result)
            state.record_step(f"Research: {step}")
            
            # Also get used leave
            used_result = self.research_agent.get_employee_leave_used()
            print(f"[Supervisor] Research result: Annual leave = {result['annual_leave_days']} days")
        
        elif "calculate" in step_lower or "calculation" in step_lower:
            # Use data from previous research
            if state.research_result:
                annual_leave = state.research_result.get('annual_leave_days', 18)
                used_leave = 7  # Example
                
                result = self.calculator_agent.calculate_remaining_leave(
                    annual_leave, used_leave
                )
                state.add_calculation_result(result)
                state.record_step(f"Calculation: {step}")
                print(f"[Supervisor] Calculation result: Remaining = {result['remaining_leave']} days")
        
        elif "summary" in step_lower or "prepare" in step_lower:
            # Create summary from previous results
            if state.research_result and state.calculation_result:
                context = {
                    "header": "LEAVE SUMMARY",
                    "annual_leave": state.research_result.get('annual_leave_days', 18),
                    "used_leave": 7,
                    "remaining_leave": state.calculation_result.get('remaining_leave', 11)
                }
                
                result = self.writer_agent.write_summary(context)
                state.add_writing_result(result)
                state.record_step(f"Summary: {step}")
                print(f"[Supervisor] Summary prepared")
    
    def _generate_final_answer(self, state: AgentState) -> str:
        """Generate the final answer from collected results."""
        if state.writing_result:
            return state.writing_result.get('summary', 'No answer generated')
        elif state.calculation_result:
            return f"Result: {state.calculation_result}"
        elif state.research_result:
            return f"Found: {state.research_result}"
        else:
            return "Unable to generate answer"
    
    def _create_execution_summary(self, state: AgentState) -> List[Dict[str, Any]]:
        """Create a summary of execution steps."""
        return state.completed_steps
    
    def handle_complex_workflow(self, request: str) -> Dict[str, Any]:
        """
        Handle complex workflows that require specialized handling.
        
        Args:
            request: User request
            
        Returns:
            Processing result
        """
        print(f"\n[Supervisor] Processing complex workflow request")
        
        # Identify task type
        task_type = self.router.classify_task(request)
        print(f"[Supervisor] Identified task type: {task_type.value}")
        
        # Route to appropriate handler
        if task_type.value == "complex":
            return self.process_request(request)
        else:
            result = self.router.route_task(request)
            return {
                "status": "success",
                "final_answer": result.get('result', result),
                "conversation_id": result.get('conversation_id', '')
            }


def run_supervisor_example():
    """Run an example with the supervisor."""
    supervisor = SupervisorAgent()
    
    result = supervisor.process_request(
        "According to the leave policy, how many annual leave days are available? "
        "I have already used 7 days. Calculate my remaining leave and provide a summary."
    )
    
    print(result['final_answer'])
    
    return result


if __name__ == "__main__":
    run_supervisor_example()
