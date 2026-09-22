"""
TASKS 14-16: Observability Metrics
- TASK 14: Latency Monitoring
- TASK 15: Token Usage Tracking  
- TASK 16: Cost Tracking

Track performance and cost metrics for AI system requests.
"""

import json
import statistics
from typing import List, Dict
from datetime import datetime


class PerformanceMetrics:
    """Track latency, tokens, and costs for AI requests."""
    
    def __init__(self, model: str = "gpt-4", 
                 input_price_per_1k: float = 0.005,
                 output_price_per_1k: float = 0.015):
        """
        Initialize with model and pricing.
        
        Example pricing (illustrative, not current rates):
        - GPT-4: $0.005 per 1K input tokens, $0.015 per 1K output tokens
        """
        self.model = model
        self.input_price_per_1k = input_price_per_1k
        self.output_price_per_1k = output_price_per_1k
        self.requests = []
    
    
    def log_request(self, request_id: str, question: str, 
                   retrieval_time: float, llm_time: float,
                   input_tokens: int, output_tokens: int,
                   tool_name: str = "rag_search"):
        """
        Log a single AI request with all metrics.
        
        Args:
            request_id: Unique request identifier
            question: User question/prompt
            retrieval_time: Time for document retrieval (seconds)
            llm_time: Time for LLM processing (seconds)
            input_tokens: Tokens in prompt+context
            output_tokens: Tokens in response
            tool_name: Which tool was used
        """
        
        total_time = retrieval_time + llm_time
        total_tokens = input_tokens + output_tokens
        
        # Calculate cost
        input_cost = (input_tokens / 1000) * self.input_price_per_1k
        output_cost = (output_tokens / 1000) * self.output_price_per_1k
        total_cost = input_cost + output_cost
        
        request = {
            "request_id": request_id,
            "timestamp": datetime.now().isoformat(),
            "question": question,
            "model": self.model,
            "tool_used": tool_name,
            # Timing
            "retrieval_time": retrieval_time,
            "llm_time": llm_time,
            "total_time": total_time,
            # Tokens
            "input_tokens": input_tokens,
            "output_tokens": output_tokens,
            "total_tokens": total_tokens,
            # Cost
            "input_cost": round(input_cost, 6),
            "output_cost": round(output_cost, 6),
            "total_cost": round(total_cost, 6)
        }
        
        self.requests.append(request)
        return request
    
    
    def calculate_latency_stats(self) -> Dict:
        """Calculate latency statistics across all requests."""
        
        if not self.requests:
            return {}
        
        times = [r["total_time"] for r in self.requests]
        retrieval_times = [r["retrieval_time"] for r in self.requests]
        llm_times = [r["llm_time"] for r in self.requests]
        
        def calculate_percentile(data, percentile):
            sorted_data = sorted(data)
            index = (len(sorted_data) - 1) * (percentile / 100)
            lower = int(index)
            upper = lower + 1
            if upper >= len(sorted_data):
                return sorted_data[lower]
            return sorted_data[lower] * (1 - (index - lower)) + sorted_data[upper] * (index - lower)
        
        return {
            "total_time": {
                "avg": statistics.mean(times),
                "min": min(times),
                "max": max(times),
                "median": statistics.median(times),
                "p50": calculate_percentile(times, 50),
                "p95": calculate_percentile(times, 95),
                "p99": calculate_percentile(times, 99),
                "stdev": statistics.stdev(times) if len(times) > 1 else 0
            },
            "retrieval_time": {
                "avg": statistics.mean(retrieval_times),
                "min": min(retrieval_times),
                "max": max(retrieval_times),
                "median": statistics.median(retrieval_times)
            },
            "llm_time": {
                "avg": statistics.mean(llm_times),
                "min": min(llm_times),
                "max": max(llm_times),
                "median": statistics.median(llm_times)
            }
        }
    
    
    def calculate_token_stats(self) -> Dict:
        """Calculate token usage statistics."""
        
        if not self.requests:
            return {}
        
        input_tokens = [r["input_tokens"] for r in self.requests]
        output_tokens = [r["output_tokens"] for r in self.requests]
        total_tokens = [r["total_tokens"] for r in self.requests]
        
        return {
            "input_tokens": {
                "total": sum(input_tokens),
                "average": statistics.mean(input_tokens),
                "min": min(input_tokens),
                "max": max(input_tokens)
            },
            "output_tokens": {
                "total": sum(output_tokens),
                "average": statistics.mean(output_tokens),
                "min": min(output_tokens),
                "max": max(output_tokens)
            },
            "total_tokens": {
                "total": sum(total_tokens),
                "average": statistics.mean(total_tokens),
                "min": min(total_tokens),
                "max": max(total_tokens)
            }
        }
    
    
    def calculate_cost_stats(self) -> Dict:
        """Calculate cost statistics."""
        
        if not self.requests:
            return {}
        
        costs = [r["total_cost"] for r in self.requests]
        input_costs = [r["input_cost"] for r in self.requests]
        output_costs = [r["output_cost"] for r in self.requests]
        
        return {
            "total_cost": sum(costs),
            "average_cost_per_request": statistics.mean(costs),
            "min_cost": min(costs),
            "max_cost": max(costs),
            "input_cost_total": sum(input_costs),
            "output_cost_total": sum(output_costs),
            "cost_breakdown": {
                "input": f"{(sum(input_costs)/sum(costs)*100):.1f}%" if sum(costs) > 0 else "0%",
                "output": f"{(sum(output_costs)/sum(costs)*100):.1f}%" if sum(costs) > 0 else "0%"
            }
        }
    
    
    def generate_report(self):
        """Generate comprehensive observability report."""
        
        if not self.requests:
            print("No requests logged.")
            return
        
        latency_stats = self.calculate_latency_stats()
        token_stats = self.calculate_token_stats()
        cost_stats = self.calculate_cost_stats()
        
        print("\n" + "="*100)
        print("OBSERVABILITY REPORT - PERFORMANCE & COST")
        print("="*100)
        
        print(f"\nModel: {self.model}")
        print(f"Total Requests: {len(self.requests)}")
        print(f"Date Range: {self.requests[0]['timestamp']} to {self.requests[-1]['timestamp']}")
        
        # LATENCY SECTION
        print(f"\n{'='*100}")
        print("LATENCY METRICS (seconds)")
        print("="*100)
        
        print(f"\n{'Total Time (End-to-End)':<40}")
        print(f"  Average:    {latency_stats['total_time']['avg']:.3f}s")
        print(f"  Min:        {latency_stats['total_time']['min']:.3f}s")
        print(f"  Max:        {latency_stats['total_time']['max']:.3f}s")
        print(f"  Median:     {latency_stats['total_time']['median']:.3f}s")
        print(f"  P50:        {latency_stats['total_time']['p50']:.3f}s")
        print(f"  P95:        {latency_stats['total_time']['p95']:.3f}s")
        print(f"  P99:        {latency_stats['total_time']['p99']:.3f}s")
        print(f"  StdDev:     {latency_stats['total_time']['stdev']:.3f}s")
        
        print(f"\n{'Retrieval Time':<40}")
        print(f"  Average:    {latency_stats['retrieval_time']['avg']:.3f}s")
        print(f"  Min:        {latency_stats['retrieval_time']['min']:.3f}s")
        print(f"  Max:        {latency_stats['retrieval_time']['max']:.3f}s")
        
        print(f"\n{'LLM Processing Time':<40}")
        print(f"  Average:    {latency_stats['llm_time']['avg']:.3f}s")
        print(f"  Min:        {latency_stats['llm_time']['min']:.3f}s")
        print(f"  Max:        {latency_stats['llm_time']['max']:.3f}s")
        
        # TOKEN SECTION
        print(f"\n{'='*100}")
        print("TOKEN USAGE METRICS")
        print("="*100)
        
        print(f"\n{'Input Tokens (context + question)':<40}")
        print(f"  Total:      {token_stats['input_tokens']['total']:,}")
        print(f"  Average:    {token_stats['input_tokens']['average']:.0f}")
        print(f"  Min:        {token_stats['input_tokens']['min']}")
        print(f"  Max:        {token_stats['input_tokens']['max']}")
        
        print(f"\n{'Output Tokens (response)':<40}")
        print(f"  Total:      {token_stats['output_tokens']['total']:,}")
        print(f"  Average:    {token_stats['output_tokens']['average']:.0f}")
        print(f"  Min:        {token_stats['output_tokens']['min']}")
        print(f"  Max:        {token_stats['output_tokens']['max']}")
        
        print(f"\n{'Total Tokens (per request)':<40}")
        print(f"  Total:      {token_stats['total_tokens']['total']:,}")
        print(f"  Average:    {token_stats['total_tokens']['average']:.0f}")
        print(f"  Min:        {token_stats['total_tokens']['min']}")
        print(f"  Max:        {token_stats['total_tokens']['max']}")
        
        # COST SECTION
        print(f"\n{'='*100}")
        print("COST METRICS (USD)")
        print("="*100)
        
        print(f"\nPricing Configuration:")
        print(f"  Input:  ${self.input_price_per_1k}/1K tokens")
        print(f"  Output: ${self.output_price_per_1k}/1K tokens")
        
        print(f"\n{'Cost Breakdown':<40}")
        print(f"  Total Cost:     ${cost_stats['total_cost']:.4f}")
        print(f"  Per Request:    ${cost_stats['average_cost_per_request']:.6f}")
        print(f"  Min Request:    ${cost_stats['min_cost']:.6f}")
        print(f"  Max Request:    ${cost_stats['max_cost']:.6f}")
        
        print(f"\n{'Cost Distribution':<40}")
        print(f"  Input Cost:     ${cost_stats['input_cost_total']:.4f} ({cost_stats['cost_breakdown']['input']})")
        print(f"  Output Cost:    ${cost_stats['output_cost_total']:.4f} ({cost_stats['cost_breakdown']['output']})")
        
        # INSIGHTS
        print(f"\n{'='*100}")
        print("KEY INSIGHTS")
        print("="*100)
        print(f"""
1. LATENCY PERFORMANCE:
   - P95 Latency: {latency_stats['total_time']['p95']:.2f}s
   - This is the time 95% of requests complete within
   - For production, target: < 5s for most queries
   
2. RETRIEVAL vs LLM TIME:
   - Retrieval: {latency_stats['retrieval_time']['avg']:.3f}s/request
   - LLM: {latency_stats['llm_time']['avg']:.3f}s/request
   - Ratio: {latency_stats['retrieval_time']['avg']/latency_stats['llm_time']['avg']:.1%} retrieval vs LLM time
   
3. TOKEN EFFICIENCY:
   - Avg input tokens: {token_stats['input_tokens']['average']:.0f}
   - Avg output tokens: {token_stats['output_tokens']['average']:.0f}
   - Ratio: {token_stats['output_tokens']['average']/token_stats['input_tokens']['average']:.1%}
   
4. COST ANALYSIS:
   - Total cost for {len(self.requests)} requests: ${cost_stats['total_cost']:.4f}
   - Cost per request: ${cost_stats['average_cost_per_request']:.6f}
   - Estimated cost per 1000 requests: ${cost_stats['total_cost']/len(self.requests)*1000:.2f}
   
5. OPTIMIZATION OPPORTUNITIES:
   - Longer context = more tokens = higher cost
   - Consider truncating context or using more targeted retrieval
   - Shorter responses = lower output token cost
   
6. PERFORMANCE TARGETS:
   - Latency P95: < 5 seconds
   - Avg tokens/request: < 2000
   - Cost per request: < $0.001
        """)
        print("="*100)
    
    
    def save_results(self, filepath: str = "observability/performance_metrics.json"):
        """Save metrics to JSON."""
        data = {
            "requests": self.requests,
            "summary": {
                "total_requests": len(self.requests),
                "model": self.model,
                "latency": self.calculate_latency_stats(),
                "tokens": self.calculate_token_stats(),
                "costs": self.calculate_cost_stats()
            }
        }
        
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2)
        
        print(f"\n[OK] Metrics saved to: {filepath}")


def main():
    """Simulate and log AI requests."""
    
    metrics = PerformanceMetrics(
        model="gpt-4-turbo",
        input_price_per_1k=0.005,
        output_price_per_1k=0.015
    )
    
    print("Logging AI Requests...\n")
    
    # Simulate various requests
    requests_data = [
        ("R001", "What is annual leave?", 0.20, 3.2, 1200, 250),
        ("R002", "How do I apply for leave?", 0.18, 2.9, 900, 180),
        ("R003", "Work from home policy?", 0.25, 3.4, 1100, 220),
        ("R004", "What benefits exist?", 0.19, 3.1, 1300, 240),
        ("R005", "Maternity leave details?", 0.21, 3.3, 1400, 260),
        ("R006", "Office hours?", 0.17, 2.8, 800, 150),
        ("R007", "Sick leave policy?", 0.22, 3.2, 1150, 230),
        ("R008", "Performance appraisal?", 0.20, 3.0, 950, 190),
        ("R009", "Overtime compensation?", 0.23, 3.4, 1250, 270),
        ("R010", "Dress code?", 0.19, 2.9, 850, 160),
    ]
    
    for req_id, question, ret_time, llm_time, in_tokens, out_tokens in requests_data:
        metrics.log_request(req_id, question, ret_time, llm_time, in_tokens, out_tokens)
    
    # Generate report
    metrics.generate_report()
    
    # Save results
    metrics.save_results()


if __name__ == "__main__":
    main()
