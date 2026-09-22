# Complete RAG Pipeline
Documents -> Load -> Extract -> Clean -> Split -> Chunk -> Embed -> Store -> Retrieve -> Rerank -> Context -> Prompt -> LLM -> Answer

## Stage Template
For each stage:
- Purpose
- Input
- Output
- Possible Failure

Load: read files.
Extract: get text.
Clean: remove noise.
Split: break into sections.
Chunk: create retrievable units.
Embed: create vectors.
Store: save vectors.
Retrieve: find candidates.
Rerank: improve ordering.
Context: build evidence.
Prompt: instruction + context.
LLM: generate answer.
Answer: final response.
