"""
Agent Execution Logger
Traces and logs all agent execution steps.
"""

import json
from typing import Dict, Any, List, Optional
from datetime import datetime
from enum import Enum


class ExecutionStatus(Enum):
    """Execution status for each step."""
    STARTED = "started"
    PROCESSING = "processing"
    SUCCESS = "success"
    ERROR = "error"
    SKIPPED = "skipped"


class ExecutionStep:
    """Represents a single execution step."""
    
    def __init__(self, step_id: int, agent: str, action: str):
        self.step_id = step_id
        self.agent = agent
        self.action = action
        self.status = ExecutionStatus.STARTED
        self.result = None
        self.error = None
        self.started_at = datetime.now()
        self.completed_at = None
        self.duration_ms = 0
    
    def complete(self, result: Any = None, error: Optional[str] = None):
        """Mark step as complete."""
        self.completed_at = datetime.now()
        self.duration_ms = (self.completed_at - self.started_at).total_seconds() * 1000
        
        if error:
            self.status = ExecutionStatus.ERROR
            self.error = error
        else:
            self.status = ExecutionStatus.SUCCESS
            self.result = result
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "step": self.step_id,
            "agent": self.agent,
            "action": self.action,
            "status": self.status.value,
            "result": self.result,
            "error": self.error,
            "started_at": self.started_at.isoformat(),
            "completed_at": self.completed_at.isoformat() if self.completed_at else None,
            "duration_ms": self.duration_ms
        }


class AgentLogger:
    """
    Logs all agent execution steps for tracing and debugging.
    
    Every action should be recorded:
    
    Step 1
    Supervisor
    Action: Research
    
    Step 2
    Research Agent
    Tool: Vector Search
    
    Step 3
    Research Agent
    Result: 18 annual leave days
    
    ... and so on
    """
    
    def __init__(self, conversation_id: str = None):
        """Initialize logger."""
        import uuid
        self.conversation_id = conversation_id or f"CONV-{uuid.uuid4().hex[:8].upper()}"
        self.steps: List[ExecutionStep] = []
        self.step_counter = 0
        self.started_at = datetime.now()
    
    def log_step(self, agent: str, action: str) -> ExecutionStep:
        """
        Log a new execution step.
        
        Args:
            agent: Agent name
            action: Action description
            
        Returns:
            ExecutionStep object
        """
        self.step_counter += 1
        step = ExecutionStep(self.step_counter, agent, action)
        self.steps.append(step)
        
        print(f"\n[Logger] Step {self.step_counter}")
        print(f"         Agent: {agent}")
        print(f"         Action: {action}")
        
        return step
    
    def mark_success(self, step: ExecutionStep, result: Any = None):
        """Mark a step as successful."""
        step.complete(result)
        print(f"         Status: SUCCESS")
        if result:
            print(f"         Result: {result}")
    
    def mark_error(self, step: ExecutionStep, error: str):
        """Mark a step as failed."""
        step.complete(error=error)
        print(f"         Status: ERROR")
        print(f"         Error: {error}")
    
    def get_steps_for_agent(self, agent: str) -> List[ExecutionStep]:
        """Get all steps executed by a specific agent."""
        return [step for step in self.steps if step.agent == agent]
    
    def get_execution_trace(self) -> List[Dict[str, Any]]:
        """Get the full execution trace."""
        return [step.to_dict() for step in self.steps]
    
    def get_execution_trace_json(self) -> str:
        """Get execution trace as JSON."""
        trace = {
            "conversation_id": self.conversation_id,
            "started_at": self.started_at.isoformat(),
            "completed_at": datetime.now().isoformat(),
            "total_steps": len(self.steps),
            "steps": self.get_execution_trace()
        }
        
        return json.dumps(trace, indent=2, default=str)
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get execution statistics."""
        total_steps = len(self.steps)
        successful = len([s for s in self.steps if s.status == ExecutionStatus.SUCCESS])
        errors = len([s for s in self.steps if s.status == ExecutionStatus.ERROR])
        
        total_duration = sum(s.duration_ms for s in self.steps)
        
        agents_used = set(s.agent for s in self.steps)
        
        return {
            "total_steps": total_steps,
            "successful_steps": successful,
            "failed_steps": errors,
            "success_rate": f"{(successful/total_steps*100):.1f}%" if total_steps > 0 else "N/A",
            "total_duration_ms": total_duration,
            "average_step_duration_ms": total_duration / total_steps if total_steps > 0 else 0,
            "unique_agents": len(agents_used),
            "agents_used": sorted(list(agents_used))
        }
    
    def print_execution_trace(self):
        """Print the execution trace."""
        print(f"\n{'='*70}")
        print(f"AGENT EXECUTION TRACE - {self.conversation_id}")
        print(f"{'='*70}\n")
        
        for step in self.steps:
            print(f"Step {step.step_id}: {step.agent}")
            print(f"  Action: {step.action}")
            print(f"  Status: {step.status.value}")
            if step.result:
                print(f"  Result: {step.result}")
            if step.error:
                print(f"  Error: {step.error}")
            print(f"  Duration: {step.duration_ms:.2f}ms")
            print()
    
    def print_statistics(self):
        """Print execution statistics."""
        stats = self.get_statistics()
        
        print(f"\n{'='*70}")
        print(f"EXECUTION STATISTICS")
        print(f"{'='*70}\n")
        
        print(f"Total Steps: {stats['total_steps']}")
        print(f"Successful: {stats['successful_steps']}")
        print(f"Failed: {stats['failed_steps']}")
        print(f"Success Rate: {stats['success_rate']}")
        print(f"Total Duration: {stats['total_duration_ms']:.2f}ms")
        print(f"Average Step Duration: {stats['average_step_duration_ms']:.2f}ms")
        print(f"Unique Agents: {stats['unique_agents']}")
        print(f"Agents Used: {', '.join(stats['agents_used'])}")
    
    def save_trace_to_file(self, filename: str):
        """Save execution trace to file."""
        with open(filename, 'w') as f:
            f.write(self.get_execution_trace_json())
        
        print(f"\n[Logger] Trace saved to: {filename}")


def test_logger():
    """Test the agent logger."""
    logger = AgentLogger()
    
    print(f"\n{'='*70}")
    print(f"AGENT LOGGER TEST")
    print(f"{'='*70}")
    
    # Simulate execution steps
    step1 = logger.log_step("Supervisor", "Analyze request")
    logger.mark_success(step1, "Request decomposed into 3 steps")
    
    step2 = logger.log_step("ResearchAgent", "Search for leave policy")
    logger.mark_success(step2, {"annual_leave": 18, "source": "policy.pdf"})
    
    step3 = logger.log_step("CalculatorAgent", "Calculate remaining leave")
    logger.mark_success(step3, {"remaining": 11})
    
    step4 = logger.log_step("WriterAgent", "Generate summary")
    logger.mark_success(step4, "Summary generated")
    
    # Try a failed step
    step5 = logger.log_step("ValidationAgent", "Validate result")
    logger.mark_error(step5, "Validation failed: Missing data")
    
    # Print results
    logger.print_execution_trace()
    logger.print_statistics()


if __name__ == "__main__":
    test_logger()
