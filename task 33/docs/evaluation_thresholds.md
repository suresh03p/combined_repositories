# AI Evaluation Thresholds

These minimum thresholds define whether an AI application is acceptable for continued deployment.

## Default thresholds

- Relevance >= 0.80
- Groundedness >= 0.85
- Retrieval Hit Rate >= 0.90
- Hallucination Rate <= 0.05
- Overall Quality >= 0.80

## Interpretation

If the application falls below a threshold, the system should fail the quality gate and block deployment.

Example:

- relevance is 0.72 -> FAIL
- groundedness is 0.88 -> PASS
- retrieval hit rate is 0.86 -> FAIL
- hallucination rate is 0.08 -> FAIL

## Quality gate rule

```text
Run Evaluation
  ↓
Calculate Scores
  ↓
Compare to threshold
  ↓
PASS or FAIL
```

A deployment pipeline should only continue when all critical thresholds pass.
