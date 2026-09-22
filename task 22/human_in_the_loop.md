# Human-in-the-Loop System

## Overview

Human-in-the-Loop (HiL) systems integrate human judgment into AI workflows for sensitive or high-risk operations. Not all agent actions should happen automatically.

## Problem Scenario

**Without Human-in-the-Loop:**
```
User: "Delete all company documents."
       ↓
Agent: Immediately executes deletion
       ↓
Documents GONE
       ↓
Disaster!
```

**With Human-in-the-Loop:**
```
User: "Delete all company documents."
       ↓
Agent: Recognizes sensitive action
       ↓
System: Requests human approval
       ↓
Human Reviews Request
       ↓
Approve or Reject
       ↓
Execute only if approved
```

## Risk Categories

### LOW RISK - Automatic Execution
- Search documents
- Calculate salary
- Read policy
- Get information

These actions are safe and can be executed immediately without approval.

**Implementation:**
```python
if risk_level == "low":
    # Execute immediately
    result = execute_action()
```

---

### MEDIUM RISK - Request Confirmation
- Update record
- Modify data
- Export data
- Change settings

These actions can be executed but should ask for user confirmation first.

**Implementation:**
```python
if risk_level == "medium":
    # Ask user confirmation
    confirmation = input("Confirm action? (yes/no): ")
    if confirmation == "yes":
        result = execute_action()
```

---

### HIGH RISK - Human Approval Required
- Delete document
- Delete record
- Send external email
- Grant access
- Terminate service

These actions should ONLY execute after explicit human (admin) approval.

**Implementation:**
```python
if risk_level == "high":
    # Request admin approval
    approval = request_admin_approval()
    if approval:
        result = execute_action()
    else:
        result = "Action not approved"
```

---

## Risk Classification Table

| Action | Risk Level | Approval Type | Example |
|--------|-----------|---------------|---------|
| Search documents | LOW | None | "Find policy file" |
| Calculate metrics | LOW | None | "Calculate 18-7" |
| Read data | LOW | None | "Get leave balance" |
| Update record | MEDIUM | Confirmation | "Update employee record" |
| Modify settings | MEDIUM | Confirmation | "Change system config" |
| Export data | MEDIUM | Confirmation | "Export reports" |
| Delete document | HIGH | Admin | "Delete all files" |
| Delete record | HIGH | Admin | "Remove employee record" |
| Send external email | HIGH | Admin | "Email external partner" |
| Grant access | HIGH | Admin | "Give admin privileges" |
| Terminate service | HIGH | Admin | "Shut down system" |

---

## Decision Flow

```
                        Action Requested
                              ↓
                    Identify Risk Level
                              ↓
                   ┌──────────┼──────────┐
                   ↓          ↓          ↓
                 LOW      MEDIUM       HIGH
                   ↓          ↓          ↓
              Execute      Ask      Request
            Immediately   User      Admin
                          Confirm   Approval
                   ↓          ↓          ↓
                   └──────────┼──────────┘
                              ↓
                      Approved/Denied
                              ↓
                    Execute or Reject
```

---

## Implementation Workflow

### Step 1: Classify Action Risk

```python
def classify_risk(action):
    if action in ["search", "calculate", "read"]:
        return "low"
    elif action in ["update", "modify", "export"]:
        return "medium"
    elif action in ["delete", "grant", "terminate"]:
        return "high"
```

### Step 2: Route Based on Risk

```python
def handle_action(action):
    risk = classify_risk(action)
    
    if risk == "low":
        return execute(action)
    elif risk == "medium":
        return request_confirmation(action)
    elif risk == "high":
        return request_approval(action)
```

### Step 3: Get Approval

```python
def request_approval(action):
    print(f"⚠ High Risk Action: {action}")
    approval = input("Admin approval? (yes/no): ")
    
    if approval == "yes":
        return execute(action)
    else:
        return "Rejected"
```

### Step 4: Log & Execute

```python
def execute(action):
    log_approval(action)
    return perform_action(action)
```

---

## Best Practices

### 1. Be Clear About Risk
- Clearly communicate why approval is needed
- Show what data is at risk
- Explain consequences

### 2. Streamline Approvals
- Don't ask for approval on everything
- Set reasonable risk thresholds
- Batch similar approvals

### 3. Audit Trail
- Log all approval requests
- Record decisions (approved/rejected)
- Track who approved and when

### 4. Time Limits
- Set expiration on approvals
- Require re-approval periodically
- Alert on long pending requests

### 5. Escalation
- Define approval chain
- Routes to appropriate level
- Clear escalation criteria

---

## Real-World Example: Leave Deletion

```
User Request: "Delete employee leave record for John Smith"
              ↓
Agent Analysis: This is HIGH RISK (deletes critical data)
              ↓
System: Request Admin Approval
        
        Approval Details:
        ├── Action: Delete leave record
        ├── Target: Employee EMP-001 (John Smith)
        ├── Risk: Data loss (permanent deletion)
        └── Confirmation: Admin must explicitly approve
        
        Admin Reviews:
        ├── Check authorization
        ├── Verify necessity
        ├── Review audit log
        └── Decide: APPROVE or REJECT
        
        If APPROVED:
        ├── Log approval
        ├── Execute deletion
        └── Notify requester
        
        If REJECTED:
        ├── Log rejection
        ├── Explain reason
        └── Suggest alternative
```

---

## Approval State Machine

```
PENDING
  ↓
  ├→ APPROVED
  │  ├→ EXECUTED
  │  └→ FAILED_EXECUTION
  │
  └→ REJECTED
     └→ CANCELLED
```

---

## Key Takeaways

1. **Not all actions are equal** - Classify by risk
2. **Automate routine actions** - Don't slow down safe operations
3. **Get approval for critical actions** - Prevent disasters
4. **Maintain audit trail** - Accountability is essential
5. **Communicate clearly** - Users should understand why approval is needed
