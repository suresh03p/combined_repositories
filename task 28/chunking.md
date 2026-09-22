# Chunking From Zero

A whole document is usually too large and too broad for a retriever. Chunks make indexing, matching, citations, and context budgets manageable.

| Whole document | Chunks |
|---|---|
| High context and token cost | Smaller prompt cost |
| Weak retrieval precision | More focused matches |
| One citation covers too much | Page/section-level citations |
| May exceed model limits | Fits a controlled budget |

`Chunk size` controls how much text travels with a match. Small chunks improve precision but may lose context; large chunks improve context but dilute relevance. `Chunk overlap` repeats boundary text so a sentence split across chunks remains retrievable. Overlap improves recall but increases storage and duplicate context. Retrieval precision means returned results are relevant; recall means relevant results are not missed.

```text
Document -> Chunk 1 -> Chunk 2 -> Chunk 3 -> Chunk 4
```

Recursive chunking tries paragraph, sentence, then word boundaries before making a hard character cut.
