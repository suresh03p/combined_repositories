# AI Testing Fundamentals

## Unit Testing vs Integration Testing vs API Testing vs Load Testing vs AI Evaluation

### Unit Testing
Unit tests validate a single component or function in isolation. They usually verify deterministic logic such as parsing, formatting, transformations, and decision rules.

Example:

- a function that calculates tax
- a validator that checks a date format
- a parser that extracts a customer ID

### Integration Testing
Integration tests validate that different components work together correctly. The goal is to verify data flow and interfaces between modules.

Example:

- API layer calls the database
- retrieval service returns documents to the prompt builder
- application layer calls the LLM client

### API Testing
API tests validate HTTP behavior, status codes, payload structure, authentication, validation, and contract compliance.

Example:

- POST /chat returns HTTP 200
- response contains a `result` object
- invalid token returns 401

### Load Testing
Load tests determine whether a system remains stable under volume and concurrency. This checks throughput, latency, timeout behavior, and bottlenecks.

Example:

- 1,000 concurrent user requests
- 10,000 prompts processed per minute
- p95 latency remains below a threshold

### AI Evaluation
AI evaluation checks whether the AI system produces answers that are correct, relevant, grounded, safe, and useful. LLMs are not deterministic by default, so output quality must be assessed using metrics and test sets.

## Why a technically valid response can still be a bad answer

A response may be structurally valid and still be wrong.

Example:

Question: What is our refund policy?

AI: Our refund policy allows refunds within 30 days.

Actual policy: Refunds are allowed within 7 days.

Even if the model responds fluently and the API returns HTTP 200, the answer is incorrect. AI quality is not merely a transport-level success indicator.

## Deterministic vs non-deterministic output

Traditional software often has deterministic output for the same input.

Example:

```python
# Traditional logic
if x > 10:
    return "high"
else:
    return "low"
```

This produces the same output for the same input.

LLMs are different. They can produce different wording for equivalent answers.

Example:

Expected: Python is a programming language.

Possible valid answer: Python is a high-level programming language.

This means AI testing must evaluate meaning, not only exact string equality.

## Principle

AI quality must be measured continuously, not assumed.
