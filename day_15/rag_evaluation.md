# RAG Evaluation and Hallucination

A RAG system should answer from retrieved context. It should not fill gaps with confident guesses.

## Questions with answers in the collection

- How do I apply for leave? The leave policy says to use the HR portal and submit before the planned date.
- Who approves leave? Managers review and approve leave requests.
- When is salary processed? Salary is processed monthly after Payroll completes its checks.
- What happens if I am late? Notify the manager before the shift when possible; repeated lateness may require a conversation with the manager and HR.

## Questions that are intentionally absent

- What is the company CEO's favorite food?
- How many employees are there?
- What is the company's revenue?

The correct response to each absent question is:

> Information not available in the provided company documents.

The simple root-level pipeline demonstrates retrieval and returns the retrieved context in an extractive answer. In a production system, the context and question would be sent to an LLM with an instruction like:

```text
Answer the user's question using only the provided context.
If the answer is not available in the context, say:
"Information not available in the provided company documents."
Do not invent names, numbers, dates, or policies.
```

Evaluation has two parts. Retrieval evaluation asks whether a relevant source appeared in the top results. Answer evaluation asks whether the response is supported by the context and whether it refuses unsupported claims. A system can retrieve the right document and still produce a bad answer, so measure both.
