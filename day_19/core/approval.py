"""
Approval Manager
Handles human approval for sensitive actions.
"""

from enum import Enum
from typing import Dict, Any
from datetime import datetime


class ApprovalLevel(Enum):
    """Risk levels for different actions."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class ApprovalStatus(Enum):
    """Status of an approval request."""
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"
    EXPIRED = "expired"


class ApprovalRequest:
    """Represents an approval request."""
    
    def __init__(self, request_id: str, action: str, level: ApprovalLevel, reason: str = ""):
        self.request_id = request_id
        self.action = action
        self.level = level
        self.reason = reason
        self.status = ApprovalStatus.PENDING
        self.created_at = datetime.now()
        self.approved_by = None
        self.approved_at = None
    
    def approve(self, approved_by: str = "system"):
        """Approve the request."""
        self.status = ApprovalStatus.APPROVED
        self.approved_by = approved_by
        self.approved_at = datetime.now()
    
    def reject(self, approved_by: str = "system"):
        """Reject the request."""
        self.status = ApprovalStatus.REJECTED
        self.approved_by = approved_by
        self.approved_at = datetime.now()
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "request_id": self.request_id,
            "action": self.action,
            "level": self.level.value,
            "reason": self.reason,
            "status": self.status.value,
            "created_at": self.created_at.isoformat(),
            "approved_by": self.approved_by,
            "approved_at": self.approved_at.isoformat() if self.approved_at else None
        }


class ApprovalManager:
    """
    Manages approval workflows for sensitive actions.
    
    Categories:
    
    LOW RISK
        ↓
    Automatic
    
    MEDIUM RISK
        ↓
    Ask Confirmation
    
    HIGH RISK
        ↓
    Human Approval Required
    """
    
    # Risk classification
    RISK_LEVELS = {
        # LOW RISK - Automatic approval
        "search_document": ApprovalLevel.LOW,
        "search": ApprovalLevel.LOW,
        "calculate_salary": ApprovalLevel.LOW,
        "calculate": ApprovalLevel.LOW,
        "read_policy": ApprovalLevel.LOW,
        "get_information": ApprovalLevel.LOW,
        
        # MEDIUM RISK - Ask confirmation
        "update_record": ApprovalLevel.MEDIUM,
        "update_document": ApprovalLevel.MEDIUM,
        "modify_data": ApprovalLevel.MEDIUM,
        "export_data": ApprovalLevel.MEDIUM,
        
        # HIGH RISK - Human approval required
        "delete_document": ApprovalLevel.HIGH,
        "delete_record": ApprovalLevel.HIGH,
        "send_external_email": ApprovalLevel.HIGH,
        "access_sensitive": ApprovalLevel.HIGH,
        "grant_access": ApprovalLevel.HIGH,
        "terminate_service": ApprovalLevel.HIGH
    }
    
    def __init__(self):
        """Initialize approval manager."""
        self.pending_requests: Dict[str, ApprovalRequest] = {}
        self.approval_history = []
        self.auto_approver = "system"
    
    def get_risk_level(self, action: str) -> ApprovalLevel:
        """Get risk level for an action."""
        action_lower = action.lower()
        
        for action_key, level in self.RISK_LEVELS.items():
            if action_key in action_lower:
                return level
        
        # Default to medium risk
        return ApprovalLevel.MEDIUM
    
    def request_approval(self, action: str, reason: str = "") -> Dict[str, Any]:
        """
        Request approval for an action.
        
        Args:
            action: Action to be approved
            reason: Reason for the action
            
        Returns:
            Approval request info
        """
        request_id = self._generate_request_id()
        level = self.get_risk_level(action)
        
        approval_request = ApprovalRequest(request_id, action, level, reason)
        self.pending_requests[request_id] = approval_request
        
        print(f"\n[ApprovalManager] Approval Requested")
        print(f"  Request ID: {request_id}")
        print(f"  Action: {action}")
        print(f"  Risk Level: {level.value}")
        print(f"  Reason: {reason if reason else 'Not specified'}")
        
        # Handle based on risk level
        if level == ApprovalLevel.LOW:
            return self._handle_low_risk(approval_request)
        elif level == ApprovalLevel.MEDIUM:
            return self._handle_medium_risk(approval_request)
        else:  # HIGH RISK
            return self._handle_high_risk(approval_request)
    
    def _handle_low_risk(self, request: ApprovalRequest) -> Dict[str, Any]:
        """Automatically approve low-risk actions."""
        request.approve(self.auto_approver)
        self.approval_history.append(request)
        
        print(f"  Status: APPROVED (Automatic)")
        print(f"  Reason: Low risk action")
        
        return {
            "approved": True,
            "request_id": request.request_id,
            "message": "Action automatically approved (low risk)"
        }
    
    def _handle_medium_risk(self, request: ApprovalRequest) -> Dict[str, Any]:
        """Request confirmation for medium-risk actions."""
        print(f"  Status: PENDING (Confirmation Required)")
        
        # Simulate confirmation
        confirmation = input(f"\n  Confirm action '{request.action}'? (yes/no): ")
        
        if confirmation.lower() == "yes":
            request.approve("user_confirmed")
            self.approval_history.append(request)
            
            print(f"  Status: APPROVED")
            
            return {
                "approved": True,
                "request_id": request.request_id,
                "message": "Action confirmed and approved"
            }
        else:
            request.reject("user_declined")
            self.approval_history.append(request)
            
            print(f"  Status: REJECTED")
            
            return {
                "approved": False,
                "request_id": request.request_id,
                "message": "Action declined by user"
            }
    
    def _handle_high_risk(self, request: ApprovalRequest) -> Dict[str, Any]:
        """Request human approval for high-risk actions."""
        print(f"  Status: PENDING (Human Approval Required)")
        print(f"  This action requires explicit human approval.")
        
        # Simulate human approval request
        approval = input(f"\n  Admin Approval Required for '{request.action}'? (yes/no): ")
        
        if approval.lower() == "yes":
            request.approve("admin_approved")
            self.approval_history.append(request)
            
            print(f"  Status: APPROVED by Admin")
            
            return {
                "approved": True,
                "request_id": request.request_id,
                "message": "Action approved by administrator"
            }
        else:
            request.reject("admin_denied")
            self.approval_history.append(request)
            
            print(f"  Status: REJECTED")
            
            return {
                "approved": False,
                "request_id": request.request_id,
                "message": "Action not approved by administrator"
            }
    
    def get_request_status(self, request_id: str) -> Dict[str, Any]:
        """Get status of a pending request."""
        if request_id in self.pending_requests:
            return self.pending_requests[request_id].to_dict()
        
        # Check history
        for request in self.approval_history:
            if request.request_id == request_id:
                return request.to_dict()
        
        return {"error": "Request not found"}
    
    def get_pending_count(self) -> int:
        """Get count of pending approvals."""
        return len([r for r in self.pending_requests.values() 
                   if r.status == ApprovalStatus.PENDING])
    
    def _generate_request_id(self) -> str:
        """Generate unique request ID."""
        import uuid
        return f"APR-{uuid.uuid4().hex[:8].upper()}"
    
    def print_approval_summary(self):
        """Print approval summary."""
        print(f"\n{'='*60}")
        print(f"APPROVAL SUMMARY")
        print(f"{'='*60}\n")
        
        total_requests = len(self.approval_history)
        approved = len([r for r in self.approval_history if r.status == ApprovalStatus.APPROVED])
        rejected = len([r for r in self.approval_history if r.status == ApprovalStatus.REJECTED])
        
        print(f"Total Requests: {total_requests}")
        print(f"Approved: {approved}")
        print(f"Rejected: {rejected}")
        print(f"Pending: {self.get_pending_count()}\n")
        
        for request in self.approval_history:
            print(f"[{request.request_id}] {request.action}")
            print(f"  Level: {request.level.value}")
            print(f"  Status: {request.status.value}")
            print()


if __name__ == "__main__":
    manager = ApprovalManager()
    
    # Test low risk
    print("\n--- Testing LOW RISK ---")
    manager.request_approval("search_document", "Looking for policy")
    
    # Test medium risk
    print("\n--- Testing MEDIUM RISK ---")
    manager.request_approval("update_record", "Updating employee data")
    
    # Test high risk
    print("\n--- Testing HIGH RISK ---")
    manager.request_approval("delete_document", "Removing outdated file")
    
    manager.print_approval_summary()
