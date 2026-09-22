# TASK 12: Hallucination Detection

## What is a Hallucination?

A **hallucination** occurs when an AI system generates information that is:
- **False**: Contradicts known facts
- **Unsupported**: Not found in the source documents
- **Invented**: Created by the AI without basis

### Key Principle
> A RAG system should only answer based on the retrieved documents. If the document doesn't contain the answer, the system should say "I don't know" instead of inventing information.

---

## Types of Hallucinations

### 1. Factual Hallucination
AI makes up facts that are provably false.

**Example:**
```
Context: "Employees receive 18 annual leave days."

Hallucination: "Employees receive 25 annual leave days."

Detection: HALLUCINATION (contradicts source)
```

---

### 2. Semantic Hallucination
AI exaggerates or generalizes beyond what's stated.

**Example:**
```
Context: "Employees can work from home up to 2 days per week."

Hallucination: "Employees can work from home as much as they want."

Detection: HALLUCINATION (overextends the policy)
```

---

### 3. Out-of-Scope Hallucination
AI answers questions that aren't in the documents.

**Example:**
```
Question: "What is the company's international travel policy?"
Context: No documents mention international travel policy.

Hallucination: "The company provides full international travel coverage."

Correct Answer: "I don't have information about international travel policies."
```

---

## Hallucination Detection Strategy

### Step 1: Extract Key Claims
Break down the AI answer into individual factual claims.

```
AI Answer: "Employees receive 20 days of annual leave and can carry over 10 days."

Claims:
1. Employees receive annual leave
2. Amount is 20 days
3. Carry-over is allowed
4. Carry-over amount is 10 days
```

### Step 2: Verify Against Context
Check if each claim is supported by the source documents.

```
Claim 1: "Employees receive annual leave" 
Source: "Employees are entitled to annual leave"
Status: VERIFIED

Claim 2: "Amount is 20 days"
Source: "18 annual leave days"
Status: HALLUCINATION - contradicts source

Claim 3: "Carry-over is allowed"
Source: No mention of carry-over
Status: UNSUPPORTED

Claim 4: "Carry-over amount is 10 days"
Source: No mention
Status: UNSUPPORTED
```

### Step 3: Classify Hallucination Type
```
Factual Contradiction: Claim 2 (20 vs 18 days)
Unsupported Claims: Claims 3, 4
```

---

## Practical Test Cases

### Case 1: Factual Hallucination
```
DOCUMENT:
"Annual leave allowance is 18 days per year"

AI ANSWER:
"The company provides 18 days of annual leave with 5 days carry-over"

HALLUCINATION CHECK:
- "18 days annual leave" - CORRECT
- "5 days carry-over" - NOT IN DOCUMENT
- Status: PARTIAL HALLUCINATION (unsupported claim added)
```

---

### Case 2: Contradictory Hallucination
```
DOCUMENT:
"Work from home is limited to 2 days per week with manager approval"

AI ANSWER:
"Employees can work from home without any restrictions"

HALLUCINATION CHECK:
- "Can work from home" - CORRECT (partial)
- "No restrictions" - CONTRADICTS DOCUMENT
- "Without manager approval" - CONTRADICTS DOCUMENT
- Status: HALLUCINATION (multiple contradictions)
```

---

### Case 3: Unknown Questions
```
QUESTION:
"What is the company's international travel allowance?"

DOCUMENT:
No documents mention international travel

AI ANSWER (Incorrect):
"The company provides $10,000 annually for international travel"

AI ANSWER (Correct):
"I don't have information about international travel policies. 
Please contact HR for details."

HALLUCINATION CHECK:
- Answer provides specific number not in documents
- Should indicate information is not available
- Status: HALLUCINATION (inventing specific details)
```

---

### Case 4: Well-Grounded Answer
```
DOCUMENT:
"Employees can take 10 sick leave days per year. 
Medical certificate is required for absences exceeding 3 consecutive days."

AI ANSWER:
"You are entitled to 10 days of sick leave annually. 
If you're absent for more than 3 days, you'll need a medical certificate."

HALLUCINATION CHECK:
- "10 sick leave days" - CORRECT
- "Annual" - CORRECT
- "Medical certificate for >3 days" - CORRECT
- Status: NO HALLUCINATION (fully grounded)
```

---

## Hallucination Detection Checklist

For each AI-generated answer:

- [ ] Is the main claim in the source document?
- [ ] Are all numbers and dates accurate?
- [ ] Are qualifications (like "2 days per week") included?
- [ ] Are exceptions mentioned in the document stated?
- [ ] Does the answer avoid speculation?
- [ ] Does the answer know when NOT to answer?
- [ ] Are multi-claim answers fully supported?

---

## Common Hallucination Patterns

### Pattern 1: Adding Details
```
Source: "Employees get annual leave"
AI: "Employees get 18 days of annual leave and can carry over 5 days"
(carry-over is invented)
```

### Pattern 2: Removing Constraints
```
Source: "Can work from home 2 days/week with approval"
AI: "Can work from home frequently"
(removed frequency limit and approval requirement)
```

### Pattern 3: Generalizing  
```
Source: "Most employees use the HR portal"
AI: "All employees must use the HR portal"
(changed "most" to "all")
```

### Pattern 4: Mixing Documents
```
Source A: "18 days annual leave"
Source B: "5 vacation days"
AI: "23 days total leave"
(incorrectly combines different types of leave)
```

### Pattern 5: Creating New Information
```
Source: "Performance review in December"
AI: "Salary increase is 5% annual"
(salary amount not mentioned anywhere)
```

---

## Mitigation Strategies

### 1. Prompt Engineering
Include explicit instruction to system:
```
"Only answer based on the provided documents.
If information is not in the documents, say: 
'I don't have this information.'"
```

### 2. Context Truncation
Limit context size to prevent confusion from multiple documents:
```
Max: 2 most relevant documents per query
This reduces mixing documents incorrectly
```

### 3. Post-Processing Verification
```
For each claim in answer:
1. Extract claim
2. Search for evidence in context
3. Remove unsupported claims
4. Replace with "insufficient information"
```

### 4. Confidence Scoring
Ask LLM to score confidence for each claim:
```
Claim: "18 days annual leave"
Confidence: 95% (directly in document)

Claim: "Can carry over 5 days"
Confidence: 5% (not in document)
```

### 5. Citation Requirements
Force model to cite sources:
```
"According to leave_policy.pdf, employees get 18 days
of annual leave."
```

---

## Evaluation Metrics

### Hallucination Rate
```
Number of hallucinations / Total number of claims
Lower is better
Target: < 5%
```

### Supported Claim Rate
```
Number of supported claims / Total claims
Higher is better
Target: > 95%
```

### False Confidence
```
Claims marked high confidence but hallucinated
Track these separately (very problematic)
```

---

## Summary

| Aspect | Action |
|--------|--------|
| **Detection** | Verify each claim against source documents |
| **Prevention** | Use explicit prompts to constrain generation |
| **Mitigation** | Implement post-processing verification |
| **Monitoring** | Track hallucination rate per query type |
| **Escalation** | Flag and review high-confidence hallucinations |

**Key Principle**: Trust but verify. Always validate AI-generated content against source material before using it.
