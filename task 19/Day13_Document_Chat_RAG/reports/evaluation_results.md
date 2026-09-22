# Evaluation Results

The evaluation set in `src/rag_answer_evaluation.py` contains 20 policy questions. Run it after loading the sample corpus to calculate the three measures:

- **Retrieval accuracy:** expected evidence appears in retrieved context.
- **Answer accuracy:** generated answer contains the expected policy fact.
- **Citation accuracy:** answer citations come from retrieved metadata.

Retrieval and answer accuracy differ because a retriever may find the right chunk while an answer generator omits or misstates the fact. Citation accuracy is separate because an answer can be correct while pointing to incomplete or wrong provenance.