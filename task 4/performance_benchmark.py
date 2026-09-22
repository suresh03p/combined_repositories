import logging
import statistics
import threading
import time
from typing import List, Tuple

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)


def measure_threaded_work(count: int = 5) -> Tuple[float, List[float]]:
    """Benchmark a simple threaded workload."""
    timings: List[float] = []

    def worker() -> None:
        start = time.perf_counter()
        time.sleep(0.2)
        timings.append(time.perf_counter() - start)

    threads = [threading.Thread(target=worker) for _ in range(count)]
    start = time.perf_counter()
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()
    total = time.perf_counter() - start
    return total, timings


if __name__ == "__main__":
    total, timings = measure_threaded_work()
    logger.info("Total time: %.3f seconds", total)
    logger.info("Per-thread timings: %s", timings)
    logger.info("Average: %.3f seconds", statistics.mean(timings))
