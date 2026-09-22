"""
TASK 13: LLM-as-a-Judge Implementation
Uses an LLM to evaluate quality of AI-generated answers across multiple dimensions.

Judge Model evaluates:
1. Relevance (1-5): Does it address the question?
2. Faithfulness (1-5): Is it supported by context?
3. Completeness (1-5): Does it cover all aspects?
4. Clarity (1-5): Is it well-written?

Final Score = Average of all dimensions
"""

import json
from typing import List, Dict
import random


class LLMJudge:
    """Simulates an LLM judge for answer quality evaluation."""
    
    def __init__(self):
        self.judgments = []
    
    @staticmethod
    def judge_answer(question: str, ai_answer: str, reference_answer: str,
                     context: str = "") -> dict:
        """
        LLM Judge evaluates an answer across multiple dimensions.
        
        This is a simulated judge (uses heuristics).
        In production, use actual LLM API (OpenAI, Anthropic, etc.)
        """
        
        # Relevance: Does the answer address the question?
        answer_lower = ai_answer.lower()
        question_lower = question.lower()
        
        # Extract key terms from question
        question_terms = set(
            word.lower() for word in question.split()
            if len(word) > 3 and word.isalpha()
        )
        answer_terms = set(
            word.lower() for word in ai_answer.split()
            if len(word) > 3 and word.isalpha()
        )
        
        term_overlap = len(question_terms & answer_terms) / len(question_terms) if question_terms else 0
        relevance_score = min(5, int(term_overlap * 5 + 1))
        
        # Faithfulness: Is it supported by context?
        if context:
            context_terms = set(
                word.lower() for word in context.split()
                if len(word) > 3 and word.isalpha()
            )
            faithfulness = len(answer_terms & context_terms) / len(answer_terms) if answer_terms else 0
            faithfulness_score = min(5, int(faithfulness * 5 + 1))
        else:
            faithfulness_score = 3  # Neutral if no context
        
        # Completeness: Compare length and detail level to reference
        ref_length = len(reference_answer.split())
        answer_length = len(ai_answer.split())
        
        length_ratio = min(1.0, answer_length / ref_length) if ref_length > 0 else 1.0
        completeness_score = min(5, int(length_ratio * 5 + 1))
        
        # Clarity: Assess based on punctuation and structure
        sentences = ai_answer.count('.')
        words = len(ai_answer.split())
        avg_sentence_length = words / sentences if sentences > 0 else words
        
        # Ideal sentence length is 15-20 words
        if 10 <= avg_sentence_length <= 25:
            clarity_score = 5
        elif 8 <= avg_sentence_length <= 30:
            clarity_score = 4
        elif 5 <= avg_sentence_length <= 40:
            clarity_score = 3
        elif 3 <= avg_sentence_length <= 50:
            clarity_score = 2
        else:
            clarity_score = 1
        
        # Calculate overall score
        overall_score = (relevance_score + faithfulness_score + completeness_score + clarity_score) / 4
        
        return {
            "relevance": relevance_score,
            "faithfulness": faithfulness_score,
            "completeness": completeness_score,
            "clarity": clarity_score,
            "overall": round(overall_score, 2),
            "breakdown": {
                "relevance_reason": f"Question terms found in answer: {int(term_overlap*100)}%",
                "faithfulness_reason": f"Answer supported by context: {int(len(answer_terms & (set(word.lower() for word in context.split() if len(word) > 3 and word.isalpha()) if context else set()))/len(answer_terms)*100) if answer_terms else 0}%",
                "completeness_reason": f"Answer length vs reference: {int(length_ratio*100)}%",
                "clarity_reason": f"Avg sentence length: {avg_sentence_length:.1f} words"
            }
        }
    
    
    def evaluate(self, question_id: str, question: str, ai_answer: str,
                reference_answer: str, context: str = "", category: str = "General") -> dict:
        """Evaluate an answer using the judge and store results."""
        
        judgment = self.judge_answer(question, ai_answer, reference_answer, context)
        
        result = {
            "question_id": question_id,
            "question": question,
            "ai_answer": ai_answer,
            "reference_answer": reference_answer,
            "context": context if context else "N/A",
            "category": category,
            "relevance_score": judgment["relevance"],
            "faithfulness_score": judgment["faithfulness"],
            "completeness_score": judgment["completeness"],
            "clarity_score": judgment["clarity"],
            "overall_score": judgment["overall"],
            "evaluation_notes": judgment["breakdown"]
        }
        
        self.judgments.append(result)
        return result
    
    
    def generate_report(self):
        """Generate judge evaluation report."""
        
        if not self.judgments:
            print("No judgments to report.")
            return
        
        total = len(self.judgments)
        
        # Calculate averages
        avg_relevance = sum(j["relevance_score"] for j in self.judgments) / total
        avg_faithfulness = sum(j["faithfulness_score"] for j in self.judgments) / total
        avg_completeness = sum(j["completeness_score"] for j in self.judgments) / total
        avg_clarity = sum(j["clarity_score"] for j in self.judgments) / total
        avg_overall = sum(j["overall_score"] for j in self.judgments) / total
        
        print("\n" + "="*100)
        print("LLM JUDGE EVALUATION REPORT")
        print("="*100)
        
        print(f"\nTotal Evaluations: {total}\n")
        
        # Summary scores
        print(f"{'Dimension':<25} {'Score':<10} {'Assessment':<50}")
        print("-" * 85)
        print(f"{'Relevance':<25} {avg_relevance:<10.2f} {'How well does answer address question?':<50}")
        print(f"{'Faithfulness':<25} {avg_faithfulness:<10.2f} {'Is answer supported by context?':<50}")
        print(f"{'Completeness':<25} {avg_completeness:<10.2f} {'Does answer cover all aspects?':<50}")
        print(f"{'Clarity':<25} {avg_clarity:<10.2f} {'Is answer well-written?':<50}")
        print(f"{'OVERALL SCORE':<25} {avg_overall:<10.2f} {'Average of all dimensions':<50}")
        
        # Score interpretation
        if avg_overall >= 4.5:
            interpretation = "EXCELLENT - System performing at high level"
        elif avg_overall >= 4.0:
            interpretation = "GOOD - System performing well"
        elif avg_overall >= 3.0:
            interpretation = "FAIR - System has room for improvement"
        elif avg_overall >= 2.0:
            interpretation = "POOR - System needs significant improvement"
        else:
            interpretation = "CRITICAL - System requires immediate attention"
        
        print(f"\n{'Overall Assessment:':<40} {interpretation}")
        
        # Category breakdown
        categories = {}
        for j in self.judgments:
            cat = j["category"]
            if cat not in categories:
                categories[cat] = {
                    "count": 0,
                    "score_sum": 0,
                    "relevance_sum": 0,
                    "faithfulness_sum": 0
                }
            categories[cat]["count"] += 1
            categories[cat]["score_sum"] += j["overall_score"]
            categories[cat]["relevance_sum"] += j["relevance_score"]
            categories[cat]["faithfulness_sum"] += j["faithfulness_score"]
        
        if len(categories) > 1:
            print(f"\n{'SCORES BY CATEGORY':<100}")
            print("-" * 85)
            print(f"{'Category':<20} {'Count':<10} {'Overall':<12} {'Relevance':<12} {'Faithfulness':<12}")
            print("-" * 85)
            for cat, stats in sorted(categories.items()):
                avg_cat_score = stats["score_sum"] / stats["count"] if stats["count"] > 0 else 0
                avg_rel = stats["relevance_sum"] / stats["count"]
                avg_faith = stats["faithfulness_sum"] / stats["count"]
                print(f"{cat:<20} {stats['count']:<10} {avg_cat_score:>10.2f} {avg_rel:>12.2f} {avg_faith:>12.2f}")
        
        # Detailed judgments
        print(f"\n{'DETAILED JUDGMENTS':<100}")
        print("="*100)
        
        for i, judgment in enumerate(self.judgments, 1):
            print(f"\n[{i:2d}] Q{judgment['question_id']}: {judgment['question'][:60]}")
            print(f"      AI Answer: {judgment['ai_answer'][:80]}")
            print(f"      Reference: {judgment['reference_answer'][:80]}")
            print(f"      Scores: Relevance={judgment['relevance_score']}/5, "
                  f"Faithfulness={judgment['faithfulness_score']}/5, "
                  f"Completeness={judgment['completeness_score']}/5, "
                  f"Clarity={judgment['clarity_score']}/5")
            print(f"      Overall: {judgment['overall_score']}/5.0")
        
        print("\n" + "="*100)
        print("JUDGE INSIGHTS")
        print("="*100)
        print(f"""
1. Overall Quality Score: {avg_overall:.2f}/5.0
   - This represents the judge's assessment of answer quality
   - Baseline: 3.0 is average, 4.0+ is good
   
2. Dimension Analysis:
   - Relevance ({avg_relevance:.2f}): How on-topic are the answers?
   - Faithfulness ({avg_faithfulness:.2f}): How supported by documents?
   - Completeness ({avg_completeness:.2f}): How thorough are the answers?
   - Clarity ({avg_clarity:.2f}): How well-written?
   
3. Lowest Performing Dimension:
   - Focus improvement efforts here
   
4. Judge Limitations:
   - This judge uses heuristics, not true LLM evaluation
   - In production, use actual LLM for more nuanced judgment
   - Consider multiple judges to avoid bias
   - Judge should not be your only evaluation metric
   
5. Recommended Actions:
   - Address lowest dimension first
   - Analyze failure cases for patterns
   - Consider retrieval vs. generation issues separately
   - Monitor judge agreement with human evaluators
        """)
        print("="*100)
    
    
    def save_results(self, filepath: str = "evaluation/llm_judge_results.json"):
        """Save judge results to JSON."""
        data = {
            "judgments": self.judgments,
            "summary": {
                "total": len(self.judgments),
                "average_relevance": sum(j["relevance_score"] for j in self.judgments) / len(self.judgments) if self.judgments else 0,
                "average_faithfulness": sum(j["faithfulness_score"] for j in self.judgments) / len(self.judgments) if self.judgments else 0,
                "average_completeness": sum(j["completeness_score"] for j in self.judgments) / len(self.judgments) if self.judgments else 0,
                "average_clarity": sum(j["clarity_score"] for j in self.judgments) / len(self.judgments) if self.judgments else 0,
                "average_overall": sum(j["overall_score"] for j in self.judgments) / len(self.judgments) if self.judgments else 0
            }
        }
        
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2)
        
        print(f"\n✓ Judge results saved to: {filepath}")


def main():
    """Run LLM judge evaluation."""
    
    judge = LLMJudge()
    
    print("Running LLM Judge Evaluation...\n")
    
    # Test cases
    test_cases = [
        {
            "id": "Q001",
            "question": "What is the annual leave allowance?",
            "ai_answer": "Employees receive 18 annual leave days per year.",
            "reference_answer": "18 annual leave days",
            "context": "Employees are entitled to 18 annual leave days annually.",
            "category": "Leave Policy"
        },
        {
            "id": "Q002",
            "question": "How do employees apply for leave?",
            "ai_answer": "Submit request through HR portal at least 2 weeks in advance.",
            "reference_answer": "Apply through HR portal with 2 weeks notice",
            "context": "Leave requests must be submitted through HR portal minimum 2 weeks before the leave date.",
            "category": "Leave Policy"
        },
        {
            "id": "Q003",
            "question": "What is the work-from-home policy?",
            "ai_answer": "Can work from home 2 days per week.",
            "reference_answer": "2 days per week from home",
            "context": "Employees are permitted to work from home up to 2 days per week.",
            "category": "Work Policies"
        },
        {
            "id": "Q004",
            "question": "What are the benefits?",
            "ai_answer": "The company offers gym membership, health insurance, and dental coverage.",
            "reference_answer": "Gym membership and health benefits",
            "context": "Benefits include gym membership and annual health check-ups.",
            "category": "Benefits"
        },
        {
            "id": "Q005",
            "question": "What is the maternity leave policy?",
            "ai_answer": "Maternity leave is 120 days.",
            "reference_answer": "120 days maternity leave for female employees",
            "context": "Female employees are entitled to 120 days of maternity leave.",
            "category": "Leave Policy"
        },
        {
            "id": "Q006",
            "question": "What are the office hours?",
            "ai_answer": "Office hours",
            "reference_answer": "9 AM to 5 PM Monday to Friday",
            "context": "Office operating hours are 9 AM to 5 PM, Monday through Friday.",
            "category": "Office Policies"
        },
        {
            "id": "Q007",
            "question": "What is the sick leave policy?",
            "ai_answer": "10 days per year with doctor's note for absences over 3 days.",
            "reference_answer": "10 sick leave days, medical cert required for 3+ days",
            "context": "Employees receive 10 sick leave days yearly. Medical certificate required for absences exceeding 3 consecutive days.",
            "category": "Leave Policy"
        },
        {
            "id": "Q008",
            "question": "How is performance evaluated?",
            "ai_answer": "Annual appraisal done in December.",
            "reference_answer": "Performance review conducted annually in December",
            "context": "Annual performance appraisals are conducted in December.",
            "category": "HR Procedures"
        },
        {
            "id": "Q009",
            "question": "What about overtime compensation?",
            "ai_answer": "Overtime paid at regular rate.",
            "reference_answer": "Overtime at 1.5 times regular rate",
            "context": "Overtime is compensated at 1.5 times the employee's regular hourly rate.",
            "category": "Compensation"
        },
        {
            "id": "Q010",
            "question": "What dress code applies?",
            "ai_answer": "Smart casual dress code in office.",
            "reference_answer": "Smart casual attire required",
            "context": "Smart casual dress code applies in the office.",
            "category": "Office Policies"
        },
    ]
    
    # Evaluate all test cases
    for test in test_cases:
        judge.evaluate(
            question_id=test["id"],
            question=test["question"],
            ai_answer=test["ai_answer"],
            reference_answer=test["reference_answer"],
            context=test["context"],
            category=test["category"]
        )
    
    # Generate and display report
    judge.generate_report()
    
    # Save results
    judge.save_results()


if __name__ == "__main__":
    main()
