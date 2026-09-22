# AI Evaluation Terminology - Complete Glossary

## Core Evaluation Concepts

### 1. Evaluation
**Definition**: The process of measuring and assessing the quality, performance, and correctness of an AI system using predefined metrics and criteria.

**Simple Example**:
- You built a chatbot that answers HR questions
- You need to check: Does it give correct answers? Is it fast enough? Does it understand questions?
- Testing the bot against 100 questions and measuring accuracy = Evaluation

---

### 2. Evaluation Dataset
**Definition**: A collection of test inputs (questions, prompts, scenarios) used to assess AI system performance. It serves as the benchmark for testing.

**Simple Example**:
```csv
Q1: What is the annual leave allowance?
Q2: How do I apply for sick leave?
Q3: What is the office policy on remote work?
...
(50-100 questions total)
```
This becomes your evaluation dataset.

---

### 3. Ground Truth
**Definition**: The correct, authoritative answer or label that is accepted as the standard for evaluation. It represents "what is actually correct."

**Simple Example**:
```
Question: "What is the annual leave allowance?"
Ground Truth: "Employees receive 18 annual leave days"
(This is the official, correct answer)
```

---

### 4. Reference Answer
**Definition**: An example of a correct answer provided for comparison. Similar to ground truth, but acknowledges there may be multiple valid reference answers.

**Simple Example**:
```
Question: "How do I apply for leave?"

Reference Answer 1: "Submit a form through the HR portal"
Reference Answer 2: "Use the company HR system to request leave"

Both are acceptable reference answers.
```

---

### 5. LLM Judge
**Definition**: Using another Language Model to evaluate the quality of an AI system's output by comparing it against criteria and providing a score.

**Simple Example**:
```
AI System Output: "You can take 18 days of annual leave"
Reference Answer: "Employees get 18 annual leave days"
LLM Judge: "These are semantically equivalent. Score: 5/5"
```

---

### 6. Relevance
**Definition**: Whether the AI's answer addresses the specific question asked and is on-topic.

**Simple Example**:
```
Question: "What is the annual leave policy?"

Relevant Answer: "Employees receive 18 annual leave days"
Not Relevant: "The office has 200 employees"
```

---

### 7. Faithfulness
**Definition**: Whether the AI answer is supported by and consistent with the source documents (retrieved context), not contradicting them.

**Simple Example**:
```
Source Document: "Employees receive 18 annual leave days"

Faithful Answer: "You get 18 days of annual leave"
Not Faithful: "You get 25 days of annual leave"
(contradicts the source)
```

---

### 8. Groundedness
**Definition**: Whether the AI answer can be traced back to specific facts or quotes in the source documents; the opposite of hallucination.

**Simple Example**:
```
Source Document: "Annual leave policy effective Jan 1, 2024: 18 days"

Grounded: "As per the 2024 policy, employees get 18 days"
Not Grounded: "The company has always given 20 days"
(can't find this in the document)
```

---

### 9. Context Relevance
**Definition**: Whether the retrieved documents actually contain information useful for answering the question.

**Simple Example**:
```
Question: "What is the annual leave allowance?"

Retrieved Documents:
1. leave_policy.pdf (CONTEXT RELEVANT ✓)
2. office_location.pdf (NOT RELEVANT ✗)
3. employee_handbook.pdf (CONTEXT RELEVANT ✓)
```

---

### 10. Hallucination
**Definition**: When an AI generates information that is false, unsupported, or invented, not found in the source documents.

**Simple Example**:
```
Source Document: "Employees get 18 annual leave days"

AI Answer: "Employees also get 10 extra vacation days per year"
(This extra information doesn't exist in the document = Hallucination)
```

---

### 11. Precision
**Definition**: Of all the items the system retrieved/predicted as relevant, how many were actually correct?

**Formula**: `Correct Items / Total Retrieved Items`

**Simple Example**:
```
You retrieved 5 documents for "leave policy"
3 were actually relevant
Precision = 3/5 = 0.60 (60%)
```

---

### 12. Recall
**Definition**: Of all the relevant items that should have been retrieved, how many did the system actually retrieve?

**Formula**: `Retrieved Correct Items / Total Correct Items`

**Simple Example**:
```
There are 5 documents about "leave policy"
System found 4 of them
Recall = 4/5 = 0.80 (80%)
```

---

### 13. MRR (Mean Reciprocal Rank)
**Definition**: Measures how high up the correct answer appears in the ranked results. Rewards finding the correct answer early.

**Formula**: `1 / (Rank of First Correct Result)`

**Simple Example**:
```
If correct document is at Rank 1: MRR = 1/1 = 1.0
If correct document is at Rank 3: MRR = 1/3 = 0.33
If correct document is at Rank 5: MRR = 1/5 = 0.20
```

---

### 14. Latency
**Definition**: The time taken for the AI system to respond to a query, from input to output. Measured in seconds or milliseconds.

**Simple Example**:
```
User asks question at 10:00:00.000
System responds at 10:00:03.456
Latency = 3.456 seconds
```

---

### 15. Throughput
**Definition**: The number of requests the system can handle per unit of time (e.g., requests per second).

**Simple Example**:
```
In 1 minute, the system processes 60 requests
Throughput = 60 requests/minute = 1 request/second
```

---

### 16. Token Usage
**Definition**: The number of tokens (word pieces) consumed by an LLM for a request, including both input and output tokens. Used to calculate costs.

**Simple Example**:
```
Input: "What is the leave policy?" = 6 tokens
Context: 500 words = ~680 tokens
Output: "You get 18 days" = 4 tokens
Total Tokens Used: ~690 tokens
```

---

### 17. Cost
**Definition**: The financial cost of running the AI system, typically calculated from token usage and model pricing.

**Simple Example**:
```
Model charges $0.005 per 1K input tokens, $0.015 per 1K output tokens
1000 input tokens = $0.005
200 output tokens = $0.003
Total Cost = $0.008 per request
```

---

### 18. Observability
**Definition**: The ability to monitor, measure, and understand what's happening inside the AI system (logs, metrics, traces).

**Simple Example**:
```
Track each request with:
- Time taken
- Tokens used
- Documents retrieved
- LLM response quality
This is observability.
```

---

### 19. Trace
**Definition**: A detailed log of how a request flows through the entire system, recording each step from input to output.

**Simple Example**:
```
Trace ID: TR-001
├─ User Input: "What is the leave policy?"
├─ RAG Retrieval: Retrieved 3 documents (0.2s)
├─ LLM Generation: Generated answer (3.2s)
├─ Output: "18 annual leave days"
└─ Total Time: 3.4s
```

---

### 20. Completeness
**Definition**: Whether the AI answer covers all key points and relevant information needed to fully answer the question.

**Simple Example**:
```
Question: "What are the sick leave rules?"

Incomplete: "You get 10 sick days per year"
(missing: how to apply, approval process, documentation needed)

Complete: "You get 10 sick days per year. Apply through HR portal. 
Doctor's note required for absences over 3 days."
```

---

### 21. Accuracy
**Definition**: Whether the factual claims in the AI answer are correct and match ground truth.

**Simple Example**:
```
Question: "How many annual leave days do employees get?"
Correct Answer: "18 days"
AI Answer: "18 days"
Accuracy: 100% ✓
```

---

### 22. Precision@K
**Definition**: Of the top K retrieved results, how many are relevant?

**Simple Example**:
```
Top 5 results for "leave policy":
1. leave_policy.pdf (relevant ✓)
2. handbook.pdf (relevant ✓)
3. training.pdf (not relevant ✗)
4. office_rules.pdf (relevant ✓)
5. benefits.pdf (relevant ✓)

Precision@5 = 4/5 = 0.80
```

---

### 23. Recall@K
**Definition**: Of all relevant documents, how many appear in the top K results?

**Simple Example**:
```
Total relevant documents for "leave policy": 5
Top 5 results returned by system: 4 of them

Recall@5 = 4/5 = 0.80
```

---

### 24. F1-Score
**Definition**: Harmonic mean of Precision and Recall, providing a single score that balances both metrics.

**Formula**: `2 × (Precision × Recall) / (Precision + Recall)`

**Simple Example**:
```
Precision = 0.80
Recall = 0.75
F1-Score = 2 × (0.80 × 0.75) / (0.80 + 0.75) = 0.77
```

---

## Summary Table

| Term | What It Measures | Good Score |
|------|------------------|-----------|
| Relevance | Answer addresses the question | 4.5+/5 |
| Faithfulness | Answer matches source documents | 4.5+/5 |
| Precision@5 | Quality of top 5 results | 0.8+ |
| Recall@5 | Coverage of top 5 results | 0.8+ |
| MRR | How early correct answer appears | 0.9+ |
| Latency | Time to respond | <5 seconds |
| Accuracy | Factual correctness | 95%+ |

---

**Key Insight**: Evaluation is multi-dimensional. No single metric tells the whole story. You need to measure relevance, faithfulness, speed, cost, and completeness together.
