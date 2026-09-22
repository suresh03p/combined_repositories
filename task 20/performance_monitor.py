import csv
import statistics
import time
from pathlib import Path

class Timer:
    def __enter__(self):
        self.started = time.perf_counter()
        return self
    def __exit__(self, *_):
        self.seconds = time.perf_counter() - self.started

def summarize(values: list[float]) -> dict[str, float]:
    return {"average": statistics.mean(values), "minimum": min(values), "maximum": max(values)}

def write_results(rows: list[dict], output: str = "reports/performance_results.csv") -> None:
    Path(output).parent.mkdir(parents=True, exist_ok=True)
    with open(output, "w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=["request", "retrieval", "llm", "total"])
        writer.writeheader()
        writer.writerows(rows)
