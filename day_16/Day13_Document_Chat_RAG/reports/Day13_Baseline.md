# Day 13 Baseline: Day 11 RAG System

## What Was Run
The Day 11 project is the neighboring `RAG` folder. Its pipeline loads TXT policies, embeds chunks with `all-MiniLM-L6-v2`, searches Chroma, and answers by concatenating the first two retrieved chunks. The baseline uses no conversation memory, page metadata, query rewriting, re-ranking, or citations beyond source/chunk labels.

## Test Records

| Question | Retrieved Documents | Answer | Source | Correct / Incorrect |
|---|---|---|---|---|
| How do I apply for leave? | `leave_policy.txt` and related company chunks | Apply through the HR portal with dates, leave type, and any required note. | `leave_policy.txt` | Correct |
| Who approves leave? | `leave_policy.txt` | Managers review and approve leave requests. | `leave_policy.txt` | Correct |
| What is the salary policy? | `salary_policy.txt` | Salary is processed monthly through Payroll; payslips are in the payroll portal. | `salary_policy.txt` | Correct |
| What is the attendance policy? | `attendance_policy.txt` | Employees follow their agreed schedule and notify their manager before a late or absent shift. | `attendance_policy.txt` | Correct |

These expected answers are grounded in the Day 11 policy files. Runtime model loading depends on the Day 11 virtual environment and model availability; the Day 13 implementation has an offline deterministic fallback for repeatable tests.

## 1. What Already Works?
- TXT ingestion and overlapping chunks.
- Embeddings and persistent Chroma collection.
- Top-k semantic retrieval.
- A context-grounded extractive answer with source and chunk labels.
- Basic retrieval tests.

## 2. What Is Still Missing?
- PDF and HTML ingestion.
- Validation, cleaning, duplicate detection, and document IDs.
- Page, section, and citation metadata.
- Re-ranking and bounded context construction.
- Conversation memory and follow-up query rewriting.
- Explicit failure handling and a 20-question evaluation set.
- Upload/chat application boundary and operational concerns.

## 3. What Is Required for Real Document Chat?
An application needs a durable ingestion pipeline, reliable provenance, a replaceable embedding/vector layer, source-aware retrieval, answer grounding, explicit no-answer behavior, conversation-aware rewriting, access controls, observability, evaluation, and a user interface/API for uploading and asking questions.