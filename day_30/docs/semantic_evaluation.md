# Semantic Answer Evaluation

Semantic evaluation checks whether two responses have equivalent meaning, even if the wording differs.

## Why exact match is not enough

Exact comparison fails in natural-language tasks because valid responses can be phrased differently.

Example:

Expected: Refund available within 7 days.
Actual: Customers can request a refund during the first seven days.

These are semantically equivalent even though the strings differ.

## Semantic evaluation approach

A semantic evaluator should judge whether the answer preserves the same meaning as the expected answer.

Key dimensions:

- same fact or policy
- same time window or obligation
- same entity or subject
- no contradiction
- same intent

## Example judgment

Question: What is the refund policy?
Expected: Refunds are available within 7 days.
Actual: Customers can request a refund during the first seven days.

Decision: CORRECT, because the meaning matches.

## Operational guidance

Semantic evaluation is useful for:

- paraphrased answers
- equivalent time expressions
- synonyms and wording variations
- domain-specific policy questions

Semantic evaluation should complement, not replace, exact match and groundedness checks.
