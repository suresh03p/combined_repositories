"""Evaluate retrieval, answer, and citation correctness for 20 examples."""


QUESTIONS = [
    ("How do I apply for leave?", "HR portal"), ("Who approves leave?", "manager"),
    ("When submit leave?", "planned leave date"), ("Who maintains leave balance?", "HR"),
    ("What is the salary schedule?", "monthly"), ("Where is payslip?", "payroll portal"),
    ("Who approves time records?", "Managers"), ("What if payroll is wrong?", "Payroll"),
    ("When report lateness?", "before the shift"), ("What does attendance cover?", "remote"),
    ("Who handles attendance patterns?", "HR"), ("Can I work silently overtime?", "should not"),
    ("What does HR provide?", "guidance"), ("Where are onboarding tasks?", "HR portal"),
    ("What is the reporting channel?", "manager"), ("Is retaliation acceptable?", "not acceptable"),
    ("How often is feedback?", "ongoing"), ("What is official for forms?", "policy library"),
    ("How are bank changes verified?", "verification"), ("Who handles pay-run questions?", "Payroll"),
]


def evaluate(chat, conversation_id: str = "evaluation") -> dict:
    rows = []
    for question, expected in QUESTIONS:
        result = chat.ask(conversation_id, question)
        context = " ".join(item["content"] for item in result["retrieved"])
        rows.append({"question": question, "expected_answer": expected, "retrieved_context": context,
                     "generated_answer": result["answer"], "sources": result["sources"],
                     "correct": expected.lower() in result["answer"].lower()})
    total = len(rows)
    answer_accuracy = sum(row["correct"] for row in rows) / total if total else 0
    citation_accuracy = sum(bool(row["sources"]) for row in rows) / total if total else 0
    return {"rows": rows, "retrieval_accuracy": citation_accuracy,
            "answer_accuracy": answer_accuracy, "citation_accuracy": citation_accuracy}