# Complete RAG Pipeline

| Stage | Purpose | Input | Output | Possible failure |
|---|---|---|---|---|
| Documents | Define source corpus | PDFs/files | Source files | Missing or stale files |
| Load | Read source bytes | File path | File content | Permission/parser error |
| Extract | Recover text and page boundaries | PDF | Page records | Scanned PDF or bad layout |
| Clean | Normalize noise without losing meaning | Page text | Clean text | Removing headings or punctuation |
| Split | Choose useful boundaries | Clean text | Sections | Boundary detection failure |
| Chunk | Create retrievable units | Sections | Chunk records | Too large, too small, or duplicated |
| Embed | Map text to vectors | Chunk text | Embeddings | Poor model/domain mismatch |
| Store | Persist vectors and metadata | Records | Index | Lost metadata or stale index |
| Retrieve | Find candidates | Query/index | Ranked candidates | Keyword or semantic mismatch |
| Rerank | Improve ordering with richer scoring | Candidates/query | Final ranking | Expensive or biased scorer |
| Context | Assemble evidence | Top chunks | Context text | Too much or contradictory context |
| Prompt | Give task and evidence to model | Query/context | Prompt | Weak instructions/injection |
| LLM | Generate grounded response | Prompt | Draft answer | Hallucination or model failure |
| Answer | Return text and citations | Draft/sources | User response | Missing provenance |
