"""
Agent-to-Agent Communication
Structured communication between agents using standard data formats.
"""

import json
from typing import Dict, Any, Optional
from dataclasses import dataclass, asdict
from enum import Enum


class MessageType(Enum):
    """Types of messages between agents."""
    QUERY = "query"
    RESULT = "result"
    ERROR = "error"
    REQUEST = "request"
    RESPONSE = "response"


@dataclass
class AgentMessage:
    """
    Structured message passed between agents.
    
    Ensures consistent communication format and prevents miscommunication.
    """
    message_id: str
    sender: str
    recipient: str
    message_type: MessageType
    data: Dict[str, Any]
    metadata: Optional[Dict[str, Any]] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert message to dictionary."""
        return {
            "message_id": self.message_id,
            "sender": self.sender,
            "recipient": self.recipient,
            "message_type": self.message_type.value,
            "data": self.data,
            "metadata": self.metadata
        }
    
    def to_json(self) -> str:
        """Convert message to JSON string."""
        return json.dumps(self.to_dict(), indent=2)


class ResearchResult:
    """Structured result from Research Agent."""
    
    def __init__(self):
        self.annual_leave: int = 0
        self.used_leave: int = 0
        self.source: str = ""
        self.details: Dict[str, Any] = {}
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "annual_leave": self.annual_leave,
            "used_leave": self.used_leave,
            "source": self.source,
            "details": self.details
        }


class CalculationResult:
    """Structured result from Calculator Agent."""
    
    def __init__(self):
        self.expression: str = ""
        self.result: float = 0
        self.annual_leave: int = 0
        self.used_leave: int = 0
        self.remaining_leave: int = 0
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "expression": self.expression,
            "result": self.result,
            "annual_leave": self.annual_leave,
            "used_leave": self.used_leave,
            "remaining_leave": self.remaining_leave
        }


class WritingResult:
    """Structured result from Writer Agent."""
    
    def __init__(self):
        self.summary: str = ""
        self.formatted: bool = False
        self.context_used: Dict[str, Any] = {}
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "summary": self.summary,
            "formatted": self.formatted,
            "context_used": self.context_used
        }


class AgentCommunicationBus:
    """
    Central communication hub for agents.
    
    Ensures structured, traceable communication between agents.
    """
    
    def __init__(self):
        self.messages = []
        self.message_counter = 0
    
    def send_message(self, sender: str, recipient: str, 
                    message_type: MessageType, data: Dict[str, Any],
                    metadata: Optional[Dict[str, Any]] = None) -> str:
        """
        Send a message from one agent to another.
        
        Args:
            sender: Name of sending agent
            recipient: Name of receiving agent
            message_type: Type of message
            data: Message data/payload
            metadata: Optional metadata
            
        Returns:
            Message ID
        """
        self.message_counter += 1
        message_id = f"MSG-{self.message_counter:06d}"
        
        message = AgentMessage(
            message_id=message_id,
            sender=sender,
            recipient=recipient,
            message_type=message_type,
            data=data,
            metadata=metadata or {}
        )
        
        self.messages.append(message)
        
        print(f"\n[Bus] Message {message_id}")
        print(f"      From: {sender}")
        print(f"      To: {recipient}")
        print(f"      Type: {message_type.value}")
        print(f"      Data: {json.dumps(data, indent=6)}")
        
        return message_id
    
    def get_messages_for(self, recipient: str) -> list:
        """Get all messages for a specific recipient."""
        return [msg for msg in self.messages if msg.recipient == recipient]
    
    def get_message_history(self) -> list:
        """Get all message history."""
        return [msg.to_dict() for msg in self.messages]
    
    def print_communication_trace(self):
        """Print the entire communication trace."""
        print(f"\n{'='*60}")
        print(f"AGENT COMMUNICATION TRACE")
        print(f"{'='*60}\n")
        
        for msg in self.messages:
            print(f"[{msg.message_id}] {msg.sender} → {msg.recipient}")
            print(f"  Type: {msg.message_type.value}")
            print(f"  Data: {msg.data}")
            print()


class StructuredWorkflow:
    """
    Workflow using structured agent communication.
    
    Example communication flow:
    1. Supervisor sends research request to Research Agent
    2. Research Agent returns research result
    3. Supervisor sends calculation request with research result
    4. Calculator Agent returns calculation result
    5. Supervisor sends write request with all results
    6. Writer Agent returns summary
    """
    
    def __init__(self):
        self.bus = AgentCommunicationBus()
    
    def execute_research_step(self):
        """Execute research step with structured communication."""
        print("\n[Workflow] → Step 1: Research")
        
        # Supervisor requests research
        self.bus.send_message(
            sender="Supervisor",
            recipient="ResearchAgent",
            message_type=MessageType.REQUEST,
            data={
                "query": "What is the annual leave entitlement?",
                "task_id": "TASK-001"
            }
        )
        
        # Research Agent responds
        research_result = ResearchResult()
        research_result.annual_leave = 18
        research_result.used_leave = 7
        research_result.source = "leave_policy.pdf"
        
        self.bus.send_message(
            sender="ResearchAgent",
            recipient="Supervisor",
            message_type=MessageType.RESULT,
            data=research_result.to_dict()
        )
        
        return research_result
    
    def execute_calculation_step(self, research_result: ResearchResult):
        """Execute calculation step with structured communication."""
        print("\n[Workflow] → Step 2: Calculation")
        
        # Supervisor sends calculation request with research result
        self.bus.send_message(
            sender="Supervisor",
            recipient="CalculatorAgent",
            message_type=MessageType.REQUEST,
            data={
                "expression": f"{research_result.annual_leave} - {research_result.used_leave}",
                "annual_leave": research_result.annual_leave,
                "used_leave": research_result.used_leave,
                "task_id": "TASK-001"
            }
        )
        
        # Calculator Agent responds
        calc_result = CalculationResult()
        calc_result.annual_leave = research_result.annual_leave
        calc_result.used_leave = research_result.used_leave
        calc_result.remaining_leave = calc_result.annual_leave - calc_result.used_leave
        calc_result.expression = f"{calc_result.annual_leave} - {calc_result.used_leave}"
        calc_result.result = calc_result.remaining_leave
        
        self.bus.send_message(
            sender="CalculatorAgent",
            recipient="Supervisor",
            message_type=MessageType.RESULT,
            data=calc_result.to_dict()
        )
        
        return calc_result
    
    def execute_writing_step(self, research_result: ResearchResult,
                            calc_result: CalculationResult):
        """Execute writing step with structured communication."""
        print("\n[Workflow] → Step 3: Writing")
        
        # Supervisor sends write request with all results
        self.bus.send_message(
            sender="Supervisor",
            recipient="WriterAgent",
            message_type=MessageType.REQUEST,
            data={
                "annual_leave": research_result.annual_leave,
                "used_leave": research_result.used_leave,
                "remaining_leave": calc_result.remaining_leave,
                "source": research_result.source,
                "task_id": "TASK-001"
            }
        )
        
        # Writer Agent responds
        writing_result = WritingResult()
        writing_result.summary = f"""
LEAVE BALANCE REPORT
{'='*40}
Annual Leave: {research_result.annual_leave} days
Used Leave: {research_result.used_leave} days
Remaining Leave: {calc_result.remaining_leave} days
Source: {research_result.source}
"""
        writing_result.formatted = True
        writing_result.context_used = {
            "annual_leave": research_result.annual_leave,
            "used_leave": research_result.used_leave,
            "remaining_leave": calc_result.remaining_leave
        }
        
        self.bus.send_message(
            sender="WriterAgent",
            recipient="Supervisor",
            message_type=MessageType.RESULT,
            data=writing_result.to_dict()
        )
        
        return writing_result
    
    def run(self):
        """Execute the structured workflow."""
        print(f"\n{'='*60}")
        print(f"STRUCTURED AGENT COMMUNICATION WORKFLOW")
        print(f"{'='*60}")
        
        research_result = self.execute_research_step()
        calc_result = self.execute_calculation_step(research_result)
        writing_result = self.execute_writing_step(research_result, calc_result)
        
        print(writing_result.summary)
        
        self.bus.print_communication_trace()
        
        return {
            "research": research_result.to_dict(),
            "calculation": calc_result.to_dict(),
            "writing": writing_result.to_dict(),
            "communication_trace": self.bus.get_message_history()
        }


if __name__ == "__main__":
    workflow = StructuredWorkflow()
    result = workflow.run()
