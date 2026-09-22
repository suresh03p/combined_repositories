"""
TASK 7-10: RAG Retrieval Evaluation
Comprehensive evaluation of document retrieval quality including:
- TASK 7: Retrieval Evaluation (which documents were retrieved)
- TASK 8: Precision@K (quality of retrieved results)
- TASK 9: Recall@K (coverage of relevant documents)
- TASK 10: Mean Reciprocal Rank (ranking quality)
"""

import json
from typing import List, Tuple, Dict
from dataclasses import dataclass, asdict


@dataclass
class RetrievalTest:
    """Represents a single retrieval test case."""
    question_id: str
    question: str
    expected_documents: List[str]  # Documents that should be retrieved
    retrieved_documents: List[str]  # Documents actually retrieved (in order)
    category: str = "General"


class RAGEvaluator:
    """Evaluate RAG retrieval quality using multiple metrics."""
    
    def __init__(self):
        self.evaluations = []
    
    # ==================== EVALUATION FUNCTIONS ====================
    
    @staticmethod
    def evaluate_retrieval(test: RetrievalTest) -> dict:
        """
        Evaluate retrieval quality for a single test case.
        
        Returns dictionary with:
        - Correct document retrieved (boolean)
        - Rank of first correct document
        - Retrieved documents (in order)
        """
        
        correct_docs = set(test.expected_documents)
        
        # Find rank of first correct document (1-indexed)
        first_correct_rank = None
        for i, doc in enumerate(test.retrieved_documents, 1):
            if doc in correct_docs:
                first_correct_rank = i
                break
        
        correct_retrieved = first_correct_rank is not None
        
        return {
            "correct_retrieved": correct_retrieved,
            "rank": first_correct_rank,
            "expected_docs": test.expected_documents,
            "retrieved_docs": test.retrieved_documents
        }
    
    
    @staticmethod
    def precision_at_k(correct_count: int, k: int) -> float:
        """
        Calculate Precision@K
        
        Precision@K = (Number of relevant items in top K) / K
        
        Example: If 3 out of 5 retrieved documents are relevant
        Precision@5 = 3/5 = 0.60
        """
        if k == 0:
            return 0.0
        return correct_count / k
    
    
    @staticmethod
    def recall_at_k(correct_count: int, total_relevant: int) -> float:
        """
        Calculate Recall@K
        
        Recall@K = (Number of relevant items retrieved) / Total relevant items
        
        Example: If 4 out of 5 relevant documents are retrieved
        Recall@5 = 4/5 = 0.80
        """
        if total_relevant == 0:
            return 0.0
        return correct_count / total_relevant
    
    
    @staticmethod
    def mean_reciprocal_rank(rank: int) -> float:
        """
        Calculate Mean Reciprocal Rank (MRR)
        
        MRR = 1 / (Rank of first relevant document)
        
        Example:
        - If relevant doc at rank 1: MRR = 1/1 = 1.0
        - If relevant doc at rank 3: MRR = 1/3 = 0.333
        - If relevant doc at rank 5: MRR = 1/5 = 0.2
        """
        if rank is None:
            return 0.0
        return 1.0 / rank
    
    
    def evaluate(self, test: RetrievalTest, top_k_values: List[int] = None):
        """
        Evaluate a single test case and calculate all metrics.
        
        Args:
            test: RetrievalTest case with question and documents
            top_k_values: Which K values to calculate (default: [1, 3, 5])
        """
        
        if top_k_values is None:
            top_k_values = [1, 3, 5]
        
        # Basic retrieval evaluation
        retrieval_result = self.evaluate_retrieval(test)
        
        # Count correct documents in retrieved set
        correct_docs = set(test.expected_documents)
        retrieved_docs = test.retrieved_documents
        
        # Calculate metrics for each K
        precision_results = {}
        recall_results = {}
        
        for k in top_k_values:
            # Count correct documents in top K
            top_k_docs = retrieved_docs[:k]
            correct_in_k = sum(1 for doc in top_k_docs if doc in correct_docs)
            
            # Calculate Precision@K and Recall@K
            precision_results[f"@{k}"] = self.precision_at_k(correct_in_k, k)
            recall_results[f"@{k}"] = self.recall_at_k(correct_in_k, len(correct_docs))
        
        # Calculate MRR
        mrr = self.mean_reciprocal_rank(retrieval_result["rank"])
        
        result = {
            "question_id": test.question_id,
            "question": test.question,
            "category": test.category,
            "expected_documents": test.expected_documents,
            "retrieved_documents": test.retrieved_documents,
            "correct_retrieved": retrieval_result["correct_retrieved"],
            "rank_of_correct": retrieval_result["rank"],
            "precision": precision_results,
            "recall": recall_results,
            "mrr": round(mrr, 3),
            "num_correct_docs": sum(1 for doc in retrieved_docs if doc in correct_docs),
            "total_expected_docs": len(correct_docs)
        }
        
        self.evaluations.append(result)
        return result
    
    
    def generate_report(self):
        """Generate comprehensive retrieval evaluation report."""
        
        if not self.evaluations:
            print("No evaluations to report.")
            return
        
        total = len(self.evaluations)
        
        # Calculate aggregate metrics
        correct_retrievals = sum(1 for e in self.evaluations if e["correct_retrieved"])
        avg_mrr = sum(e["mrr"] for e in self.evaluations) / total
        
        # Average precision and recall at different K values
        avg_precision_1 = sum(e["precision"]["@1"] for e in self.evaluations) / total
        avg_precision_3 = sum(e["precision"]["@3"] for e in self.evaluations) / total
        avg_precision_5 = sum(e["precision"]["@5"] for e in self.evaluations) / total
        
        avg_recall_1 = sum(e["recall"]["@1"] for e in self.evaluations) / total
        avg_recall_3 = sum(e["recall"]["@3"] for e in self.evaluations) / total
        avg_recall_5 = sum(e["recall"]["@5"] for e in self.evaluations) / total
        
        print("\n" + "="*100)
        print("RAG RETRIEVAL EVALUATION REPORT")
        print("="*100)
        
        print(f"\nTotal Test Cases: {total}")
        print(f"Correct Documents Retrieved: {correct_retrievals}/{total} ({correct_retrievals/total*100:.1f}%)\n")
        
        # Summary table
        print(f"{'Metric':<25} {'Value':<12} {'Interpretation':<50}")
        print("-" * 87)
        print(f"{'Average MRR':<25} {avg_mrr:<12.3f} {'Avg rank reward':<50}")
        print(f"{'Precision@1':<25} {avg_precision_1:<12.3f} {'% of top 1 relevant':<50}")
        print(f"{'Precision@3':<25} {avg_precision_3:<12.3f} {'% of top 3 relevant':<50}")
        print(f"{'Precision@5':<25} {avg_precision_5:<12.3f} {'% of top 5 relevant':<50}")
        print(f"{'Recall@1':<25} {avg_recall_1:<12.3f} {'% of docs in top 1':<50}")
        print(f"{'Recall@3':<25} {avg_recall_3:<12.3f} {'% of docs in top 3':<50}")
        print(f"{'Recall@5':<25} {avg_recall_5:<12.3f} {'% of docs in top 5':<50}")
        
        # Category breakdown
        categories = {}
        for e in self.evaluations:
            cat = e["category"]
            if cat not in categories:
                categories[cat] = {"count": 0, "correct": 0, "mrr_sum": 0}
            categories[cat]["count"] += 1
            if e["correct_retrieved"]:
                categories[cat]["correct"] += 1
            categories[cat]["mrr_sum"] += e["mrr"]
        
        if len(categories) > 1:
            print(f"\n{'BREAKDOWN BY CATEGORY':<100}")
            print("-" * 87)
            print(f"{'Category':<20} {'Total':<8} {'Correct':<10} {'Rate':<10} {'Avg MRR':<12}")
            print("-" * 87)
            for cat, stats in sorted(categories.items()):
                rate = stats["correct"] / stats["count"] * 100
                avg_mrr_cat = stats["mrr_sum"] / stats["count"]
                print(f"{cat:<20} {stats['count']:<8} {stats['correct']:<10} {rate:>8.1f}% {avg_mrr_cat:>10.3f}")
        
        # Detailed results
        print(f"\n{'DETAILED RETRIEVAL RESULTS':<100}")
        print("="*100)
        
        for i, eval_result in enumerate(self.evaluations, 1):
            status = "PASS" if eval_result["correct_retrieved"] else "FAIL"
            print(f"\n[{i:2d}] {status} Q{eval_result['question_id']}: {eval_result['question'][:60]}")
            print(f"      Expected: {', '.join(eval_result['expected_documents'])}")
            print(f"      Retrieved: {', '.join(eval_result['retrieved_documents'][:5])}")
            if eval_result["rank_of_correct"]:
                print(f"      [1] Correct doc at Rank: {eval_result['rank_of_correct']}")
            else:
                print(f"      [1] Correct doc at Rank: NOT FOUND")
            print(f"      [2] Precision@5: {eval_result['precision']['@5']:.2f}")
            print(f"      [3] Recall@5: {eval_result['recall']['@5']:.2f}")
            print(f"      [4] MRR: {eval_result['mrr']:.3f}")
        
        print("\n" + "="*100)
        print("RETRIEVAL QUALITY ANALYSIS")
        print("="*100)
        print(f"""
1. Retrieval Success Rate: {correct_retrievals/total*100:.1f}%
   - {correct_retrievals} test cases found the correct document
   - {total - correct_retrievals} test cases failed to retrieve the correct document
   
2. Ranking Quality (MRR): {avg_mrr:.3f}
   - 1.0 = Perfect (correct doc at rank 1)
   - 0.5 = Good (correct doc at rank 2 on average)
   - 0.2 = Poor (correct doc at rank 5 on average)
   - Current: {avg_mrr:.3f}
   
3. Precision@5: {avg_precision_5:.3f}
   - How many retrieved documents are relevant
   - Current: {avg_precision_5*100:.1f}% of top 5 are relevant
   
4. Recall@5: {avg_recall_5:.3f}
   - How many relevant documents were captured
   - Current: {avg_recall_5*100:.1f}% of all relevant docs in top 5
   
5. Improvement Opportunities:
   - Improve semantic search indexing
   - Fine-tune retrieval ranking
   - Add re-ranking layer
   - Enhance document chunking strategy
        """)
        print("="*100)
    
    
    def save_results(self, filepath: str = "evaluation/retrieval_results.json"):
        """Save evaluation results to JSON file."""
        data = {
            "evaluations": self.evaluations,
            "summary": {
                "total": len(self.evaluations),
                "correct_retrievals": sum(1 for e in self.evaluations if e["correct_retrieved"]),
                "success_rate": sum(1 for e in self.evaluations if e["correct_retrieved"]) / len(self.evaluations) if self.evaluations else 0,
                "average_mrr": sum(e["mrr"] for e in self.evaluations) / len(self.evaluations) if self.evaluations else 0,
                "avg_precision_1": sum(e["precision"]["@1"] for e in self.evaluations) / len(self.evaluations) if self.evaluations else 0,
                "avg_precision_5": sum(e["precision"]["@5"] for e in self.evaluations) / len(self.evaluations) if self.evaluations else 0,
                "avg_recall_5": sum(e["recall"]["@5"] for e in self.evaluations) / len(self.evaluations) if self.evaluations else 0
            }
        }
        
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2, default=str)
        
        print(f"\n✓ Results saved to: {filepath}")


def main():
    """Run RAG retrieval evaluation."""
    
    evaluator = RAGEvaluator()
    
    print("Running RAG Retrieval Evaluation...\n")
    
    # Test cases
    test_cases = [
        RetrievalTest(
            question_id="Q001",
            question="What is the annual leave allowance?",
            expected_documents=["leave_policy.pdf"],
            retrieved_documents=["leave_policy.pdf", "employee_handbook.pdf", "office_policy.pdf"],
            category="Leave Policy"
        ),
        RetrievalTest(
            question_id="Q002",
            question="How do I apply for leave?",
            expected_documents=["leave_policy.pdf"],
            retrieved_documents=["office_policy.pdf", "leave_policy.pdf", "hr_procedures.pdf"],
            category="Leave Policy"
        ),
        RetrievalTest(
            question_id="Q003",
            question="What is the work-from-home policy?",
            expected_documents=["wfh_policy.pdf"],
            retrieved_documents=["wfh_policy.pdf", "office_policy.pdf", "leave_policy.pdf"],
            category="Work Policies"
        ),
        RetrievalTest(
            question_id="Q004",
            question="What benefits do employees get?",
            expected_documents=["benefits_policy.pdf", "compensation_policy.pdf"],
            retrieved_documents=["benefits_policy.pdf", "office_policy.pdf", "compensation_policy.pdf", "leave_policy.pdf"],
            category="Benefits"
        ),
        RetrievalTest(
            question_id="Q005",
            question="What is the dress code?",
            expected_documents=["office_policy.pdf"],
            retrieved_documents=["training_policy.pdf", "code_of_conduct.pdf", "hr_procedures.pdf"],
            category="Office Policies"
        ),
        RetrievalTest(
            question_id="Q006",
            question="How is performance evaluated?",
            expected_documents=["hr_procedures.pdf"],
            retrieved_documents=["hr_procedures.pdf", "career_development.pdf", "leave_policy.pdf"],
            category="HR Procedures"
        ),
        RetrievalTest(
            question_id="Q007",
            question="What is the maternity leave policy?",
            expected_documents=["leave_policy.pdf"],
            retrieved_documents=["employee_handbook.pdf", "benefits_policy.pdf", "leave_policy.pdf"],
            category="Leave Policy"
        ),
        RetrievalTest(
            question_id="Q008",
            question="How do I request training?",
            expected_documents=["training_policy.pdf"],
            retrieved_documents=["training_policy.pdf", "career_development.pdf", "hr_procedures.pdf"],
            category="Training"
        ),
        RetrievalTest(
            question_id="Q009",
            question="What about sick leave?",
            expected_documents=["leave_policy.pdf"],
            retrieved_documents=["leave_policy.pdf", "benefits_policy.pdf", "office_policy.pdf"],
            category="Leave Policy"
        ),
        RetrievalTest(
            question_id="Q010",
            question="What is the overtime policy?",
            expected_documents=["compensation_policy.pdf"],
            retrieved_documents=["compensation_policy.pdf", "office_policy.pdf", "hr_procedures.pdf"],
            category="Compensation"
        ),
    ]
    
    # Evaluate all test cases
    for test in test_cases:
        evaluator.evaluate(test)
    
    # Generate and display report
    evaluator.generate_report()
    
    # Save results
    evaluator.save_results()


if __name__ == "__main__":
    main()
