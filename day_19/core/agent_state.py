"""
Agent State Management
Manages shared state across agents.
"""

import json
from typing import Dict, Any, Optional
from datetime import datetime
from enum import Enum


class TaskStatus(Enum):
    """Status of a task or workflow."""
    STARTED = "started"
    IN_PROGRESS = "in_progress"
    RESEARCH_COMPLETE = "research_complete"
    CALCULATION_COMPLETE = "calculation_complete"
    WRITING_COMPLETE = "writing_complete"
    APPROVAL_PENDING = "approval_pending"
    APPROVED = "approved"
    REJECTED = "rejected"
    COMPLETED = "completed"
    FAILED = "failed"


class AgentState:
    """
    Manages the shared state across all agents in the workflow.
    
    The state is passed between agents, allowing them to share information
    and build upon previous results.
    """
    
    def __init__(self, user_request: str, conversation_id: str = None):
        """
        Initialize agent state.
        
        Args:
            user_request: The original user request
            conversation_id: Optional conversation identifier
        """
        self.conversation_id = conversation_id or self._generate_id()
        self.user_request = user_request
        self.status = TaskStatus.STARTED
        self.created_at = datetime.now()
        self.updated_at = datetime.now()
        
        # Results from each agent
        self.research_result = None
        self.calculation_result = None
        self.writing_result = None
        
        # Workflow tracking
        self.current_step = 0
        self.completed_steps = []
        self.pending_steps = []
        self.total_steps = 0
        
        # Agent results
        self.agent_results = {}
        
        # Error tracking
        self.errors = []
        
        # Approval tracking
        self.approval_required = False
        self.approval_status = None
        self.approval_reason = ""
    
    @staticmethod
    def _generate_id() -> str:
        """Generate a unique conversation ID."""
        import uuid
        return f"CONV-{uuid.uuid4().hex[:8].upper()}"
    
    def update_status(self, status: TaskStatus, message: str = ""):
        """Update the current status."""
        self.status = status
        self.updated_at = datetime.now()
        if message:
            print(f"[State] Status updated to {status.value}: {message}")
    
    def add_research_result(self, result: Dict[str, Any]):
        """Add research agent result to state."""
        print(f"\n[State] Adding research result")
        self.research_result = result
        self.agent_results['research'] = result
        self.update_status(TaskStatus.RESEARCH_COMPLETE)
    
    def add_calculation_result(self, result: Dict[str, Any]):
        """Add calculator agent result to state."""
        print(f"[State] Adding calculation result")
        self.calculation_result = result
        self.agent_results['calculator'] = result
        self.update_status(TaskStatus.CALCULATION_COMPLETE)
    
    def add_writing_result(self, result: Dict[str, Any]):
        """Add writer agent result to state."""
        print(f"[State] Adding writing result")
        self.writing_result = result
        self.agent_results['writer'] = result
        self.update_status(TaskStatus.WRITING_COMPLETE)
    
    def record_step(self, step_name: str, status: str = "success"):
        """Record a completed workflow step."""
        self.completed_steps.append({
            "step": step_name,
            "status": status,
            "timestamp": datetime.now().isoformat()
        })
        self.current_step += 1
    
    def set_pending_steps(self, steps: list):
        """Set the list of pending steps."""
        self.pending_steps = steps
        self.total_steps = len(steps)
    
    def add_error(self, error: str, agent: str = ""):
        """Record an error that occurred."""
        error_entry = {
            "timestamp": datetime.now().isoformat(),
            "agent": agent,
            "error": error
        }
        self.errors.append(error_entry)
        print(f"[State] Error recorded: {error}")
    
    def request_approval(self, action: str, reason: str = ""):
        """Request human approval for an action."""
        self.approval_required = True
        self.approval_reason = reason or f"Action: {action}"
        self.update_status(TaskStatus.APPROVAL_PENDING)
    
    def set_approval(self, approved: bool):
        """Set approval status."""
        self.approval_status = "approved" if approved else "rejected"
        self.update_status(
            TaskStatus.APPROVED if approved else TaskStatus.REJECTED
        )
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert state to dictionary."""
        return {
            "conversation_id": self.conversation_id,
            "user_request": self.user_request,
            "status": self.status.value,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
            "research_result": self.research_result,
            "calculation_result": self.calculation_result,
            "writing_result": self.writing_result,
            "current_step": self.current_step,
            "completed_steps": self.completed_steps,
            "pending_steps": self.pending_steps,
            "total_steps": self.total_steps,
            "agent_results": self.agent_results,
            "errors": self.errors,
            "approval_required": self.approval_required,
            "approval_status": self.approval_status,
            "approval_reason": self.approval_reason
        }
    
    def to_json(self, pretty: bool = True) -> str:
        """Convert state to JSON string."""
        if pretty:
            return json.dumps(self.to_dict(), indent=2, default=str)
        return json.dumps(self.to_dict(), default=str)
    
    def print_state(self):
        """Print current state."""
        print(f"\n{'='*60}")
        print(f"AGENT STATE: {self.conversation_id}")
        print(f"{'='*60}")
        print(f"User Request: {self.user_request}")
        print(f"Status: {self.status.value}")
        print(f"Current Step: {self.current_step}/{self.total_steps}")
        print(f"Completed Steps: {len(self.completed_steps)}")
        print(f"Errors: {len(self.errors)}")
        print(f"Created: {self.created_at.strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"{'='*60}\n")


class StateManager:
    """Manages multiple agent states."""
    
    def __init__(self):
        """Initialize state manager."""
        self.states: Dict[str, AgentState] = {}
    
    def create_state(self, user_request: str, conversation_id: str = None) -> AgentState:
        """Create a new agent state."""
        state = AgentState(user_request, conversation_id)
        self.states[state.conversation_id] = state
        print(f"[StateManager] Created state: {state.conversation_id}")
        return state
    
    def get_state(self, conversation_id: str) -> Optional[AgentState]:
        """Retrieve an agent state."""
        return self.states.get(conversation_id)
    
    def get_all_states(self) -> Dict[str, AgentState]:
        """Get all states."""
        return self.states.copy()
    
    def delete_state(self, conversation_id: str):
        """Delete a state."""
        if conversation_id in self.states:
            del self.states[conversation_id]
            print(f"[StateManager] Deleted state: {conversation_id}")


if __name__ == "__main__":
    # Example: Creating and managing state
    state = AgentState("Find leave policy and calculate remaining leave")
    
    # Simulate workflow
    state.set_pending_steps([
        "Research",
        "Calculator",
        "Writer"
    ])
    
    # Simulate step 1: Research
    state.record_step("Research Agent")
    state.add_research_result({
        "annual_leave": 18,
        "source": "leave_policy.pdf"
    })
    
    # Simulate step 2: Calculator
    state.record_step("Calculator Agent")
    state.add_calculation_result({
        "remaining_leave": 11,
        "calculation": "18 - 7 = 11"
    })
    
    # Simulate step 3: Writer
    state.record_step("Writer Agent")
    state.add_writing_result({
        "summary": "Employee has 11 days remaining"
    })
    
    state.update_status(TaskStatus.COMPLETED)
    
    # Print final state
    state.print_state()
    print(state.to_json())
