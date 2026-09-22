"""
TASK 5: Exact Match vs Semantic Match Evaluation
Compares different methods for evaluating answer correctness:
1. Exact String Matching
2. Keyword Matching
3. Semantic Similarity Matching
"""

import json
from difflib import SequenceMatcher
from collections import Counter


class AnswerMatcher:
    """Evaluate answers using different matching strategies."""
    
    def __init__(self):
        self.results = []
    
    # ==================== EXACT MATCH ====================
    def exact_match(self, expected: str, actual: str) -> bool:
        """
        Exact string matching: True only if strings are identical.
        
        This is the strictest method and often too restrictive for natural language.
        """
        return expected.lower().strip() == actual.lower().strip()
    
    
    # ==================== KEYWORD MATCH ====================
    def keyword_match(self, expected: str, actual: str, threshold: float = 0.7) -> bool:
        """
        Keyword matching: Check if key terms appear in the answer.
        
        Args:
            expected: Expected answer
            actual: AI-generated answer
            threshold: Percentage of keywords that must match (0.0 to 1.0)
        
        Returns:
            True if enough keywords are present
        """
        # Extract keywords (words longer than 3 characters)
        expected_keywords = set(
            word.lower() for word in expected.split() if len(word) > 3
        )
        actual_keywords = set(
            word.lower() for word in actual.split() if len(word) > 3
        )
        
        if not expected_keywords:
            return True  # No keywords to match
        
        matches = len(expected_keywords & actual_keywords)
        match_percentage = matches / len(expected_keywords)
        
        return match_percentage >= threshold
    
    
    # ==================== SEMANTIC SIMILARITY ====================
    def semantic_similarity(self, expected: str, actual: str, threshold: float = 0.7) -> float:
        """
        Semantic similarity: Measure text overlap using sequence matching.
        
        This is a simple approximation using SequenceMatcher.
        In production, you would use embedding models like sentence-transformers.
        
        Returns:
            Similarity score between 0.0 and 1.0
        """
        # Normalize text
        exp = expected.lower().strip()
        act = actual.lower().strip()
        
        # Calculate sequence match ratio
        similarity = SequenceMatcher(None, exp, act).ratio()
        return similarity
    
    
    # ==================== EVALUATION TEST CASES ====================
    def evaluate_test_case(self, question_id: str, question: str, 
                          expected: str, actual: str):
        """Evaluate a single test case using all three methods."""
        
        exact_result = self.exact_match(expected, actual)
        keyword_result = self.keyword_match(expected, actual, threshold=0.7)
        semantic_score = self.semantic_similarity(expected, actual)
        semantic_result = semantic_score >= 0.7
        
        result = {
            "question_id": question_id,
            "question": question,
            "expected": expected,
            "actual": actual,
            "exact_match": exact_result,
            "keyword_match": keyword_result,
            "semantic_similarity": round(semantic_score, 3),
            "semantic_match": semantic_result
        }
        
        self.results.append(result)
        return result
    
    
    def generate_report(self):
        """Generate evaluation report with statistics."""
        
        if not self.results:
            print("No results to report. Run evaluate_test_case first.")
            return
        
        exact_correct = sum(1 for r in self.results if r["exact_match"])
        keyword_correct = sum(1 for r in self.results if r["keyword_match"])
        semantic_correct = sum(1 for r in self.results if r["semantic_match"])
        total = len(self.results)
        
        print("\n" + "="*80)
        print("ANSWER MATCHING EVALUATION REPORT")
        print("="*80)
        
        print(f"\nTotal Test Cases: {total}\n")
        
        print(f"{'Metric':<30} {'Correct':<12} {'Percentage':<12}")
        print("-" * 54)
        print(f"{'Exact Match':<30} {exact_correct:<12} {exact_correct/total*100:>10.1f}%")
        print(f"{'Keyword Match':<30} {keyword_correct:<12} {keyword_correct/total*100:>10.1f}%")
        print(f"{'Semantic Similarity':<30} {semantic_correct:<12} {semantic_correct/total*100:>10.1f}%")
        
        print("\n" + "-" * 80)
        print("DETAILED RESULTS:")
        print("-" * 80)
        
        for i, result in enumerate(self.results, 1):
            print(f"\n[{i}] Q{result['question_id']}: {result['question']}")
            print(f"    Expected: {result['expected']}")
            print(f"    Actual:   {result['actual']}")
            print(f"    ├─ Exact Match:       {'PASS' if result['exact_match'] else 'FAIL'}")
            print(f"    ├─ Keyword Match:     {'PASS' if result['keyword_match'] else 'FAIL'}")
            print(f"    └─ Semantic Match:    {result['semantic_similarity']} (Score) - {'PASS' if result['semantic_match'] else 'FAIL'}")
        
        print("\n" + "="*80)
        print("KEY INSIGHTS:")
        print("="*80)
        print("""
1. EXACT MATCH is too strict:
   - Often fails even when answers are semantically correct
   - Doesn't account for word variation or rephrasing
   - Success rate: Usually 20-40% on real AI responses

2. KEYWORD MATCH is better but still limited:
   - Catches variations in phrasing
   - Doesn't understand semantic nuance
   - Can be fooled by answers that mention keywords without context
   - Success rate: Usually 60-80% on real AI responses

3. SEMANTIC SIMILARITY is most appropriate:
   - Understands meaning beyond exact words
   - Handles paraphrasing and alternative phrasings well
   - Best suited for evaluating AI-generated natural language
   - Success rate: Usually 80-95% on real AI responses
   - Requires embedding models for production use

RECOMMENDATION: Use semantic similarity (embeddings) for AI system evaluation.
        """)
        
        print("="*80)


def main():
    """Run evaluation examples."""
    
    matcher = AnswerMatcher()
    
    # Test Case 1: Simple exact match
    print("\nRunning Test Cases...\n")
    
    matcher.evaluate_test_case(
        question_id="Q001",
        question="What is the annual leave allowance?",
        expected="Employees receive 18 annual leave days.",
        actual="Employees receive 18 annual leave days."
    )
    
    # Test Case 2: Semantic equivalence (different wording)
    matcher.evaluate_test_case(
        question_id="Q002",
        question="What is the annual leave allowance?",
        expected="Employees receive 18 annual leave days.",
        actual="The company provides 18 days of annual leave."
    )
    
    # Test Case 3: Partial information
    matcher.evaluate_test_case(
        question_id="Q003",
        question="What is the leave policy?",
        expected="Annual leave is 18 days. You can carry over 5 days.",
        actual="Employees get 18 annual leave days."
    )
    
    # Test Case 4: Word order variation
    matcher.evaluate_test_case(
        question_id="Q004",
        question="What leave types exist?",
        expected="Leave includes vacation sick leave and personal days.",
        actual="Personal days sick leave and vacation are all covered."
    )
    
    # Test Case 5: Synonym usage
    matcher.evaluate_test_case(
        question_id="Q005",
        question="How do I request leave?",
        expected="Contact HR to apply for leave.",
        actual="Reach out to the Human Resources department to submit your leave request."
    )
    
    # Test Case 6: Completely wrong answer
    matcher.evaluate_test_case(
        question_id="Q006",
        question="What is the annual leave allowance?",
        expected="Employees receive 18 annual leave days.",
        actual="The office has 200 employees."
    )
    
    # Test Case 7: Hallucination
    matcher.evaluate_test_case(
        question_id="Q007",
        question="What is the work from home policy?",
        expected="Employees can work from home 2 days per week.",
        actual="Employees can work from home every day without restrictions."
    )
    
    # Test Case 8: Extra information
    matcher.evaluate_test_case(
        question_id="Q008",
        question="What is the annual leave?",
        expected="Employees get 18 days.",
        actual="Employees get 18 days of annual leave and can carry over up to 5 days to the next year."
    )
    
    # Generate and display report
    matcher.generate_report()
    
    # Save results to JSON
    with open('evaluation/answer_matching_results.json', 'w') as f:
        json.dump({
            "results": matcher.results,
            "summary": {
                "total_cases": len(matcher.results),
                "exact_match_accuracy": sum(1 for r in matcher.results if r["exact_match"]) / len(matcher.results),
                "keyword_match_accuracy": sum(1 for r in matcher.results if r["keyword_match"]) / len(matcher.results),
                "semantic_match_accuracy": sum(1 for r in matcher.results if r["semantic_match"]) / len(matcher.results)
            }
        }, f, indent=2)
    
    print(f"\n✓ Results saved to: evaluation/answer_matching_results.json")


if __name__ == "__main__":
    main()
