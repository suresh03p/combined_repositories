"""Evaluate whether the top semantic result comes from the expected policy."""

from src.semantic_search import search_company_knowledge

QUESTIONS = [
    ("How do I apply for leave?", "leave_policy.txt"),
    ("Who approves leave?", "leave_policy.txt"),
    ("How can I request vacation?", "leave_policy.txt"),
    ("When is salary processed?", "salary_policy.txt"),
    ("Where can I find my payslip?", "salary_policy.txt"),
    ("What happens if I come late?", "attendance_policy.txt"),
    ("What is the attendance policy?", "attendance_policy.txt"),
    ("Where do I report harassment?", "hr_policy.txt"),
    ("How should I protect confidential information?", "company_policy.txt"),
    ("What should I do about a phishing message?", "company_policy.txt"),
]


if __name__ == "__main__":
    correct = 0
    for question, expected in QUESTIONS:
        results = search_company_knowledge(question, top_k=1)
        actual = results[0]["metadata"]["source"] if results else "none"
        is_correct = actual == expected
        correct += is_correct
        print(f"Question: {question}")
        print(f"Expected Source: {expected}")
        print(f"Retrieved Source: {actual}")
        print("Correct" if is_correct else "Incorrect")
        print()
    print(f"{correct} / {len(QUESTIONS)} correct")
    print(f"Retrieval Accuracy = {correct / len(QUESTIONS):.0%}")
