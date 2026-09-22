# Prompting vs RAG vs Fine-Tuning

| Requirement | Prompting | RAG | Fine-Tuning |
|---|---|---|---|
| Change response style | Good for tone, formatting, and simple behavioral instructions | Not the primary tool; style changes can be partially influenced through retrieval, but not durable | Strong when a consistent style needs to be learned across many examples |
| Add private documents | Poor fit unless documents are manually embedded in the prompt | Best option; retrieve private documents at runtime | Not appropriate for private documents by itself; it changes behavior, not document access |
| Improve repeated task behavior | Helps for one-off prompts but may be inconsistent across sessions | Can help with retrieval-based context, but not task learning itself | Best option when the same task repeats with stable patterns |
| Frequently changing information | Weak because prompts are static and may become stale | Best option because current facts can be fetched from external sources | Poor fit because model behavior is not updated automatically with new facts |
| Enforce output format | Very effective with prompt instructions and examples | Useful only when format is combined with retrieved context | Strong when the model must consistently produce a fixed schema or label set |
| Domain-specific behavior | Useful for quick adaptation with prompt guidance | Helpful when domain knowledge lives in documents | Best choice when domain behavior must become part of the model’s learned patterns |
| Add current knowledge | Not suitable for fresh knowledge unless manually included | Best choice; retrieves live or latest information | Not the right tool for current knowledge; fine-tuning is for learned behavior |

## Why each approach is appropriate

### Prompting
Prompting is appropriate when the user needs a quick change in tone, format, or instructions. It is easy to test and inexpensive, but it is limited by the model’s base behavior and the prompt context that is passed at runtime.

### RAG
RAG is appropriate when the task requires access to external documents, private company knowledge, or frequently updated information. It retrieves relevant information during inference and is highly effective for knowledge-intensive workflows.

### Fine-tuning
Fine-tuning is appropriate when a task is repeated, stable, and the model should learn consistent behavior such as classification, structured extraction, or domain-specific response patterns. It changes model behavior rather than adding runtime knowledge.

## Practical rule
Use prompting for flexibility, RAG for facts, and fine-tuning for task behavior. Do not fine-tune just to add documents or dynamic knowledge; that is usually a retrieval problem rather than a model-training problem.
