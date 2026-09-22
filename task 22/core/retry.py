"""
Retry Manager
Handles agent failures with retry logic.
"""

import time
from typing import Callable, Dict, Any, Optional
from enum import Enum


class RetryStatus(Enum):
    """Status of a retry attempt."""
    SUCCESS = "success"
    FAILED = "failed"
    RETRYING = "retrying"
    EXHAUSTED = "exhausted"


class RetryAttempt:
    """Represents a single retry attempt."""
    
    def __init__(self, attempt_number: int, agent: str, action: str):
        self.attempt_number = attempt_number
        self.agent = agent
        self.action = action
        self.status = RetryStatus.FAILED
        self.error = None
        self.result = None
        self.timestamp = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "attempt_number": self.attempt_number,
            "agent": self.agent,
            "action": self.action,
            "status": self.status.value,
            "error": self.error,
            "result": self.result,
            "timestamp": self.timestamp
        }


class RetryManager:
    """
    Manages retry logic for failed agent actions.
    
    Example:
    
    Agent Action
          ↓
    ERROR
          ↓
    Retry
          ↓
    Success
    
    Or if all retries fail:
    
    Attempt 1 → Failed
    Attempt 2 → Failed
    Attempt 3 → Failed
    Agent status = failed
    """
    
    def __init__(self, max_retries: int = 3, backoff_factor: float = 1.0):
        """
        Initialize retry manager.
        
        Args:
            max_retries: Maximum number of retry attempts
            backoff_factor: Backoff multiplier between attempts (seconds)
        """
        self.max_retries = max_retries
        self.backoff_factor = backoff_factor
        self.retry_history = []
    
    def execute_with_retry(self, func: Callable, agent: str, action: str,
                          *args, **kwargs) -> Dict[str, Any]:
        """
        Execute a function with retry logic.
        
        Args:
            func: Function to execute
            agent: Agent name
            action: Action description
            *args: Function arguments
            **kwargs: Function keyword arguments
            
        Returns:
            Result dict with status and data
        """
        print(f"\n[RetryManager] Executing action with retry: {action}")
        print(f"  Agent: {agent}")
        print(f"  Max retries: {self.max_retries}")
        
        for attempt_num in range(1, self.max_retries + 1):
            attempt = RetryAttempt(attempt_num, agent, action)
            
            try:
                print(f"\n  Attempt {attempt_num}/{self.max_retries}...", end=" ")
                
                result = func(*args, **kwargs)
                
                attempt.status = RetryStatus.SUCCESS
                attempt.result = result
                self.retry_history.append(attempt)
                
                print("✓ SUCCESS")
                
                return {
                    "status": "success",
                    "result": result,
                    "attempts": attempt_num,
                    "message": f"Succeeded on attempt {attempt_num}"
                }
            
            except Exception as e:
                attempt.status = RetryStatus.RETRYING if attempt_num < self.max_retries else RetryStatus.EXHAUSTED
                attempt.error = str(e)
                self.retry_history.append(attempt)
                
                print(f"✗ FAILED: {str(e)}")
                
                if attempt_num < self.max_retries:
                    wait_time = self.backoff_factor * attempt_num
                    print(f"  Waiting {wait_time}s before retry...")
                    time.sleep(wait_time)
        
        # All retries exhausted
        print(f"\n  ✗ All {self.max_retries} attempts failed")
        
        return {
            "status": "failed",
            "result": None,
            "attempts": self.max_retries,
            "message": f"Failed after {self.max_retries} attempts",
            "last_error": self.retry_history[-1].error if self.retry_history else None
        }
    
    def simulate_agent_failure(self) -> Dict[str, Any]:
        """Simulate an agent failure with retries."""
        def failing_function():
            """Simulates a function that fails initially then succeeds."""
            attempt_count = len([a for a in self.retry_history if a.agent == "SimulatedAgent"])
            
            if attempt_count < 2:
                raise Exception(f"Simulated failure on attempt {attempt_count + 1}")
            
            return {"data": "Success on attempt 3"}
        
        return self.execute_with_retry(
            failing_function,
            "SimulatedAgent",
            "Simulate failure then success"
        )
    
    def get_retry_statistics(self) -> Dict[str, Any]:
        """Get retry statistics."""
        total_attempts = len(self.retry_history)
        successful = len([a for a in self.retry_history if a.status == RetryStatus.SUCCESS])
        failed = len([a for a in self.retry_history if a.status == RetryStatus.EXHAUSTED])
        
        success_rate = (successful / total_attempts * 100) if total_attempts > 0 else 0
        
        return {
            "total_attempts": total_attempts,
            "successful": successful,
            "failed": failed,
            "success_rate": f"{success_rate:.1f}%"
        }
    
    def print_retry_summary(self):
        """Print retry execution summary."""
        print(f"\n{'='*60}")
        print(f"RETRY MANAGER SUMMARY")
        print(f"{'='*60}\n")
        
        stats = self.get_retry_statistics()
        print(f"Total Attempts: {stats['total_attempts']}")
        print(f"Successful: {stats['successful']}")
        print(f"Failed: {stats['failed']}")
        print(f"Success Rate: {stats['success_rate']}\n")
        
        for attempt in self.retry_history:
            print(f"Attempt {attempt.attempt_number}: {attempt.agent}")
            print(f"  Action: {attempt.action}")
            print(f"  Status: {attempt.status.value}")
            if attempt.error:
                print(f"  Error: {attempt.error}")
            print()


if __name__ == "__main__":
    manager = RetryManager(max_retries=3, backoff_factor=0.1)
    
    # Test with simulated failure
    print("\n--- Testing Retry Logic ---")
    result = manager.simulate_agent_failure()
    
    print(f"\nFinal Result:")
    print(f"  Status: {result['status']}")
    print(f"  Attempts: {result['attempts']}")
    print(f"  Message: {result['message']}")
    
    manager.print_retry_summary()
