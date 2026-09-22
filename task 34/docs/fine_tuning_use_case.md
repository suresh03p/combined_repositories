# Fine-Tuning Use Case

## Selected use case
Customer Support Intent Classification

## Problem definition
We want a model to read a customer message and predict the correct intent category so the support team can route it to the right queue.

### Input
Customer message

### Output
Intent label

Example:

```text
Input:
"I cannot log into my account."

Output:
account_login_issue
```

## Why this is a good fine-tuning use case
This task has a clear target, repeated patterns, and a fixed label set. The model needs to learn repeated language patterns for support issues such as account login, refund, payment, technical problems, and general questions.

## Why it is not a good RAG case
The task does not require external retrieval of facts on every request. The needed behavior is classification based on message patterns and domain wording, not on current documents.

## Controlled and safe scope
The dataset avoids private production data and uses synthetic but realistic customer messages. That keeps the experiment controlled and safe while still representing realistic support traffic.

## Expected outcome
The fine-tuned model should consistently map similar customer messages to the correct intent class, reducing classification noise and increasing routing precision.
