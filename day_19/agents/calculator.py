"""
Calculator Agent
Responsible for arithmetic, calculations, and numeric analysis.
"""

import json
import re
from typing import Dict, Any, Union


class CalculatorAgent:
    """
    Calculator Agent handles arithmetic operations and numeric analysis.
    
    Responsibilities:
    - Arithmetic calculations
    - Numeric analysis
    - Expression evaluation
    - Mathematical operations
    """
    
    def __init__(self, name: str = "CalculatorAgent"):
        self.name = name
        self.last_result = None
    
    def calculate(self, expression: str) -> Dict[str, Any]:
        """
        Evaluate a mathematical expression safely.
        
        Args:
            expression: Mathematical expression (e.g., "18 - 7")
            
        Returns:
            Dict containing result, expression, and status
        """
        print(f"\n[Calculator Agent] Calculating: {expression}")
        
        try:
            # Simple validation and evaluation
            # In production, use a proper expression parser
            result = self._safe_eval(expression)
            
            self.last_result = result
            
            return {
                "status": "success",
                "expression": expression,
                "result": result,
                "type": type(result).__name__
            }
        except Exception as e:
            return {
                "status": "error",
                "expression": expression,
                "error": str(e)
            }
    
    def _safe_eval(self, expression: str) -> Union[int, float]:
        """
        Safely evaluate an expression using eval with restrictions.
        
        Args:
            expression: Mathematical expression
            
        Returns:
            Result of the calculation
        """
        # Remove dangerous characters
        safe_expr = expression.strip()
        
        # Only allow numbers, operators, and parentheses
        if not re.match(r'^[0-9+\-*/(). ]*$', safe_expr):
            raise ValueError("Invalid characters in expression")
        
        # Evaluate safely (in production, use ast.literal_eval or sympy)
        result = eval(safe_expr)
        return result
    
    def calculate_remaining_leave(self, annual_leave: int, used_leave: int) -> Dict[str, Any]:
        """
        Calculate remaining leave days.
        
        Args:
            annual_leave: Total annual leave days
            used_leave: Leave days already used
            
        Returns:
            Dict with calculation result
        """
        print(f"\n[Calculator Agent] Calculating remaining leave: {annual_leave} - {used_leave}")
        
        remaining = annual_leave - used_leave
        
        result = {
            "status": "success",
            "annual_leave": annual_leave,
            "used_leave": used_leave,
            "remaining_leave": remaining,
            "calculation": f"{annual_leave} - {used_leave} = {remaining}"
        }
        
        self.last_result = remaining
        print(f"[Calculator Agent] Result: {remaining} days remaining")
        
        return result
    
    def calculate_percentage(self, used: int, total: int) -> Dict[str, Any]:
        """Calculate percentage of leave used."""
        if total == 0:
            return {
                "status": "error",
                "error": "Total cannot be zero"
            }
        
        percentage = (used / total) * 100
        
        return {
            "status": "success",
            "used": used,
            "total": total,
            "percentage_used": round(percentage, 2),
            "percentage_remaining": round(100 - percentage, 2)
        }
    
    def add(self, a: Union[int, float], b: Union[int, float]) -> Union[int, float]:
        """Add two numbers."""
        return a + b
    
    def subtract(self, a: Union[int, float], b: Union[int, float]) -> Union[int, float]:
        """Subtract two numbers."""
        return a - b
    
    def multiply(self, a: Union[int, float], b: Union[int, float]) -> Union[int, float]:
        """Multiply two numbers."""
        return a * b
    
    def divide(self, a: Union[int, float], b: Union[int, float]) -> Union[int, float]:
        """Divide two numbers."""
        if b == 0:
            raise ValueError("Cannot divide by zero")
        return a / b


if __name__ == "__main__":
    agent = CalculatorAgent()
    
    # Test basic calculation
    result = agent.calculate("18 - 7")
    print(json.dumps(result, indent=2))
    
    # Test remaining leave calculation
    leave_calc = agent.calculate_remaining_leave(18, 7)
    print(json.dumps(leave_calc, indent=2))
    
    # Test percentage
    percent = agent.calculate_percentage(7, 18)
    print(json.dumps(percent, indent=2))
