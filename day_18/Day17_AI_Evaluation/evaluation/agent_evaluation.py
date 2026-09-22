"""
TASK 17 & 18: Agent Evaluation and Tracing
Evaluates multi-agent systems and creates request traces.
"""

import json
from datetime import datetime
from typing import List, Dict


class AgentTracer:
    """Trace and evaluate agent execution."""
    
    def __init__(self):
        self.traces = []
        self.agents_used = {}
    
    
    def create_trace(self, trace_id: str, user_question: str, 
                    agents_used: List[str], tools_used: List[str],
                    num_steps: int, total_time: float,
                    success: bool = True, answer: str = ""):
        """Create a trace for a single request."""
        
        trace = {
            "trace_id": trace_id,
            "timestamp": datetime.now().isoformat(),
            "user_question": user_question,
            "agents_used": agents_used,
            "tools_used": tools_used,
            "num_steps": num_steps,
            "total_time": total_time,
            "success": success,
            "answer": answer
        }
        
        self.traces.append(trace)
        
        # Track agent usage
        for agent in agents_used:
            if agent not in self.agents_used:
                self.agents_used[agent] = {"count": 0, "success": 0}
            self.agents_used[agent]["count"] += 1
            if success:
                self.agents_used[agent]["success"] += 1
        
        return trace
    
    
    def generate_report(self):
        """Generate tracing and agent evaluation report."""
        
        if not self.traces:
            print("No traces recorded.")
            return
        
        total_traces = len(self.traces)
        successful = sum(1 for t in self.traces if t["success"])
        avg_steps = sum(t["num_steps"] for t in self.traces) / total_traces
        avg_time = sum(t["total_time"] for t in self.traces) / total_traces
        
        print("\n" + "="*100)
        print("AGENT EVALUATION AND TRACING REPORT")
        print("="*100)
        
        print(f"\nTotal Traces: {total_traces}")
        print(f"Successful: {successful}/{total_traces} ({successful/total_traces*100:.1f}%)")
        print(f"Avg Steps: {avg_steps:.1f}")
        print(f"Avg Time: {avg_time:.2f}s")
        
        # Agent performance
        print(f"\n{'Agent Performance':<100}")
        print("-" * 100)
        print(f"{'Agent':<20} {'Used':<10} {'Success Rate':<15}")
        print("-" * 100)
        
        for agent, stats in sorted(self.agents_used.items()):
            rate = stats["success"] / stats["count"] * 100 if stats["count"] > 0 else 0
            print(f"{agent:<20} {stats['count']:<10} {rate:>10.1f}%")
        
        # Tool usage
        tools_used = {}
        for t in self.traces:
            for tool in t["tools_used"]:
                tools_used[tool] = tools_used.get(tool, 0) + 1
        
        if tools_used:
            print(f"\n{'Tool Usage':<100}")
            print("-" * 100)
            for tool, count in sorted(tools_used.items(), key=lambda x: x[1], reverse=True):
                print(f"{tool:<20} {count} times")
        
        # Detailed traces
        print(f"\n{'Sample Traces':<100}")
        print("="*100)
        
        for i, trace in enumerate(self.traces[:5], 1):
            status = "SUCCESS" if trace["success"] else "FAILED"
            print(f"\n[{i}] {trace['trace_id']} - {status}")
            print(f"    Q: {trace['user_question'][:60]}")
            print(f"    Agents: {', '.join(trace['agents_used'])}")
            print(f"    Tools: {', '.join(trace['tools_used'])}")
            print(f"    Steps: {trace['num_steps']}, Time: {trace['total_time']:.2f}s")
        
        print("\n" + "="*100)
        print("[OK] Report generated")
        print("="*100)
    
    
    def save_results(self, filepath: str = "observability/traces.json"):
        """Save traces to JSON."""
        data = {
            "traces": self.traces,
            "summary": {
                "total": len(self.traces),
                "successful": sum(1 for t in self.traces if t["success"]),
                "success_rate": sum(1 for t in self.traces if t["success"]) / len(self.traces) if self.traces else 0,
                "avg_steps": sum(t["num_steps"] for t in self.traces) / len(self.traces) if self.traces else 0,
                "avg_time": sum(t["total_time"] for t in self.traces) / len(self.traces) if self.traces else 0,
                "agents_performance": self.agents_used
            }
        }
        
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2)
        
        print(f"\n[OK] Traces saved to: {filepath}")


def main():
    """Run agent tracing evaluation."""
    
    tracer = AgentTracer()
    
    print("Recording Agent Traces...\n")
    
    # Sample traces
    traces_data = [
        ("TR-001", "What is the annual leave policy?", ["RAG"], ["rag_search"], 2, 3.4, True),
        ("TR-002", "How do I apply for leave?", ["RAG"], ["rag_search"], 3, 3.8, True),
        ("TR-003", "Calculate my remaining leave", ["RAG", "Calculator"], ["rag_search", "calculate"], 5, 4.2, True),
        ("TR-004", "What is the WFH policy?", ["RAG"], ["rag_search"], 2, 3.1, True),
        ("TR-005", "Policy combination question", ["RAG", "Reasoner"], ["rag_search", "reason"], 4, 5.0, True),
        ("TR-006", "Complex benefits query", ["RAG", "Aggregator"], ["rag_search", "aggregate"], 6, 6.2, True),
        ("TR-007", "Unknown policy", ["RAG"], ["rag_search"], 2, 2.8, False),
        ("TR-008", "Leave calculation", ["Calculator"], ["calculate"], 1, 1.5, True),
        ("TR-009", "Multi-step reasoning", ["RAG", "Calculator", "Reasoner"], ["rag_search", "calculate", "reason"], 7, 7.1, True),
        ("TR-010", "Simple office hours", ["RAG"], ["rag_search"], 1, 2.5, True),
    ]
    
    for trace_id, question, agents, tools, steps, time_taken, success in traces_data:
        tracer.create_trace(trace_id, question, agents, tools, steps, time_taken, success)
    
    tracer.generate_report()
    tracer.save_results()


if __name__ == "__main__":
    main()
