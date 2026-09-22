import logging
import threading
import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from urllib.request import urlopen


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)


# =========================
# Thread Example
# =========================
class MyThread(threading.Thread):
    def __init__(self, name, delay=0.2):
        super().__init__(name=name)
        self.delay = delay

    def run(self):
        logger.info("%s started", self.name)
        time.sleep(self.delay)
        logger.info("%s finished", self.name)


# =========================
# Lock Example
# =========================
class Counter:
    def __init__(self):
        self.value = 0
        self.lock = threading.Lock()

    def add(self):
        with self.lock:
            self.value += 1


# =========================
# RLock Example
# =========================
class RCounter:
    def __init__(self):
        self.value = 0
        self.lock = threading.RLock()

    def add(self):
        with self.lock:
            self.value += 1
            self._increment()

    def _increment(self):
        with self.lock:
            self.value += 1


# =========================
# Event Example
# =========================
class EventDemo:
    def __init__(self):
        self.ready = threading.Event()
        self.stop = threading.Event()

    def worker(self):
        logger.info("Waiting")
        self.ready.wait()

        logger.info("Started")
        self.stop.wait(timeout=2)

        logger.info("Stopped")


# =========================
# Semaphore Example
# =========================
class SemDemo:
    def __init__(self, limit):
        self.sem = threading.Semaphore(limit)

    def access(self, name):
        with self.sem:
            logger.info("%s got access", name)
            time.sleep(0.5)
            logger.info("%s released", name)


# =========================
# Producer / Consumer Example
# =========================
class QDemo:
    def __init__(self):
        self.queue = []
        self.lock = threading.Lock()

    def produce(self, items):
        for item in items:
            with self.lock:
                self.queue.append(item)

            logger.info("Produced: %s", item)

    def consume(self):
        while True:
            with self.lock:
                if not self.queue:
                    item = None
                else:
                    item = self.queue.pop(0)

            if item is None:
                time.sleep(0.1)

                with self.lock:
                    if not self.queue:
                        continue

            if item is None:
                break

            logger.info("Consumed: %s", item)


# =========================
# Thread Demo
# =========================
def run_threads():
    threads = [
        MyThread(f"T-{i}", 0.2 + i * 0.1)
        for i in range(3)
    ]

    for t in threads:
        t.start()

    for t in threads:
        t.join()


# =========================
# Thread Pool Demo
# =========================
def run_pool():
    with ThreadPoolExecutor(max_workers=3) as pool:
        result = list(pool.map(lambda x: x * x, [1, 2, 3, 4]))

    logger.info("Pool: %s", result)


# =========================
# Daemon Thread Demo
# =========================
def run_daemon():
    t = threading.Thread(
        target=lambda: (
            time.sleep(0.5),
            logger.info("Daemon done")
        ),
        daemon=True
    )

    t.start()
    t.join(timeout=0.2)

    logger.info("Main keeps going")


# =========================
# Event Demo
# =========================
def run_event():
    demo = EventDemo()

    t = threading.Thread(target=demo.worker)
    t.start()

    time.sleep(0.5)
    demo.ready.set()

    time.sleep(0.5)
    demo.stop.set()

    t.join()


# =========================
# Lock & RLock Demo
# =========================
def run_locks():
    counter = Counter()
    rcounter = RCounter()

    def work():
        for _ in range(5):
            counter.add()
            rcounter.add()

    threads = [
        threading.Thread(target=work)
        for _ in range(3)
    ]

    for t in threads:
        t.start()

    for t in threads:
        t.join()

    logger.info("Lock Counter: %s", counter.value)
    logger.info("RLock Counter: %s", rcounter.value)


# =========================
# Semaphore Demo
# =========================
def run_semaphore():
    demo = SemDemo(2)

    threads = [
        threading.Thread(
            target=demo.access,
            args=(f"T-{i}",)
        )
        for i in range(4)
    ]

    for t in threads:
        t.start()

    for t in threads:
        t.join()


# =========================
# Queue Demo
# =========================
def run_queue():
    demo = QDemo()

    producer = threading.Thread(
        target=demo.produce,
        args=(["A", "B", "C", None],)
    )

    consumer = threading.Thread(
        target=demo.consume
    )

    producer.start()
    consumer.start()

    producer.join()
    consumer.join()


# =========================
# Download Utility
# =========================
def download(url, destination):
    data = urlopen(url).read()

    Path(destination).write_bytes(data)

    logger.info("Downloaded %s", destination)


# =========================
# File Processing
# =========================
def process(path):
    logger.info("Processing %s", path)

    time.sleep(0.3)

    logger.info("Done %s", path)


def read_file(path):
    text = Path(path).read_text(encoding="utf-8")

    logger.info(
        "Read %d chars from %s",
        len(text),
        path
    )


# =========================
# Build Workflow
# =========================
def build():
    logger.info("Starting downloader")

    download(
        "https://example.com",
        "downloaded_page.html"
    )

    logger.info("Starting jobs")

    with ThreadPoolExecutor(max_workers=3) as pool:
        list(
            pool.map(
                process,
                [
                    "img1.jpg",
                    "img2.jpg",
                    "img3.jpg"
                ]
            )
        )

    logger.info("Starting reads")

    with ThreadPoolExecutor(max_workers=2) as pool:
        list(
            pool.map(
                read_file,
                [
                    "Day04/multithreading_examples.py",
                    "Day04/async_examples.py"
                ]
            )
        )


# =========================
# Main
# =========================
if __name__ == "__main__":
    run_threads()
    run_pool()
    run_daemon()
    run_event()
    run_locks()
    run_semaphore()
    run_queue()
    build()