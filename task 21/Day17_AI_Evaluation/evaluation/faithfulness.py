"""
TASK 11: RAG Faithfulness Evaluation
Evaluates whether AI answers are supported by and faithful to source documents.

Faithfulness = Answer is supported by the retrieved context, not contradicting it.
"""

import json
from typing import List, Tuple


class FaithfulnessEvaluator:
    """Evaluate answer faithfulness to source documents."""
    
    def __init__(self):
        self.evaluations = []
    
    @staticmethod
    def evaluate_faithfulness(context: str, answer: str) -> dict:
        """
        Evaluate if an answer is faithful to its source context.
        
        Three levels:
        - Faithful (2): Answer fully supported by context
        - Partially Faithful (1): Answer partially supported, some claims unsupported
        - Unsupported (0): Answer contradicts context or is not in context
        """
        
        # Convert to lowercase for comparison
        context_lower = context.lower()
        answer_lower = answer.lower()
        
        # Extract key claims from answer (simple noun phrases)
        answer_words = set(word.lower() for word in answer.split() if len(word) > 3)
        context_words = set(word.lower() for word in context.split() if len(word) > 3)
        
        # Calculate word overlap
        overlap = len(answer_words & context_words)
        total_answer_words = len(answer_words)
        
        if total_answer_words == 0:
            return {"score": 2, "label": "Faithful", "overlap_percentage": 100.0}
        
        overlap_percentage = (overlap / total_answer_words) * 100
        
        # Scoring logic
        if overlap_percentage >= 80:
            score = 2  # Faithful
            label = "Faithful"
        elif overlap_percentage >= 50:
            score = 1  # Partially Faithful
            label = "Partially Faithful"
        else:
            score = 0  # Unsupported/Contradicting
            label = "Unsupported"
        
        return {
            "score": score,
            "label": label,
            "overlap_percentage": round(overlap_percentage, 1)
        }
    
    
    def evaluate(self, question_id: str, question: str, context: str, 
                answer: str, category: str = "General") -> dict:
        """Evaluate a single question-answer-context triplet."""
        
        result = self.evaluate_faithfulness(context, answer)
        
        evaluation = {
            "question_id": question_id,
            "question": question,
            "context": context,
            "answer": answer,
            "category": category,
            "faithfulness_score": result["score"],
            "faithfulness_label": result["label"],
            "overlap_percentage": result["overlap_percentage"]
        }
        
        self.evaluations.append(evaluation)
        return evaluation
    
    
    def generate_report(self):
        """Generate faithfulness evaluation report."""
        
        if not self.evaluations:
            print("No evaluations to report.")
            return
        
        total = len(self.evaluations)
        faithful = sum(1 for e in self.evaluations if e["faithfulness_score"] == 2)
        partial = sum(1 for e in self.evaluations if e["faithfulness_score"] == 1)
        unsupported = sum(1 for e in self.evaluations if e["faithfulness_score"] == 0)
        
        avg_overlap = sum(e["overlap_percentage"] for e in self.evaluations) / total
        
        print("\n" + "="*100)
        print("RAG FAITHFULNESS EVALUATION REPORT")
        print("="*100)
        
        print(f"\nTotal Evaluations: {total}\n")
        
        # Summary statistics
        print(f"{'Faithfulness Level':<25} {'Count':<10} {'Percentage':<12}")
        print("-" * 75)
        print(f"{'Faithful':<25} {faithful:<10} {faithful/total*100:>10.1f}%")
        print(f"{'Partially Faithful':<25} {partial:<10} {partial/total*100:>10.1f}%")
        print(f"{'Unsupported':<25} {unsupported:<10} {unsupported/total*100:>10.1f}%")
        
        print(f"\n{'Average Context Overlap:':<40} {avg_overlap:.1f}%")
        
        # Category breakdown
        categories = {}
        for e in self.evaluations:
            cat = e.get("category", "General")
            if cat not in categories:
                categories[cat] = {"total": 0, "faithful": 0, "score_sum": 0}
            categories[cat]["total"] += 1
            categories[cat]["score_sum"] += e["faithfulness_score"]
            if e["faithfulness_score"] == 2:
                categories[cat]["faithful"] += 1
        
        if len(categories) > 1:
            print(f"\n{'BREAKDOWN BY CATEGORY':<100}")
            print("-" * 75)
            print(f"{'Category':<20} {'Total':<10} {'Faithful':<12} {'Rate':<12}")
            print("-" * 75)
            for cat, stats in sorted(categories.items()):
                rate = stats["faithful"] / stats["total"] * 100
                print(f"{cat:<20} {stats['total']:<10} {stats['faithful']:<12} {rate:>10.1f}%")
        
        # Detailed results
        print(f"\n{'DETAILED RESULTS':<100}")
        print("="*100)
        
        for i, eval_result in enumerate(self.evaluations, 1):
            status = "PASS" if eval_result["faithfulness_score"] == 2 else ("PARTIAL" if eval_result["faithfulness_score"] == 1 else "FAIL")
            print(f"\n[{i:2d}] {status} Q{eval_result['question_id']}: {eval_result['question'][:60]}")
            print(f"      Context: {eval_result['context'][:80]}")
            print(f"      Answer: {eval_result['answer'][:80]}")
            print(f"      Score: {eval_result['faithfulness_score']}/2 - {eval_result['faithfulness_label']}")
            print(f"      Overlap: {eval_result['overlap_percentage']:.1f}%")
        
        print("\n" + "="*100)
        print("FAITHFULNESS INSIGHTS")
        print("="*100)
        print(f"""
1. Faithfulness Score: {faithful/total*100:.1f}%
   - {faithful} answers were fully faithful to context
   - {partial} answers were partially faithful
   - {unsupported} answers contradicted or diverged from context
   
2. Context Overlap: {avg_overlap:.1f}%
   - Measures how much answer content comes from context
   - High overlap = faithful answer
   - Low overlap = potential hallucination
   
3. Common Faithfulness Issues:
   - Adding unsupported information
   - Generalizing beyond what's stated
   - Mixing multiple documents incorrectly
   - Inferring beyond source material
   
4. Action Items:
   - Review {unsupported} unsupported answers
   - Add grounding constraints to LLM prompt
   - Implement faithfulness scoring in pipeline
   - Train model to cite sources
   
Faithfulness is critical for trustworthy AI systems.
        """)
        print("="*100)
    
    
    def save_results(self, filepath: str = "evaluation/faithfulness_results.json"):
        """Save results to JSON."""
        data = {
            "evaluations": self.evaluations,
            "summary": {
                "total": len(self.evaluations),
                "faithful_count": sum(1 for e in self.evaluations if e["faithfulness_score"] == 2),
                "partial_count": sum(1 for e in self.evaluations if e["faithfulness_score"] == 1),
                "unsupported_count": sum(1 for e in self.evaluations if e["faithfulness_score"] == 0),
                "percentage_faithful": (sum(1 for e in self.evaluations if e["faithfulness_score"] == 2) / len(self.evaluations) * 100) if self.evaluations else 0,
                "average_overlap": sum(e["overlap_percentage"] for e in self.evaluations) / len(self.evaluations) if self.evaluations else 0
            }
        }
        
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2)
        
        print(f"\n[OK] Results saved to: {filepath}")


def main():
    """Run faithfulness evaluation."""
    
    evaluator = FaithfulnessEvaluator()
    
    print("Running Faithfulness Evaluation...\n")
    
    # Test cases: (question, context, answer, category)
    test_cases = [
        # Faithful answers
        {
            "id": "Q001",
            "question": "What is the annual leave allowance?",
            "context": "Employees receive 18 annual leave days per year.",
            "answer": "You get 18 days of annual leave.",
            "category": "Leave Policy"
        },
        {
            "id": "Q002",
            "question": "What is the WFH policy?",
            "context": "Employees can work from home up to 2 days per week.",
            "answer": "The policy allows 2 days per week working from home.",
            "category": "Work Policies"
        },
        {
            "id": "Q003",
            "question": "What is the maternity leave?",
            "context": "Female employees are entitled to 120 days of maternity leave.",
            "answer": "Maternity leave is 120 days for female employees.",
            "category": "Leave Policy"
        },
        # Partially faithful
        {
            "id": "Q004",
            "question": "What leave is available?",
            "context": "Annual leave is 18 days. Sick leave is 10 days.",
            "answer": "Annual leave is 18 days, sick leave is 10 days, and vacation is 5 days.",
            "category": "Leave Policy"
        },
        {
            "id": "Q005",
            "question": "What is the WFH policy?",
            "context": "Employees can work from home 2 days per week with manager approval.",
            "answer": "Work from home is allowed 2 days weekly. You can work from home whenever needed.",
            "category": "Work Policies"
        },
        # Unsupported/Contradicting
        {
            "id": "Q006",
            "question": "What is the annual leave allowance?",
            "context": "Employees receive 18 annual leave days per year.",
            "answer": "Employees get 30 days of annual leave.",
            "category": "Leave Policy"
        },
        {
            "id": "Q007",
            "question": "What is the WFH policy?",
            "context": "Employees can work from home up to 2 days per week.",
            "answer": "Employees can work from home every day without restrictions.",
            "category": "Work Policies"
        },
        {
            "id": "Q008",
            "question": "What about benefits?",
            "context": "The company provides gym membership.",
            "answer": "We offer gym membership, dental insurance, pension plans, and stock options.",
            "category": "Benefits"
        },
        {
            "id": "Q009",
            "question": "What is the dress code?",
            "context": "Smart casual dress code applies in the office.",
            "answer": "Formal business wear is required at all times.",
            "category": "Office Policies"
        },
        {
            "id": "Q010",
            "question": "What is the salary increase?",
            "context": "Annual salary reviews are conducted in December.",
            "answer": "All employees receive a 10 percent annual salary increase.",
            "category": "Compensation"
        },
        # More faithful
        {
            "id": "Q011",
            "question": "What about sick leave?",
            "context": "Employees are entitled to 10 sick leave days per year.",
            "answer": "You get 10 days of sick leave annually.",
            "category": "Leave Policy"
        },
        {
            "id": "Q012",
            "question": "Performance appraisal process?",
            "context": "Annual appraisal consists of self-assessment, manager review, and feedback session.",
            "answer": "The appraisal includes self-assessment and manager feedback.",
            "category": "HR Procedures"
        },
        # More unsupported
        {
            "id": "Q013",
            "question": "International travel policy?",
            "context": "For international travel, employees must notify HR and get approval.",
            "answer": "All international travel is fully funded by the company.",
            "category": "Travel"
        },
        {
            "id": "Q014",
            "question": "Promotion criteria?",
            "context": "Minimum 2 years service with performance rating above average.",
            "answer": "Anyone can be promoted immediately regardless of performance.",
            "category": "Career Development"
        },
        {
            "id": "Q015",
            "question": "What about wellness?",
            "context": "The company provides gym membership and annual health check-ups.",
            "answer": "Wellness programs include gym access and health screening.",
            "category": "Benefits"
        },
    ]
    
    # Evaluate all test cases
    for test in test_cases:
        evaluator.evaluate(
            question_id=test["id"],
            question=test["question"],
            context=test["context"],
            answer=test["answer"],
            category=test["category"]
        )
    
    # Generate and display report
    evaluator.generate_report()
    
    # Save results
    evaluator.save_results()


if __name__ == "__main__":
    main()
