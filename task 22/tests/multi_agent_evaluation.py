"""
Multi-Agent System Evaluation
Comprehensive testing framework with 20+ test cases.
"""

import json
from typing import Dict, Any, List
from workflows.conditional_workflow import TaskRouter, TaskType


class MultiAgentEvaluation:
    """
    Evaluation framework for multi-agent system routing accuracy.
    
    Tests include:
    - Simple tasks
    - Research tasks
    - Calculation tasks
    - Writing tasks
    - Multi-step tasks
    - Invalid tasks
    - Failed tool tasks
    - Approval tasks
    """
    
    def __init__(self):
        """Initialize evaluation."""
        self.router = TaskRouter()
        self.test_results = []
        self.correct_count = 0
        self.total_tests = 0
    
    def create_test_cases(self) -> List[Dict[str, Any]]:
        """Create 20+ test cases."""
        return [
            # Category: Research Tasks (5 cases)
            {
                "id": 1,
                "question": "What is the leave policy?",
                "expected_agent": "research",
                "category": "Research"
            },
            {
                "id": 2,
                "question": "Find the annual leave entitlement",
                "expected_agent": "research",
                "category": "Research"
            },
            {
                "id": 3,
                "question": "Search for company handbook information",
                "expected_agent": "research",
                "category": "Research"
            },
            {
                "id": 4,
                "question": "What does the policy say about sick leave?",
                "expected_agent": "research",
                "category": "Research"
            },
            {
                "id": 5,
                "question": "Look up the leave request procedure",
                "expected_agent": "research",
                "category": "Research"
            },
            
            # Category: Calculation Tasks (5 cases)
            {
                "id": 6,
                "question": "Calculate 25 × 4",
                "expected_agent": "calculator",
                "category": "Calculation"
            },
            {
                "id": 7,
                "question": "What is 250 * 8?",
                "expected_agent": "calculator",
                "category": "Calculation"
            },
            {
                "id": 8,
                "question": "Compute 100 - 35",
                "expected_agent": "calculator",
                "category": "Calculation"
            },
            {
                "id": 9,
                "question": "Calculate percentage: 7 out of 18",
                "expected_agent": "calculator",
                "category": "Calculation"
            },
            {
                "id": 10,
                "question": "What is 1000 / 10?",
                "expected_agent": "calculator",
                "category": "Calculation"
            },
            
            # Category: Writing Tasks (3 cases)
            {
                "id": 11,
                "question": "Summarize the leave policy",
                "expected_agent": "writing",
                "category": "Writing"
            },
            {
                "id": 12,
                "question": "Write a report about leave usage",
                "expected_agent": "writing",
                "category": "Writing"
            },
            {
                "id": 13,
                "question": "Create a summary document",
                "expected_agent": "writing",
                "category": "Writing"
            },
            
            # Category: Complex/Multi-Step Tasks (5 cases)
            {
                "id": 14,
                "question": "Find the leave policy and calculate remaining days",
                "expected_agent": "complex",
                "category": "Complex"
            },
            {
                "id": 15,
                "question": "Research the policy, calculate 18-7, and write a summary",
                "expected_agent": "complex",
                "category": "Complex"
            },
            {
                "id": 16,
                "question": "Search for employee data, compute salary, and generate report",
                "expected_agent": "complex",
                "category": "Complex"
            },
            {
                "id": 17,
                "question": "Find the policy, determine eligibility, calculate benefit, and explain",
                "expected_agent": "complex",
                "category": "Complex"
            },
            {
                "id": 18,
                "question": "Research standards, calculate metrics, and prepare documentation",
                "expected_agent": "complex",
                "category": "Complex"
            },
            
            # Category: Edge Cases (3 cases)
            {
                "id": 19,
                "question": "xyz abc def",
                "expected_agent": "unknown",
                "category": "Edge Case"
            },
            {
                "id": 20,
                "question": "",
                "expected_agent": "unknown",
                "category": "Edge Case"
            },
            {
                "id": 21,
                "question": "12345 @#$%",
                "expected_agent": "unknown",
                "category": "Edge Case"
            }
        ]
    
    def run_evaluation(self) -> Dict[str, Any]:
        """Run the complete evaluation."""
        print(f"\n{'='*70}")
        print(f"MULTI-AGENT SYSTEM EVALUATION")
        print(f"{'='*70}\n")
        
        test_cases = self.create_test_cases()
        
        for test_case in test_cases:
            self._run_test_case(test_case)
        
        # Calculate accuracy
        accuracy = (self.correct_count / self.total_tests * 100) if self.total_tests > 0 else 0
        
        results_summary = {
            "total_tests": self.total_tests,
            "correct": self.correct_count,
            "incorrect": self.total_tests - self.correct_count,
            "accuracy": f"{accuracy:.1f}%",
            "test_results": self.test_results
        }
        
        return results_summary
    
    def _run_test_case(self, test_case: Dict[str, Any]):
        """Run a single test case."""
        self.total_tests += 1
        test_id = test_case['id']
        question = test_case['question']
        expected = test_case['expected_agent']
        category = test_case['category']
        
        # Route the task
        routing_result = self.router.route_task(question) if question else {"task_type": "unknown"}
        actual = routing_result.get('task_type', 'unknown')
        
        # Check if correct
        is_correct = actual == expected
        
        if is_correct:
            self.correct_count += 1
        
        result = {
            "test_id": test_id,
            "category": category,
            "question": question[:50] + "..." if len(question) > 50 else question,
            "expected": expected,
            "actual": actual,
            "correct": is_correct,
            "status": "✓ PASS" if is_correct else "✗ FAIL"
        }
        
        self.test_results.append(result)
    
    def print_evaluation_results(self, results: Dict[str, Any]):
        """Print evaluation results."""
        print(f"\n{'='*70}")
        print(f"EVALUATION RESULTS")
        print(f"{'='*70}\n")
        
        print(f"Total Tests: {results['total_tests']}")
        print(f"Correct: {results['correct']}")
        print(f"Incorrect: {results['incorrect']}")
        print(f"Agent Routing Accuracy: {results['accuracy']}\n")
        
        print(f"{'ID':<4} {'Category':<15} {'Expected':<12} {'Actual':<12} {'Status':<8}")
        print("-" * 70)
        
        for test in results['test_results']:
            print(f"{test['test_id']:<4} {test['category']:<15} {test['expected']:<12} "
                  f"{test['actual']:<12} {test['status']:<8}")
        
        print(f"\n{'='*70}\n")
    
    def print_detailed_report(self):
        """Print detailed evaluation report."""
        print(f"\n{'='*70}")
        print(f"DETAILED EVALUATION REPORT")
        print(f"{'='*70}\n")
        
        categories = {}
        
        for result in self.test_results:
            category = result['category']
            if category not in categories:
                categories[category] = {"total": 0, "correct": 0}
            
            categories[category]['total'] += 1
            if result['correct']:
                categories[category]['correct'] += 1
        
        print("Accuracy by Category:\n")
        
        for category, stats in sorted(categories.items()):
            accuracy = (stats['correct'] / stats['total'] * 100) if stats['total'] > 0 else 0
            print(f"  {category:<20} {stats['correct']}/{stats['total']:<3} ({accuracy:.1f}%)")
        
        print(f"\n{'='*70}\n")


def run_evaluation():
    """Run the complete evaluation."""
    evaluator = MultiAgentEvaluation()
    
    results = evaluator.run_evaluation()
    
    # Redirect print to catch output
    import io
    import sys
    
    # Print results
    evaluator.print_evaluation_results(results)
    evaluator.print_detailed_report()
    
    return results


if __name__ == "__main__":
    results = run_evaluation()
    
    # Save results to file
    with open("evaluation_results.json", "w") as f:
        json.dump(results, f, indent=2)
    
    print(f"Evaluation results saved to evaluation_results.json")
