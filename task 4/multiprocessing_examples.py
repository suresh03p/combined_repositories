import multiprocessing
import os
from typing import List


def worker(value: int) -> int:
    """Perform a simple CPU-bound task in a separate process."""
    return value * value


def run_processes(values: List[int]) -> List[int]:
    """Create a process pool and execute work in parallel."""
    with multiprocessing.Pool(processes=4) as pool:
        return pool.map(worker, values)


if __name__ == "__main__":
    print(run_processes([1, 2, 3, 4]))
