# Memory vs Retrieval

Conversation memory answers: **What did the user say earlier?** It stores messages by conversation ID and helps resolve references such as “it” or “that policy.”

Knowledge retrieval answers: **What do the uploaded documents say?** It searches cleaned, chunked document content and returns evidence with source, page, section, and score.

```text
Conversation History -> Understand Question -> Rewrite Question
-> Knowledge Retrieval -> Relevant Documents
```

The entire conversation should not be blindly embedded into the vector database. Chit-chat, old topics, assistant wording, and pronouns dilute the terms that describe the current information need. The correct boundary is to use history to produce a standalone question, then search only that question against document chunks.