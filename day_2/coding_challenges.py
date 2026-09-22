import asyncio
import csv
import math
import os
import queue
import tempfile
import threading
import time
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor
from pathlib import Path
from typing import Any, Callable, List, Sequence, Tuple
from urllib.request import Request, urlopen

try:
    from PIL import Image
except ImportError:  # pragma: no cover
    Image = None


class ProducerConsumerDemo:
    """Simple producer-consumer example with a thread-safe queue."""

    def __init__(self, size: int = 5) -> None:
        self.queue: "queue.Queue[int]" = queue.Queue(maxsize=size)
        self.stop_event = threading.Event()

    def producer(self, items: Sequence[int]) -> None:
        for item in items:
            self.queue.put(item)
        self.stop_event.set()

    def consumer(self) -> List[int]:
        results: List[int] = []
        while True:
            if self.stop_event.is_set() and self.queue.empty():
                break
            try:
                item = self.queue.get(timeout=0.2)
                results.append(item)
                self.queue.task_done()
            except queue.Empty:
                continue
        return results


def is_prime(n: int) -> bool:
    """Return True if n is a prime number."""
    if n < 2:
        return False
    for factor in range(2, int(math.isqrt(n)) + 1):
        if n % factor == 0:
            return False
    return True


def find_primes(numbers: Sequence[int]) -> List[int]:
    """Find prime numbers using a thread pool."""
    with ThreadPoolExecutor(max_workers=4) as executor:
        flags = list(executor.map(is_prime, numbers))
    return [number for number, is_prime_number in zip(numbers, flags) if is_prime_number]


class ThreadSafeCounter:
    """Thread-safe counter using a lock."""

    def __init__(self) -> None:
        self.value = 0
        self.lock = threading.Lock()

    def increment(self) -> None:
        with self.lock:
            self.value += 1

    def get_value(self) -> int:
        with self.lock:
            return self.value


def multiply_cell(args: Tuple[List[List[int]], int, int]) -> Tuple[int, int, int]:
    """Compute one cell in matrix multiplication."""
    matrix, row, col = args
    total = 0
    for index in range(len(matrix[row])):
        total += matrix[row][index] * matrix[col][index]
    return row, col, total


def matrix_multiplication(matrix: List[List[int]]) -> List[List[int]]:
    """Perform matrix multiplication using a process pool."""
    size = len(matrix)
    result = [[0 for _ in range(size)] for _ in range(size)]
    with ProcessPoolExecutor(max_workers=4) as executor:
        futures = [executor.submit(multiply_cell, (matrix, i, j)) for i in range(size) for j in range(size)]
        for future in futures:
            row, col, value = future.result()
            result[row][col] = value
    return result


async def schedule_tasks(tasks: Sequence[Callable[[], None]]) -> None:
    """Run a list of tasks concurrently."""
    async def run_task(task: Callable[[], None]) -> None:
        await asyncio.sleep(0)
        task()

    await asyncio.gather(*(run_task(task) for task in tasks))


class ConcurrentLogProcessor:
    """Thread-safe log writer."""

    def __init__(self, log_file: str) -> None:
        self.log_file = log_file
        self.lock = threading.Lock()

    def process_log(self, message: str) -> None:
        with self.lock:
            with open(self.log_file, "a", encoding="utf-8") as handle:
                handle.write(message + "\n")

    def process_many(self, messages: Sequence[str]) -> None:
        with ThreadPoolExecutor(max_workers=4) as executor:
            list(executor.map(self.process_log, messages))


def process_csv(path: str) -> List[dict[str, Any]]:
    """Read rows from a CSV file."""
    with open(path, "r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        return list(reader)


def process_csvs(paths: Sequence[str]) -> List[List[dict[str, Any]]]:
    """Process multiple CSV files in parallel."""
    with ThreadPoolExecutor(max_workers=4) as executor:
        return list(executor.map(process_csv, paths))


if __name__ == "__main__":
    print("Prime numbers:", find_primes([2, 3, 4, 5, 7, 8, 11]))

    demo_queue = ProducerConsumerDemo(size=3)
    producer_thread = threading.Thread(target=demo_queue.producer, args=([1, 2, 3],))
    consumer_thread = threading.Thread(target=lambda: print("Queue output:", demo_queue.consumer()))
    producer_thread.start()
    consumer_thread.start()
    producer_thread.join()
    consumer_thread.join()

    counter = ThreadSafeCounter()
    for _ in range(5):
        counter.increment()
    print("Counter:", counter.get_value())

    sample_matrix = [[1, 2], [3, 4]]
    print("Matrix multiplication:", matrix_multiplication(sample_matrix))

    asyncio.run(schedule_tasks([lambda: print("Task 1"), lambda: print("Task 2")]))

    with tempfile.TemporaryDirectory() as tmp_dir:
        log_path = os.path.join(tmp_dir, "demo.log")
        processor = ConcurrentLogProcessor(log_path)
        processor.process_many(["a", "b", "c"])
        with open(log_path, "r", encoding="utf-8") as handle:
            print("Log file:", handle.read().strip().splitlines())

        csv_path = os.path.join(tmp_dir, "demo.csv")
        with open(csv_path, "w", newline="", encoding="utf-8") as handle:
            writer = csv.writer(handle)
            writer.writerow(["name", "age"])
            writer.writerow(["Alice", 20])
            writer.writerow(["Bob", 21])
        print("CSV rows:", process_csv(csv_path))
