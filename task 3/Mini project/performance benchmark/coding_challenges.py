"""
coding_challenges.py

Advanced Python Coding Challenges:
1. Custom Range Iterator
2. Prime Generator
3. Infinite Fibonacci Generator
4. Memoization Decorator
5. Retry Decorator
6. Timing Decorator
7. Singleton Decorator
8. Custom File Context Manager
9. Batch Processing Generator
10. Circular Iterator
"""

from __future__ import annotations

import logging
import time
from functools import wraps
from typing import Any, Callable, Generator, Iterator, List, TypeVar

# --------------------------------------------------
# Logging Configuration
# --------------------------------------------------

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)

T = TypeVar("T")


# ==================================================
# 1. Custom Range Iterator
# ==================================================


class CustomRange:
    """
    Custom implementation of Python's range().
    """

    def __init__(self, start: int, end: int, step: int = 1) -> None:
        self.start = start
        self.end = end
        self.step = step

    def __iter__(self) -> Iterator[int]:
        current = self.start
        while current < self.end:
            yield current
            current += self.step


# ==================================================
# 2. Prime Generator
# ==================================================


def prime_generator(limit: int) -> Generator[int, None, None]:
    """
    Generate prime numbers up to a limit.
    """

    for num in range(2, limit + 1):
        prime = True

        for i in range(2, int(num ** 0.5) + 1):
            if num % i == 0:
                prime = False
                break

        if prime:
            yield num


# ==================================================
# 3. Infinite Fibonacci Generator
# ==================================================


def fibonacci_generator() -> Generator[int, None, None]:
    """
    Infinite Fibonacci sequence generator.
    """

    a, b = 0, 1

    while True:
        yield a
        a, b = b, a + b


# ==================================================
# 4. Memoization Decorator
# ==================================================


def memoize(func: Callable[..., Any]) -> Callable[..., Any]:
    """
    Cache function results.
    """

    cache: dict[tuple[Any, ...], Any] = {}

    @wraps(func)
    def wrapper(*args: Any) -> Any:
        if args not in cache:
            cache[args] = func(*args)
        return cache[args]

    return wrapper


@memoize

def fibonacci(n: int) -> int:
    """
    Recursive Fibonacci implementation.
    """

    if n < 2:
        return n

    return fibonacci(n - 1) + fibonacci(n - 2)


# ==================================================
# 5. Retry Decorator
# ==================================================


def retry(
    retries: int = 3,
    delay: float = 1.0
) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
    """
    Retry failed function execution.
    """

    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:

        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            for attempt in range(1, retries + 1):
                try:
                    return func(*args, **kwargs)
                except Exception as exc:
                    logger.warning(
                        "Attempt %s failed: %s",
                        attempt,
                        exc
                    )
                    if attempt == retries:
                        raise
                    time.sleep(delay)

        return wrapper

    return decorator


# ==================================================
# 6. Timing Decorator
# ==================================================


def timing(func: Callable[..., Any]) -> Callable[..., Any]:
    """
    Measure execution time.
    """

    @wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        start = time.perf_counter()
        result = func(*args, **kwargs)
        duration = time.perf_counter() - start
        logger.info(
            "%s executed in %.6f seconds",
            func.__name__,
            duration
        )
        return result

    return wrapper


# ==================================================
# 7. Singleton Decorator
# ==================================================


def singleton(cls: type) -> Callable[..., Any]:
    """
    Singleton class decorator.
    """

    instances: dict[type, Any] = {}

    @wraps(cls)
    def get_instance(*args: Any, **kwargs: Any) -> Any:
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]

    return get_instance


@singleton
class Database:
    """
    Example Singleton.
    """

    pass


# ==================================================
# 8. Custom File Context Manager
# ==================================================


class FileManager:
    """
    Custom context manager for file handling.
    """

    def __init__(self, filename: str, mode: str):
        self.filename = filename
        self.mode = mode
        self.file = None

    def __enter__(self):
        self.file = open(
            self.filename,
            self.mode,
            encoding="utf-8"
        )
        return self.file

    def __exit__(
        self,
        exc_type,
        exc_value,
        traceback
    ) -> bool:
        if self.file:
            self.file.close()
        if exc_type:
            logger.error("Exception: %s", exc_value)
        return False


# ==================================================
# 9. Batch Processing Generator
# ==================================================


def batch_generator(
    data: List[Any],
    batch_size: int
) -> Generator[List[Any], None, None]:
    """
    Yield data in batches.
    """

    for i in range(0, len(data), batch_size):
        yield data[i:i + batch_size]


# ==================================================
# 10. Circular Iterator
# ==================================================


class CircularIterator:
    """
    Infinite circular iterator.
    """

    def __init__(self, items: List[Any]):
        if not items:
            raise ValueError("List cannot be empty.")
        self.items = items
        self.index = 0

    def __iter__(self) -> Iterator[Any]:
        return self

    def __next__(self) -> Any:
        item = self.items[self.index]
        self.index = (self.index + 1) % len(self.items)
        return item


# ==================================================
# Example Usage
# ==================================================

if __name__ == "__main__":
    print("Custom Range:")
    for value in CustomRange(1, 6):
        print(value)

    print("\nPrime Numbers:")
    print(list(prime_generator(30)))

    print("\nFirst 10 Fibonacci Numbers:")
    fib = fibonacci_generator()
    for _ in range(10):
        print(next(fib), end=" ")
    print("\n")

    print("Memoized Fibonacci(10):")
    print(fibonacci(10))

    print("\nBatch Generator:")
    for batch in batch_generator(list(range(10)), 3):
        print(batch)

    print("\nCircular Iterator:")
    circular = CircularIterator(["A", "B", "C"])
    for _ in range(10):
        print(next(circular), end=" ")
''