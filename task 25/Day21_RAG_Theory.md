# RAG Theory
User Question -> Retriever -> Relevant Documents -> Context -> LLM -> Answer

## Components
- Retriever: Finds relevant documents.
- Relevant Documents: Retrieved knowledge.
- Context: Selected information given to LLM.
- LLM: Generates response from context.
- Answer: Final output.

## Important Question
Can a powerful LLM recover from wrong retrieval?

Usually no.
Bad Retrieval -> Bad Context -> Bad Answer.
Even a strong LLM depends on the evidence it receives. If retrieval returns incorrect or unrelated documents, the generated answer becomes unreliable because grounding information is wrong or missing.
