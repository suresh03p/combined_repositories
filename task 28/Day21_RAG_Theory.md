# RAG From Zero

```text
User Question
      |
   Retriever
      |
Relevant Documents
      |
    Context
      |
     LLM
      |
    Answer
```

- **User question:** the information need expressed in natural language.
- **Retriever:** searches indexed chunks and returns likely relevant evidence.
- **Relevant documents:** source passages selected by semantic, keyword, or hybrid search.
- **Context:** the small, ordered evidence package placed into the prompt.
- **LLM:** reads the question plus context and generates a response.
- **Answer:** the response, ideally grounded in the supplied sources.

## Important question

A powerful LLM cannot reliably compensate for wrong retrieval. The reasoning chain is:

```text
Bad Retrieval -> Bad Context -> Bad Answer
```

The model may produce fluent text, but it lacks the correct evidence. It can guess, combine unrelated policy text, or confidently state an unsupported answer. Better generation does not repair missing or unauthorized source material; retrieval quality is therefore a first-class part of answer quality.
