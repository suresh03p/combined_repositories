# Keyword Search vs Semantic Search

Question: `How can I take vacation?`

Document: `Employees may request leave through the HR portal.`

A keyword search may fail because `vacation` and `leave` are different strings. Semantic search embeds both texts and can recognize that they describe related time away from work.

## Ten comparison questions

| # | Question | Expected source | What to observe |
| --- | --- | --- | --- |
| 1 | How can I take vacation? | `leave_policy.txt` | Vacation and leave are related ideas. |
| 2 | Who signs off on time away? | `leave_policy.txt` | Approval may be expressed as signing off. |
| 3 | When does my monthly pay arrive? | `salary_policy.txt` | Pay and salary are related terms. |
| 4 | What should I do if I am late? | `attendance_policy.txt` | Lateness may not match the word attendance. |
| 5 | Where do I report a workplace concern? | `hr_policy.txt` | Report and raise are related actions. |
| 6 | How do I protect private company information? | `company_policy.txt` | Private and confidential are related. |
| 7 | Can I ask for time off before a trip? | `leave_policy.txt` | Time off is a vacation concept. |
| 8 | Why is money missing from my paycheck? | `salary_policy.txt` | Paycheck and salary are related. |
| 9 | What if my internet stops while working remotely? | `attendance_policy.txt` | Connectivity and remote attendance are related. |
| 10 | What does the people team help with? | `hr_policy.txt` | People team refers to HR. |

## How to compare

Run `document_store.py` once, then use `semantic_search.py` with each question. Record the top source. For keyword search, implement a small baseline with lowercased tokens and count how many question words occur in each document. Compare the top source from both methods with the expected source.

Keyword search is still useful for exact names, IDs, policy codes, and rare terms. Semantic search is useful when a question uses different words from the document. A hybrid retriever can combine both signals instead of pretending one method wins every case. Evaluation should use questions written by a person, not only copied sentences.
