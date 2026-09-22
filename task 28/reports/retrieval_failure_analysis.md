# Retrieval Failure Analysis

Use this table while running experiments. The examples cover the common failure modes required by the exercise.

| Query | Failure | Root cause | Fix |
|---|---|---|---|
| Leave policy | Wrong chunk | Chunk too large | Reduce chunk size |
| Reimbursement | Missing result | Bad extraction | Fix PDF parser/OCR |
| Remote work | No match | Keyword mismatch | Add semantic or hybrid retrieval |
| Policy 17-B | No match | Wrong embedding vocabulary | Add keyword search |
| Annual allowance | Incomplete answer | Poor overlap | Increase overlap modestly |
| Leave days | Duplicate context | Duplicate content | Deduplicate chunks |
| WFH eligibility | Unauthorized result | Missing metadata filter | Filter tenant/access before retrieval |
| Probation | Weak rank | Reranking failure | Tune second-stage scorer |
| Attendance hours | Irrelevant top five | Wrong top-K | Evaluate several K values |
| Expense receipt | Garbled text | PDF extraction layout | Use layout-aware parser/OCR |

Aggressive text cleaning can remove punctuation, table structure, section labels, or negation. That changes the evidence and can make a fluent answer wrong.
