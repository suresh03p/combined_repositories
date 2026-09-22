"""
Research Agent
Responsible for document search, RAG, and information retrieval.
"""

import json
from typing import Dict, Any, List
from abc import ABC, abstractmethod


class ResearchAgent:
    """
    Research Agent handles information retrieval, document search, and RAG operations.
    
    Responsibilities:
    - Document searching
    - RAG (Retrieval-Augmented Generation)
    - Information retrieval
    - Source tracking
    """
    
    def __init__(self, name: str = "ResearchAgent"):
        self.name = name
        self.documents = self._load_documents()
    
    def _load_documents(self) -> Dict[str, str]:
        """Load sample documents for demonstration."""
        return {
            "leave_policy.pdf": """
            COMPANY LEAVE POLICY
            
            Annual Leave Entitlement:
            - All full-time employees: 18 working days per annum
            - Part-time employees: Pro-rata based on hours
            
            Leave Year: January 1 - December 31
            
            Types of Leave:
            - Annual/Vacation Leave: 18 days
            - Sick Leave: 10 days (with medical certificate for >2 consecutive days)
            - Compassionate Leave: 3 days
            - Parental Leave: As per company policy
            
            Conditions:
            - Leave must be requested 2 weeks in advance
            - Unused leave can carry over max 5 days to next year
            - Leave requests subject to business requirements
            """,
            "employee_records.txt": """
            EMPLOYEE DATABASE
            
            Employee ID: EMP-001
            Name: John Smith
            Department: Engineering
            Leave Used in 2026: 7 days
            Leave Balance: To be calculated
            
            Employee ID: EMP-002
            Name: Jane Doe
            Department: Marketing
            Leave Used in 2026: 3 days
            Leave Balance: To be calculated
            """,
            "company_handbook.pdf": """
            COMPANY HANDBOOK
            
            Leave Policy Summary:
            Maximum annual leave: 18 days
            Sick leave: 10 days
            Can be combined for extended leave with manager approval
            """
        }
    
    def research(self, question: str) -> Dict[str, Any]:
        """
        Research a question by searching documents.
        
        Args:
            question: The research question
            
        Returns:
            Dict containing results, sources, and metadata
        """
        print(f"\n[Research Agent] Researching: {question}")
        
        results = []
        sources = []
        
        # Simple keyword matching for demonstration
        question_lower = question.lower()
        
        for doc_name, content in self.documents.items():
            if any(keyword in question_lower for keyword in ["leave", "policy", "annual", "days"]):
                if "leave" in content.lower():
                    results.append({
                        "source": doc_name,
                        "relevant_content": self._extract_relevant_content(content, question),
                        "confidence": 0.95
                    })
                    sources.append(doc_name)
        
        result = {
            "status": "success",
            "question": question,
            "results": results,
            "sources": sources,
            "found_documents": len(results) > 0
        }
        
        print(f"[Research Agent] Found {len(results)} relevant documents")
        return result
    
    def _extract_relevant_content(self, content: str, question: str) -> str:
        """Extract relevant lines from content."""
        lines = content.split('\n')
        relevant_lines = []
        
        question_words = set(question.lower().split())
        for line in lines:
            if any(word in line.lower() for word in question_words if len(word) > 3):
                relevant_lines.append(line.strip())
        
        return ' '.join(relevant_lines[:3]) if relevant_lines else content[:200]
    
    def get_annual_leave_entitlement(self) -> Dict[str, Any]:
        """Get the annual leave entitlement from policy."""
        result = self.research("What is the annual leave entitlement?")
        
        # Extract specific data
        annual_leave = 18  # From policy
        
        return {
            "status": "success",
            "annual_leave_days": annual_leave,
            "source": "leave_policy.pdf",
            "details": result
        }
    
    def get_employee_leave_used(self, employee_id: str = "EMP-001") -> Dict[str, Any]:
        """Get employee's leave used so far."""
        result = self.research(f"Leave used by {employee_id}")
        
        # In a real system, this would query a database
        leave_used = 7  # Example data
        
        return {
            "status": "success",
            "employee_id": employee_id,
            "leave_used": leave_used,
            "source": "employee_records.txt",
            "details": result
        }


if __name__ == "__main__":
    agent = ResearchAgent()
    
    # Test research
    result = agent.research("What is the leave policy?")
    print(json.dumps(result, indent=2))
    
    # Test specific functions
    entitlement = agent.get_annual_leave_entitlement()
    print(f"\nAnnual Leave Entitlement: {entitlement['annual_leave_days']} days")
    
    used = agent.get_employee_leave_used()
    print(f"Leave Used: {used['leave_used']} days")
