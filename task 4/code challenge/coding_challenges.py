import asyncio
import csv
import math
import os
import queue
import threading
import time
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor
from pathlib import Path
from typing import Any, Callable, List, Sequence, Tuple
from urllib.request import Request, urlopen


# 1. Multi-threaded File Downloader

def download_file(url: str, destination: str) -> None:
    req = Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urlopen(req, timeout=10) as response:
        Path(destination).parent.mkdir(parents=True, exist_ok=True)
        with open(destination, "wb") as handle:
            handle.write(response.read())


def download_files(urls: Sequence[Tuple[str, str]]) -> None:
    with ThreadPoolExecutor(max_workers=4) as executor:
        list(executor.map(lambda item: download_file(item[0], item[1]), urls))


# 2. Producer-Consumer Queue

class ProducerConsumerDemo:
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


# 3. Parallel Prime Number Finder

def is_prime(n: int) -> bool:
    if n < 2:
        return False
    for i in range(2, int(math.isqrt(n)) + 1):
        if n % i == 0:
            return False
    return True


def find_primes(numbers: Sequence[int]) -> List[int]:
    with ThreadPoolExecutor(max_workers=4) as executor:
        results = list(executor.map(is_prime, numbers))
    return [num for num, flag in zip(numbers, results) if flag]


# 4. Async Web Scraper

async def fetch_url(url: str) -> str:
    loop = asyncio.get_running_loop()
    await loop.run_in_executor(None, lambda: urlopen(Request(url, headers={"User-Agent": "Mozilla/5.0"})).read().decode("utf-8", errors="ignore"))
    return url


async def scrape_urls(urls: Sequence[str]) -> List[str]:
    tasks = [asyncio.create_task(fetch_url(url)) for url in urls]
    return await asyncio.gather(*tasks)


# 5. Thread-safe Counter

class ThreadSafeCounter:
    def __init__(self) -> None:
        self.value = 0
        self.lock = threading.Lock()

    def increment(self) -> None:
        with self.lock:
            self.value += 1

    def get_value(self) -> int:
        with self.lock:
            return self.value


# 6. Process-based Matrix Multiplication

def multiply_row_column(args: Tuple[List[List[int]], int, int]) -> int:
    matrix_a, row, col = args
    total = 0
    for index in range(len(matrix_a[row])):
        total += matrix_a[row][index] * matrix_a[col][index]
    return total


def matrix_multiplication(matrix: List[List[int]]) -> List[List[int]]:
    size = len(matrix)
    result = [[0 for _ in range(size)] for _ in range(size)]
    with ProcessPoolExecutor(max_workers=4) as executor:
        for i in range(size):
            for j in range(size):
                result[i][j] = executor.submit(multiply_row_column, (matrix, i, j)).result()
    return result


# 7. Async Task Scheduler

async def schedule_tasks(tasks: Sequence[Callable[[], None]]) -> None:
    async def run_task(task: Callable[[], None]) -> None:
        await asyncio.sleep(0)
        task()

    await asyncio.gather(*(run_task(task) for task in tasks))


# 8. Concurrent Log Processor

class ConcurrentLogProcessor:
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


# 9. Multi-threaded Image Resizer

from PIL import Image


def resize_image(input_path: str, output_path: str, size: Tuple[int, int]) -> None:
    with Image.open(input_path) as image:
        resized = image.resize(size)
        resized.save(output_path)


def resize_images(files: Sequence[Tuple[str, str, Tuple[int, int]]]) -> None:
    with ThreadPoolExecutor(max_workers=4) as executor:
        list(executor.map(lambda item: resize_image(item[0], item[1], item[2]), files))


# 10. Parallel CSV Processor

def process_csv(path: str) -> List[dict[str, Any]]:
    with open(path, "r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        return list(reader)


def process_csvs(paths: Sequence[str]) -> List[List[dict[str, Any]]]:
    with ThreadPoolExecutor(max_workers=4) as executor:
        return list(executor.map(process_csv, paths))


if __name__ == "__main__":
    print("Concurrency challenge script ready")
