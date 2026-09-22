"""
TASK 6: Answer Relevance Evaluation
Evaluates whether answers are relevant to the questions asked.

Relevance Score:
0 = Not Relevant (completely off-topic)
1 = Partially Relevant (addresses some aspects)
2 = Relevant (fully addresses the question)
"""

import json
from typing import List, Tuple
from difflib import SequenceMatcher


class RelevanceEvaluator:
    """Evaluate answer relevance to questions."""
    
    def __init__(self):
        self.evaluations = []
    
    # ==================== RELEVANCE SCORING ====================
    def calculate_relevance(self, question: str, answer: str) -> int:
        """
        Calculate relevance score (0-2) for an answer to a question.
        
        Scoring Logic:
        - Score 2: Answer directly addresses the question
        - Score 1: Answer partially addresses the question
        - Score 0: Answer is completely off-topic
        
        Args:
            question: The question asked
            answer: The answer provided
        
        Returns:
            Relevance score: 0, 1, or 2
        """
        
        # Extract key terms from question (words > 3 chars)
        question_terms = set(
            word.lower() for word in question.split()
            if len(word) > 3 and word.isalpha()
        )
        
        # Extract key terms from answer
        answer_terms = set(
            word.lower() for word in answer.split()
            if len(word) > 3 and word.isalpha()
        )
        
        if not question_terms:
            return 2  # No keywords to evaluate
        
        # Calculate term overlap
        overlap = len(question_terms & answer_terms)
        overlap_percentage = overlap / len(question_terms)
        
        # Calculate semantic similarity
        similarity = SequenceMatcher(None, 
                                   question.lower(), 
                                   answer.lower()).ratio()
        
        # Scoring decision tree
        if similarity > 0.4 or overlap_percentage > 0.5:
            # Good relevance
            if similarity > 0.5 or overlap_percentage > 0.7:
                return 2  # Highly relevant
            else:
                return 1  # Partially relevant
        else:
            return 0  # Not relevant
    
    
    # ==================== EVALUATION ====================
    def evaluate(self, question_id: str, question: str, answer: str,
                category: str = "General") -> dict:
        """
        Evaluate a single question-answer pair for relevance.
        
        Args:
            question_id: ID of the question
            question: The question text
            answer: The answer text
            category: Category of the question
        
        Returns:
            Evaluation result dictionary
        """
        
        relevance_score = self.calculate_relevance(question, answer)
        
        # Map score to label
        if relevance_score == 0:
            relevance_label = "Not Relevant"
        elif relevance_score == 1:
            relevance_label = "Partially Relevant"
        else:
            relevance_label = "Relevant"
        
        result = {
            "question_id": question_id,
            "question": question,
            "answer": answer,
            "category": category,
            "relevance_score": relevance_score,
            "relevance_label": relevance_label
        }
        
        self.evaluations.append(result)
        return result
    
    
    # ==================== REPORTING ====================
    def generate_report(self):
        """Generate comprehensive relevance evaluation report."""
        
        if not self.evaluations:
            print("No evaluations to report.")
            return
        
        # Calculate statistics
        total = len(self.evaluations)
        not_relevant = sum(1 for e in self.evaluations if e["relevance_score"] == 0)
        partially_relevant = sum(1 for e in self.evaluations if e["relevance_score"] == 1)
        relevant = sum(1 for e in self.evaluations if e["relevance_score"] == 2)
        
        # Average score (0-2 scale)
        avg_score = sum(e["relevance_score"] for e in self.evaluations) / total
        
        print("\n" + "="*100)
        print("ANSWER RELEVANCE EVALUATION REPORT")
        print("="*100)
        
        print(f"\nTotal Evaluations: {total}\n")
        
        # Summary statistics
        print(f"{'Relevance Level':<25} {'Count':<10} {'Percentage':<12} {'Score':<8}")
        print("-" * 75)
        print(f"{'Relevant':<25} {relevant:<10} {relevant/total*100:>10.1f}% {'2/2':<8}")
        print(f"{'Partially Relevant':<25} {partially_relevant:<10} {partially_relevant/total*100:>10.1f}% {'1/2':<8}")
        print(f"{'Not Relevant':<25} {not_relevant:<10} {not_relevant/total*100:>10.1f}% {'0/2':<8}")
        
        print(f"\n{'Average Relevance Score:':<40} {avg_score:.2f}/2.0 ({avg_score/2*100:.1f}%)")
        
        # Break down by category if available
        categories = {}
        for e in self.evaluations:
            cat = e.get("category", "General")
            if cat not in categories:
                categories[cat] = {"total": 0, "relevant": 0, "score_sum": 0}
            categories[cat]["total"] += 1
            categories[cat]["score_sum"] += e["relevance_score"]
            if e["relevance_score"] == 2:
                categories[cat]["relevant"] += 1
        
        if len(categories) > 1:
            print(f"\n{'BREAKDOWN BY CATEGORY':<100}")
            print("-" * 75)
            print(f"{'Category':<25} {'Total':<10} {'Relevant':<12} {'Avg Score':<12}")
            print("-" * 75)
            for cat, stats in sorted(categories.items()):
                avg_cat_score = stats["score_sum"] / stats["total"] if stats["total"] > 0 else 0
                print(f"{cat:<25} {stats['total']:<10} {stats['relevant']:<12} {avg_cat_score:>10.2f}")
        
        # Detailed results
        print(f"\n{'DETAILED RESULTS':<100}")
        print("="*100)
        
        for i, eval_result in enumerate(self.evaluations, 1):
            score_label = "PASS" if eval_result["relevance_score"] == 2 else ("PARTIAL" if eval_result["relevance_score"] == 1 else "FAIL")
            print(f"\n[{i:2d}] {score_label} Q{eval_result['question_id']}: {eval_result['question'][:70]}")
            print(f"      Answer: {eval_result['answer'][:80]}")
            print(f"      Score: {eval_result['relevance_score']}/2 - {eval_result['relevance_label']}")
        
        print("\n" + "="*100)
        print("KEY INSIGHTS")
        print("="*100)
        print(f"""
1. Relevance is fundamental to AI system quality
   - Score {relevant} out of {total} answers were fully relevant
   - {not_relevant} answers were completely off-topic
   
2. Relevance failures indicate:
   - Poor question understanding by the AI
   - Insufficient retrieval context
   - Semantic mismatch between question and documents
   
3. Action items for improvement:
   - Review {not_relevant} non-relevant answers
   - Improve document indexing and retrieval
   - Fine-tune question understanding
   - Add better quality filters
   
4. Relevance benchmarks:
   - < 50% relevant: Critical issue, system needs major revision
   - 50-80% relevant: Room for improvement
   - 80-95% relevant: Good performance
   - 95%+ relevant: Excellent performance
   
Current Performance: {relevant/total*100:.1f}% relevant
        """)
        print("="*100)
    
    
    def save_results(self, filepath: str = "evaluation/relevance_results.json"):
        """Save evaluation results to JSON file."""
        data = {
            "evaluations": self.evaluations,
            "summary": {
                "total": len(self.evaluations),
                "relevant_count": sum(1 for e in self.evaluations if e["relevance_score"] == 2),
                "partially_relevant_count": sum(1 for e in self.evaluations if e["relevance_score"] == 1),
                "not_relevant_count": sum(1 for e in self.evaluations if e["relevance_score"] == 0),
                "average_score": sum(e["relevance_score"] for e in self.evaluations) / len(self.evaluations) if self.evaluations else 0,
                "percentage_relevant": (sum(1 for e in self.evaluations if e["relevance_score"] == 2) / len(self.evaluations) * 100) if self.evaluations else 0
            }
        }
        
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2)
        
        print(f"\n✓ Results saved to: {filepath}")


def main():
    """Run relevance evaluation on test cases."""
    
    evaluator = RelevanceEvaluator()
    
    print("Running Relevance Evaluation...\n")
    
    # Test Cases - Mixed relevance
    test_cases = [
        # Relevant answers
        {
            "id": "Q001",
            "question": "What is the annual leave allowance?",
            "answer": "Employees receive 18 annual leave days per year.",
            "category": "Leave Policy"
        },
        {
            "id": "Q002",
            "question": "How do I apply for leave?",
            "answer": "Submit a request through the HR portal at least 2 weeks in advance.",
            "category": "Leave Policy"
        },
        {
            "id": "Q003",
            "question": "What is the work-from-home policy?",
            "answer": "Employees can work from home up to 2 days per week.",
            "category": "Work Policies"
        },
        # Partially relevant answers
        {
            "id": "Q004",
            "question": "What is the annual leave allowance?",
            "answer": "The company provides 18 days of leave. Employees can also take sick leave.",
            "category": "Leave Policy"
        },
        {
            "id": "Q005",
            "question": "How many vacation days do we get?",
            "answer": "Employees receive 5 vacation days in addition to annual leave.",
            "category": "Leave Policy"
        },
        {
            "id": "Q006",
            "question": "What is the office dress code?",
            "answer": "Employees work from 9 AM to 5 PM and smart casual dress is required.",
            "category": "Office Policies"
        },
        # Not relevant answers
        {
            "id": "Q007",
            "question": "What is the annual leave allowance?",
            "answer": "The office has 200 employees and located in downtown area.",
            "category": "Leave Policy"
        },
        {
            "id": "Q008",
            "question": "How do I apply for leave?",
            "answer": "The company has a strong commitment to employee wellbeing.",
            "category": "Leave Policy"
        },
        {
            "id": "Q009",
            "question": "What is the work-from-home policy?",
            "answer": "Our CEO founded the company in 2015.",
            "category": "Work Policies"
        },
        {
            "id": "Q010",
            "question": "What benefits are included?",
            "answer": "Our office has excellent parking facilities.",
            "category": "Benefits"
        },
        # Additional relevant test cases
        {
            "id": "Q011",
            "question": "What is the maternity leave policy?",
            "answer": "Female employees are entitled to 120 days of maternity leave.",
            "category": "Leave Policy"
        },
        {
            "id": "Q012",
            "question": "How is performance appraisal done?",
            "answer": "Annual appraisal consists of self-assessment, manager review, and feedback.",
            "category": "HR Procedures"
        },
        {
            "id": "Q013",
            "question": "What are the sick leave benefits?",
            "answer": "Employees get 10 sick leave days per year.",
            "category": "Leave Policy"
        },
        {
            "id": "Q014",
            "question": "Can I work from home permanently?",
            "answer": "The work-from-home policy allows 2 days per week from home.",
            "category": "Work Policies"
        },
        {
            "id": "Q015",
            "question": "What is the bereavement leave policy?",
            "answer": "Employees can take 5 days of bereavement leave for immediate family.",
            "category": "Leave Policy"
        },
        {
            "id": "Q016",
            "question": "Are overtime hours paid?",
            "answer": "Overtime is compensated at 1.5 times the regular rate with manager approval.",
            "category": "Compensation"
        },
        {
            "id": "Q017",
            "question": "What wellness programs are available?",
            "answer": "The company provides gym membership and annual health check-ups.",
            "category": "Benefits"
        },
        {
            "id": "Q018",
            "question": "How do I request professional training?",
            "answer": "Submit a training request to your manager, get approval, and HR processes it.",
            "category": "Training"
        },
        {
            "id": "Q019",
            "question": "What is the promotion criteria?",
            "answer": "We are a growing tech company with innovative solutions.",
            "category": "Career Development"
        },
        {
            "id": "Q020",
            "question": "How many public holidays does the company observe?",
            "answer": "The company observes 12 public holidays with full pay.",
            "category": "Holidays"
        }
    ]
    
    # Evaluate all test cases
    for test in test_cases:
        evaluator.evaluate(
            question_id=test["id"],
            question=test["question"],
            answer=test["answer"],
            category=test["category"]
        )
    
    # Generate and display report
    evaluator.generate_report()
    
    # Save results
    evaluator.save_results()


if __name__ == "__main__":
    main()
