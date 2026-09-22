# Semantic vs Keyword vs Hybrid

| Query | Semantic search | Keyword search | Better |
|---|---|---|---|
| Leave allowance | Finds annual leave paraphrases | Finds exact leave terms | Hybrid |
| Policy ID | May miss exact identifier | Strong exact match | Keyword |
| WFH eligibility | Finds work-from-home meaning | Finds WFH token | Hybrid |
| Employee ID | Weak unless indexed as text | Strong exact match | Keyword |

Semantic retrieval is strongest for meaning and paraphrasing. Keyword retrieval is strongest for names, IDs, policy numbers, and exact technical terms. Hybrid ranking combines both signals. Experiment with `0.5/0.5`, `0.7/0.3`, and `0.8/0.2`; the best choice depends on the evaluation set.
