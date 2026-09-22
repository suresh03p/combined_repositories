"""
TASK 19: AI Quality Score Builder
Combines multiple evaluation dimensions into a single quality score.

Weights:
- Answer Relevance: 30%
- Faithfulness: 30%
- Retrieval Quality: 20%
- Completeness: 10%
- Latency: 10%
"""

import json
from typing import Dict


class QualityScoreBuilder:
    """Build composite quality scores from individual metrics."""
    
    def __init__(self, weights: Dict[str, float] = None):
        """
        Initialize with metric weights (must sum to 1.0).
        
        Default weights:
        - Relevance: 30%
        - Faithfulness: 30%
        - Retrieval Quality: 20%
        - Completeness: 10%
        - Latency: 10%
        """
        
        self.weights = weights or {
            "relevance": 0.30,
            "faithfulness": 0.30,
            "retrieval_quality": 0.20,
            "completeness": 0.10,
            "latency": 0.10
        }
        
        # Validate weights sum to 1.0
        if abs(sum(self.weights.values()) - 1.0) > 0.001:
            raise ValueError("Weights must sum to 1.0")
        
        self.evaluations = []
    
    
    @staticmethod
    def normalize_score(score: float, max_score: float = 5.0, min_score: float = 0.0) -> float:
        """
        Normalize a score to 0-1 range.
        
        Args:
            score: Actual score
            max_score: Maximum possible score
            min_score: Minimum possible score
        
        Returns:
            Normalized score (0-1)
        """
        if max_score == min_score:
            return 1.0
        return max(0.0, min(1.0, (score - min_score) / (max_score - min_score)))
    
    
    @staticmethod
    def normalize_latency(latency_seconds: float, target_latency: float = 5.0) -> float:
        """
        Normalize latency (lower is better).
        
        Args:
            latency_seconds: Actual latency in seconds
            target_latency: Target latency (e.g., 5 seconds)
        
        Returns:
            Score where 1.0 is at/below target, 0.0 is 5x target
        """
        if latency_seconds <= target_latency:
            return 1.0
        ratio = latency_seconds / target_latency
        if ratio >= 5:
            return 0.0
        return 1.0 - ((ratio - 1) / 4)
    
    
    def calculate_quality_score(self, 
                               relevance: float,  # 0-5
                               faithfulness: float,  # 0-5
                               retrieval_quality: float,  # 0-1 (precision/recall)
                               completeness: float,  # 0-5
                               latency: float = 3.0  # seconds
                               ) -> Dict:
        """
        Calculate composite quality score.
        
        Args:
            relevance: Relevance score (0-5)
            faithfulness: Faithfulness score (0-5)
            retrieval_quality: Retrieval metric (0-1, e.g., MRR or precision)
            completeness: Completeness score (0-5)
            latency: Response time in seconds
        
        Returns:
            Dictionary with component and overall scores
        """
        
        # Normalize all scores to 0-1 range
        norm_relevance = self.normalize_score(relevance, max_score=5.0)
        norm_faithfulness = self.normalize_score(faithfulness, max_score=5.0)
        norm_retrieval = retrieval_quality  # Already 0-1
        norm_completeness = self.normalize_score(completeness, max_score=5.0)
        norm_latency = self.normalize_latency(latency, target_latency=5.0)
        
        # Apply weights
        weighted_score = (
            norm_relevance * self.weights["relevance"] +
            norm_faithfulness * self.weights["faithfulness"] +
            norm_retrieval * self.weights["retrieval_quality"] +
            norm_completeness * self.weights["completeness"] +
            norm_latency * self.weights["latency"]
        )
        
        # Scale to 0-100 for easier interpretation
        final_score = weighted_score * 100
        
        return {
            "normalized_scores": {
                "relevance": round(norm_relevance, 3),
                "faithfulness": round(norm_faithfulness, 3),
                "retrieval_quality": round(norm_retrieval, 3),
                "completeness": round(norm_completeness, 3),
                "latency": round(norm_latency, 3)
            },
            "weighted_scores": {
                "relevance": round(norm_relevance * self.weights["relevance"], 3),
                "faithfulness": round(norm_faithfulness * self.weights["faithfulness"], 3),
                "retrieval_quality": round(norm_retrieval * self.weights["retrieval_quality"], 3),
                "completeness": round(norm_completeness * self.weights["completeness"], 3),
                "latency": round(norm_latency * self.weights["latency"], 3)
            },
            "overall_score": round(final_score, 1),
            "grade": self._get_grade(final_score)
        }
    
    
    @staticmethod
    def _get_grade(score: float) -> str:
        """Convert score (0-100) to grade."""
        if score >= 90:
            return "A+"
        elif score >= 80:
            return "A"
        elif score >= 70:
            return "B"
        elif score >= 60:
            return "C"
        elif score >= 50:
            return "D"
        else:
            return "F"
    
    
    def evaluate(self, request_id: str, relevance: float, faithfulness: float,
                retrieval_quality: float, completeness: float, latency: float,
                category: str = "General") -> Dict:
        """Evaluate a single request and store results."""
        
        quality_calc = self.calculate_quality_score(
            relevance, faithfulness, retrieval_quality, completeness, latency
        )
        
        result = {
            "request_id": request_id,
            "category": category,
            "input_scores": {
                "relevance": relevance,
                "faithfulness": faithfulness,
                "retrieval_quality": retrieval_quality,
                "completeness": completeness,
                "latency": latency
            },
            **quality_calc
        }
        
        self.evaluations.append(result)
        return result
    
    
    def generate_report(self):
        """Generate quality score report."""
        
        if not self.evaluations:
            print("No evaluations to report.")
            return
        
        scores = [e["overall_score"] for e in self.evaluations]
        avg_score = sum(scores) / len(scores)
        
        print("\n" + "="*100)
        print("AI QUALITY SCORE REPORT")
        print("="*100)
        
        print(f"\nTotal Evaluations: {len(self.evaluations)}")
        print(f"Average Quality Score: {avg_score:.1f}/100 ({self._get_grade(avg_score)})")
        
        print(f"\n{'Score Distribution':<40}")
        A_plus = sum(1 for s in scores if s >= 90)
        A = sum(1 for s in scores if 80 <= s < 90)
        B = sum(1 for s in scores if 70 <= s < 80)
        C = sum(1 for s in scores if 60 <= s < 70)
        D = sum(1 for s in scores if 50 <= s < 60)
        F = sum(1 for s in scores if s < 50)
        
        print(f"  A+ (90-100): {A_plus} ({A_plus/len(self.evaluations)*100:.1f}%)")
        print(f"  A  (80-89):  {A} ({A/len(self.evaluations)*100:.1f}%)")
        print(f"  B  (70-79):  {B} ({B/len(self.evaluations)*100:.1f}%)")
        print(f"  C  (60-69):  {C} ({C/len(self.evaluations)*100:.1f}%)")
        print(f"  D  (50-59):  {D} ({D/len(self.evaluations)*100:.1f}%)")
        print(f"  F  (<50):    {F} ({F/len(self.evaluations)*100:.1f}%)")
        
        # Component analysis
        print(f"\n{'Component Contribution (normalized scores)':<100}")
        print("-" * 100)
        
        components = {}
        for e in self.evaluations:
            for component, score in e["normalized_scores"].items():
                if component not in components:
                    components[component] = []
                components[component].append(score)
        
        for component, scores_list in sorted(components.items()):
            avg_comp = sum(scores_list) / len(scores_list)
            weight = self.weights.get(component, 0)
            print(f"{component:<20} {avg_comp:>6.3f}/1.0   (Weight: {weight*100:>5.1f}%)")
        
        # Category breakdown
        categories = {}
        for e in self.evaluations:
            cat = e["category"]
            if cat not in categories:
                categories[cat] = []
            categories[cat].append(e["overall_score"])
        
        if len(categories) > 1:
            print(f"\n{'Scores by Category':<100}")
            print("-" * 100)
            for cat, cat_scores in sorted(categories.items()):
                avg_cat = sum(cat_scores) / len(cat_scores)
                print(f"{cat:<25} {avg_cat:>6.1f}/100 ({self._get_grade(avg_cat)})")
        
        # Detailed results
        print(f"\n{'Detailed Scores':<100}")
        print("="*100)
        
        for i, e in enumerate(self.evaluations, 1):
            print(f"\n[{i:2d}] Q{e['request_id']}")
            print(f"      Input Scores: Rel={e['input_scores']['relevance']:.1f}, "
                  f"Faith={e['input_scores']['faithfulness']:.1f}, "
                  f"Ret={e['input_scores']['retrieval_quality']:.2f}, "
                  f"Compl={e['input_scores']['completeness']:.1f}")
            print(f"      Normalized:  Rel={e['normalized_scores']['relevance']:.2f}, "
                  f"Faith={e['normalized_scores']['faithfulness']:.2f}, "
                  f"Ret={e['normalized_scores']['retrieval_quality']:.2f}, "
                  f"Compl={e['normalized_scores']['completeness']:.2f}")
            print(f"      Overall Score: {e['overall_score']:.1f}/100 ({e['grade']})")
        
        print("\n" + "="*100)
        print("QUALITY SCORE INSIGHTS")
        print("="*100)
        print(f"""
1. OVERALL QUALITY: {avg_score:.1f}/100 ({self._get_grade(avg_score)})
   
2. WEIGHT BREAKDOWN:
   - Relevance (30%): How well do answers address questions?
   - Faithfulness (30%): How supported are answers by documents?
   - Retrieval Quality (20%): How well does RAG find relevant documents?
   - Completeness (10%): Do answers cover all important points?
   - Latency (10%): How fast does the system respond?

3. COMPONENT PERFORMANCE:
   - Look for components below 0.7 (70%) for improvement targets
   - Components scoring < 0.5 need immediate attention

4. BUSINESS IMPLICATIONS:
   - Score >= 80: Production ready
   - Score 60-80: Needs improvement but can be deployed with monitoring
   - Score < 60: Not ready for production

5. RECOMMENDATIONS FOR IMPROVEMENT:
   - If Relevance low: Improve question understanding, prompt engineering
   - If Faithfulness low: Better retrieval, stronger grounding constraints
   - If Retrieval low: Improve indexing, better chunking, embeddings
   - If Completeness low: Larger context windows, multi-hop reasoning
   - If Latency high: Optimize retrieval, caching, parallel processing

6. WEIGHT JUSTIFICATION:
   - Relevance & Faithfulness weighted equally (60% total): Core quality
   - Retrieval Quality (20%): Enables the above
   - Completeness & Latency (20% total): Nice-to-have optimizations
   
   Why these weights?
   - An irrelevant or unfaithful answer is useless
   - Fast but wrong answers are worse than slow but correct
   - Users value correctness over speed/completeness
        """)
        print("="*100)
    
    
    def save_results(self, filepath: str = "evaluation/quality_scores.json"):
        """Save quality scores to JSON."""
        data = {
            "evaluations": self.evaluations,
            "weights": self.weights,
            "summary": {
                "total": len(self.evaluations),
                "average_score": sum(e["overall_score"] for e in self.evaluations) / len(self.evaluations) if self.evaluations else 0,
                "min_score": min(e["overall_score"] for e in self.evaluations) if self.evaluations else 0,
                "max_score": max(e["overall_score"] for e in self.evaluations) if self.evaluations else 0,
                "grade_distribution": {
                    "A+": sum(1 for e in self.evaluations if e["overall_score"] >= 90),
                    "A": sum(1 for e in self.evaluations if 80 <= e["overall_score"] < 90),
                    "B": sum(1 for e in self.evaluations if 70 <= e["overall_score"] < 80),
                    "C": sum(1 for e in self.evaluations if 60 <= e["overall_score"] < 70),
                    "D": sum(1 for e in self.evaluations if 50 <= e["overall_score"] < 60),
                    "F": sum(1 for e in self.evaluations if e["overall_score"] < 50)
                }
            }
        }
        
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2)
        
        print(f"\n[OK] Quality scores saved to: {filepath}")


def main():
    """Run quality score evaluation."""
    
    scorer = QualityScoreBuilder()
    
    print("Calculating Quality Scores...\n")
    
    # Test cases: relevance, faithfulness, retrieval_quality, completeness, latency
    test_cases = [
        ("R001", 5, 5, 0.9, 5, 3.2, "Leave Policy"),
        ("R002", 4, 4, 0.8, 4, 2.9, "Leave Policy"),
        ("R003", 5, 5, 0.95, 5, 3.4, "Work Policies"),
        ("R004", 3, 3, 0.6, 3, 4.1, "Benefits"),
        ("R005", 4, 5, 0.85, 4, 3.0, "Leave Policy"),
        ("R006", 2, 2, 0.4, 2, 5.2, "Office Policies"),
        ("R007", 5, 4, 0.9, 4, 3.3, "Leave Policy"),
        ("R008", 3, 3, 0.5, 3, 6.0, "HR Procedures"),
        ("R009", 4, 4, 0.75, 4, 2.8, "Compensation"),
        ("R010", 5, 5, 0.95, 5, 2.5, "Office Policies"),
    ]
    
    for req_id, rel, faith, ret_qual, compl, latency, cat in test_cases:
        scorer.evaluate(req_id, rel, faith, ret_qual, compl, latency, cat)
    
    # Generate report
    scorer.generate_report()
    
    # Save results
    scorer.save_results()


if __name__ == "__main__":
    main()
