"""Benchmark common Python patterns for regex, data structures, and serialization."""

from __future__ import annotations

import gc
import json
import pickle
import re
import time
import tracemalloc
from collections import Counter, defaultdict, deque
from pathlib import Path
from typing import Callable


def benchmark(fn: Callable[[], None], repeats: int = 5) -> tuple[float, float]:
    """Measure average runtime and peak memory for a callable."""
    tracemalloc.start()
    start = time.perf_counter()
    for _ in range(repeats):
        fn()
    elapsed = time.perf_counter() - start
    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    gc.collect()
    return elapsed / repeats, peak / (1024 * 1024)


def regex_benchmark() -> None:
    text = "user@example.com " * 5000
    pattern = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}")
    for _ in range(100):
        pattern.findall(text)


def loop_vs_regex_benchmark() -> None:
    text = "abc123def456ghi789" * 200
    re.findall(r"\d+", text)


def dict_vs_defaultdict_benchmark() -> None:
    mapping: dict[str, int] = {}
    for key in ["a", "b", "a", "c", "b"]:
        mapping[key] = mapping.get(key, 0) + 1
    dd: defaultdict[str, int] = defaultdict(int)
    for key in ["a", "b", "a", "c", "b"]:
        dd[key] += 1


def list_vs_deque_benchmark() -> None:
    items: list[int] = []
    for index in range(1000):
        items.append(index)
    items.pop(0)
    queue: deque[int] = deque()
    for index in range(1000):
        queue.append(index)
    queue.popleft()


def json_vs_pickle_benchmark() -> None:
    payload = {"name": "employee", "values": list(range(1000))}
    json.dumps(payload)
    pickle.dumps(payload)


def generate_report(output_path: Path | None = None) -> str:
    """Generate a benchmark report and write it to disk."""
    output_path = output_path or Path(__file__).resolve().parent / "benchmark_report.txt"
    scenarios = {
        "Compiled regex": regex_benchmark,
        "Loop vs regex": loop_vs_regex_benchmark,
        "dict vs defaultdict": dict_vs_defaultdict_benchmark,
        "list vs deque": list_vs_deque_benchmark,
        "json vs pickle": json_vs_pickle_benchmark,
    }
    lines = ["Benchmark Report", "================", ""]
    for name, fn in scenarios.items():
        avg_time, peak_mem = benchmark(fn)
        lines.append(f"{name}: avg {avg_time:.6f}s | peak {peak_mem:.2f} MB")
    output_path.write_text("\n".join(lines), encoding="utf-8")
    return "\n".join(lines)


if __name__ == "__main__":
    print(generate_report())
