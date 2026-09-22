"""
AI Evaluation Complete Test Runner
Executes all evaluation and observability modules.
"""

import subprocess
import json
from datetime import datetime


def run_script(script_name: str, description: str) -> bool:
    """Run a Python script and report status."""
    print(f"\n{'='*80}")
    print(f"Running: {description}")
    print(f"Script: {script_name}")
    print('='*80)
    
    try:
        result = subprocess.run(
            ["python", script_name],
            capture_output=False,
            text=True,
            timeout=30
        )
        if result.returncode == 0:
            print(f"[OK] {script_name} completed successfully")
            return True
        else:
            print(f"[ERROR] {script_name} failed with code {result.returncode}")
            return False
    except subprocess.TimeoutExpired:
        print(f"[ERROR] {script_name} timed out")
        return False
    except Exception as e:
        print(f"[ERROR] Exception running {script_name}: {e}")
        return False


def generate_summary():
    """Generate execution summary."""
    
    results_files = [
        ("evaluation/answer_matching_results.json", "Answer Matching"),
        ("evaluation/relevance_results.json", "Relevance"),
        ("evaluation/retrieval_results.json", "Retrieval"),
        ("evaluation/faithfulness_results.json", "Faithfulness"),
        ("evaluation/llm_judge_results.json", "LLM Judge"),
        ("evaluation/quality_scores.json", "Quality Scores"),
        ("evaluation/agent_evaluation_traces.json", "Agent Traces"),
        ("observability/performance_metrics.json", "Performance Metrics")
    ]
    
    print(f"\n{'='*80}")
    print("EVALUATION RESULTS SUMMARY")
    print('='*80)
    
    for filepath, name in results_files:
        try:
            with open(filepath, 'r') as f:
                data = json.load(f)
                if isinstance(data, dict) and 'summary' in data:
                    summary = data['summary']
                    print(f"\n{name}:")
                    print(f"  - Total: {summary.get('total', 'N/A')}")
                    # Print key metrics based on type
                    if name == "Answer Matching":
                        for metric, value in summary.items():
                            if isinstance(value, (int, float)):
                                print(f"  - {metric}: {value}")
        except FileNotFoundError:
            print(f"\n{name}: [FILE NOT FOUND]")
        except Exception as e:
            print(f"\n{name}: [ERROR] {e}")


def main():
    """Execute all evaluation modules."""
    
    print("""
    
    ╔══════════════════════════════════════════════════════════════════════════╗
    ║                  AI EVALUATION COMPLETE TEST SUITE                       ║
    ║                     Day17 Curriculum - All Tasks                         ║
    ╚══════════════════════════════════════════════════════════════════════════╝
    
    """)
    
    start_time = datetime.now()
    
    # Define all evaluation scripts
    scripts = [
        ("evaluation/answer_matching.py", "TASK 5: Answer Matching"),
        ("evaluation/relevance.py", "TASK 6: Relevance Scoring"),
        ("evaluation/retrieval_evaluation.py", "TASKS 7-10: RAG Retrieval"),
        ("evaluation/faithfulness.py", "TASK 11: Faithfulness"),
        ("evaluation/llm_judge.py", "TASK 13: LLM Judge"),
        ("evaluation/quality_score.py", "TASK 19: Quality Scores"),
        ("evaluation/agent_evaluation.py", "TASKS 17-18: Agent Eval"),
        ("observability/performance_metrics.py", "TASKS 14-16: Performance"),
    ]
    
    results = {}
    for script, description in scripts:
        success = run_script(script, description)
        results[description] = "PASSED" if success else "FAILED"
    
    # Generate summary
    generate_summary()
    
    # Print final results
    print(f"\n{'='*80}")
    print("OVERALL RESULTS")
    print('='*80)
    
    passed = sum(1 for v in results.values() if v == "PASSED")
    total = len(results)
    
    for desc, status in results.items():
        symbol = "[OK]" if status == "PASSED" else "[FAIL]"
        print(f"{symbol} {desc}: {status}")
    
    print(f"\nTotal: {passed}/{total} passed")
    
    elapsed = (datetime.now() - start_time).total_seconds()
    print(f"Time: {elapsed:.1f}s")
    
    if passed == total:
        print("\n[SUCCESS] All evaluations completed successfully!")
    else:
        print(f"\n[WARNING] {total - passed} evaluation(s) failed")
    
    print("\nGenerated Files:")
    print("  - evaluation/ (8 Python modules)")
    print("  - observability/ (1 Python module)")
    print("  - reports/Day17_AI_Evaluation_Report.md")
    print("  - results/ (JSON output files)")
    
    print("\n" + "="*80)


if __name__ == "__main__":
    main()
