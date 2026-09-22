"""
Loop Protection
Prevents infinite agent loops by limiting execution steps.
"""

from typing import Dict, Any, List
from enum import Enum


class LoopProtectionStatus(Enum):
    """Status of loop protection."""
    ACTIVE = "active"
    WARNING = "warning"
    LIMIT_REACHED = "limit_reached"
    STOPPED = "stopped"


class LoopProtection:
    """
    Prevents infinite loops in multi-agent systems.
    
    Dangerous situation:
    
    Supervisor
         ↓
    Research
         ↓
    Supervisor
         ↓
    Research
         ↓
    Supervisor
         ↓
    Research
         ↓
    ...
    
    This class prevents that by setting a maximum step limit.
    """
    
    def __init__(self, max_steps: int = 10):
        """
        Initialize loop protection.
        
        Args:
            max_steps: Maximum number of execution steps allowed
        """
        self.max_steps = max_steps
        self.current_step = 0
        self.steps = []
        self.status = LoopProtectionStatus.ACTIVE
    
    def record_step(self, agent: str, action: str) -> Dict[str, Any]:
        """
        Record an execution step.
        
        Args:
            agent: Agent name
            action: Action performed
            
        Returns:
            Dict with step info and status
        """
        self.current_step += 1
        
        step_info = {
            "step_number": self.current_step,
            "agent": agent,
            "action": action
        }
        
        self.steps.append(step_info)
        
        print(f"\n[LoopProtection] Step {self.current_step}/{self.max_steps}")
        print(f"  Agent: {agent}")
        print(f"  Action: {action}")
        
        # Check if we're approaching the limit
        if self.current_step == int(self.max_steps * 0.8):
            self.status = LoopProtectionStatus.WARNING
            print(f"  ⚠ WARNING: Approaching step limit ({self.current_step}/{self.max_steps})")
        
        # Check if we've reached the limit
        if self.current_step >= self.max_steps:
            self.status = LoopProtectionStatus.LIMIT_REACHED
            print(f"  ✗ LIMIT REACHED: Maximum steps ({self.max_steps}) exceeded!")
        
        return step_info
    
    def can_continue(self) -> bool:
        """
        Check if execution can continue.
        
        Returns:
            True if under limit, False if limit reached
        """
        return self.current_step < self.max_steps
    
    def should_warn(self) -> bool:
        """
        Check if warning threshold reached.
        
        Returns:
            True if warning threshold reached
        """
        warning_threshold = int(self.max_steps * 0.8)
        return self.current_step >= warning_threshold
    
    def detect_loop(self) -> Dict[str, Any]:
        """
        Detect potential infinite loops by analyzing step patterns.
        
        Returns:
            Dict with loop detection results
        """
        if len(self.steps) < 3:
            return {"loop_detected": False}
        
        # Check for repeating pattern
        recent_steps = self.steps[-5:] if len(self.steps) >= 5 else self.steps
        
        agents = [s["agent"] for s in recent_steps]
        
        # Check if same agent appears multiple times in succession
        loop_patterns = []
        
        for i in range(len(agents) - 1):
            if agents[i] == agents[i + 1]:
                loop_patterns.append(agents[i])
        
        if loop_patterns:
            return {
                "loop_detected": True,
                "repeating_agent": loop_patterns[0],
                "occurrences": len(loop_patterns),
                "message": f"Agent '{loop_patterns[0]}' executed {len(loop_patterns)} times in succession"
            }
        
        return {"loop_detected": False}
    
    def stop_execution(self) -> Dict[str, Any]:
        """
        Stop execution and return status.
        
        Returns:
            Stop status and summary
        """
        self.status = LoopProtectionStatus.STOPPED
        
        return {
            "status": "stopped",
            "reason": "Maximum execution steps reached",
            "total_steps": self.current_step,
            "max_steps": self.max_steps,
            "message": f"Agent stopped because the maximum number of execution steps ({self.max_steps}) was reached."
        }
    
    def reset(self):
        """Reset the loop protection counter."""
        self.current_step = 0
        self.steps = []
        self.status = LoopProtectionStatus.ACTIVE
    
    def get_summary(self) -> Dict[str, Any]:
        """Get execution summary."""
        return {
            "current_step": self.current_step,
            "max_steps": self.max_steps,
            "status": self.status.value,
            "total_steps_recorded": len(self.steps),
            "progress_percentage": (self.current_step / self.max_steps * 100),
            "steps": self.steps
        }
    
    def print_summary(self):
        """Print execution summary."""
        summary = self.get_summary()
        
        print(f"\n{'='*60}")
        print(f"LOOP PROTECTION SUMMARY")
        print(f"{'='*60}\n")
        
        print(f"Status: {summary['status']}")
        print(f"Current Step: {summary['current_step']}/{summary['max_steps']}")
        print(f"Progress: {summary['progress_percentage']:.1f}%\n")
        
        print(f"Step History:")
        for step in summary['steps']:
            print(f"  {step['step_number']:2d}. {step['agent']:20s} - {step['action']}")
        
        # Check for loops
        loop_info = self.detect_loop()
        if loop_info['loop_detected']:
            print(f"\n⚠ LOOP DETECTED: {loop_info['message']}")


def test_loop_protection():
    """Test loop protection with simulated execution."""
    print(f"\n{'='*60}")
    print(f"LOOP PROTECTION TEST")
    print(f"{'='*60}")
    
    loop_protection = LoopProtection(max_steps=10)
    
    # Simulate a loop
    agents = ["Supervisor", "Research", "Research", "Research", "Supervisor", "Research", 
              "Research", "Supervisor", "Supervisor"]
    
    for i, agent in enumerate(agents):
        if not loop_protection.can_continue():
            print("\n[Main] Execution stopped due to loop protection")
            break
        
        loop_protection.record_step(agent, f"Execute action {i+1}")
    
    # Check for loops
    loop_info = loop_protection.detect_loop()
    if loop_info['loop_detected']:
        print(f"\n[Main] Loop detected: {loop_info['message']}")
    
    if loop_protection.current_step >= loop_protection.max_steps:
        stop_result = loop_protection.stop_execution()
        print(f"\n[Main] {stop_result['message']}")
    
    loop_protection.print_summary()


if __name__ == "__main__":
    test_loop_protection()
