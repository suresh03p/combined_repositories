"""Examples using Python's collection data structures."""

from __future__ import annotations

from collections import Counter, defaultdict, OrderedDict, deque, namedtuple
from typing import Any


def word_frequency_analyzer(text: str) -> Counter[str]:
    """Count word frequencies in a sample string."""
    words = text.lower().replace("\n", " ").split()
    return Counter(words)


class LRUCacheSimulation:
    """A simple LRU cache built with OrderedDict."""

    def __init__(self, capacity: int) -> None:
        self.capacity = capacity
        self.store: OrderedDict[str, int] = OrderedDict()

    def get(self, key: str) -> int | None:
        value = self.store.pop(key, None)
        if value is None:
            return None
        self.store[key] = value
        return value

    def put(self, key: str, value: int) -> None:
        if key in self.store:
            self.store.pop(key)
        self.store[key] = value
        if len(self.store) > self.capacity:
            self.store.popitem(last=False)


class QueueManager:
    """A queue implementation using deque."""

    def __init__(self) -> None:
        self._queue: deque[str] = deque()

    def enqueue(self, item: str) -> None:
        self._queue.append(item)

    def dequeue(self) -> str | None:
        return self._queue.popleft() if self._queue else None


class InventoryTracker:
    """Track inventory using defaultdict."""

    def __init__(self) -> None:
        self.items: defaultdict[str, int] = defaultdict(int)

    def add(self, sku: str, quantity: int) -> None:
        self.items[sku] += quantity

    def get(self, sku: str) -> int:
        return self.items[sku]


class TaskScheduler:
    """Define tasks using namedtuple."""

    Task = namedtuple("Task", ["name", "priority", "due_day"])

    def __init__(self) -> None:
        self.tasks: list[object] = []

    def add_task(self, name: str, priority: int, due_day: int) -> None:
        self.tasks.append(self.Task(name=name, priority=priority, due_day=due_day))

    def sorted_tasks(self) -> list[Task]:
        return sorted(self.tasks, key=lambda task: (task.priority, task.due_day))


def demo() -> list[dict[str, Any]]:
    """Run a simple set of collection examples."""
    text = "python python is great great for data processing"
    frequencies = word_frequency_analyzer(text)
    cache = LRUCacheSimulation(2)
    cache.put("a", 1)
    cache.put("b", 2)
    cache.get("a")
    cache.put("c", 3)
    queue = QueueManager()
    queue.enqueue("job-1")
    queue.enqueue("job-2")
    inventory = InventoryTracker()
    inventory.add("SKU1", 5)
    inventory.add("SKU1", 3)
    scheduler = TaskScheduler()
    scheduler.add_task("Deploy", 2, 3)
    scheduler.add_task("Test", 1, 2)
    results = [
        ("Word Frequency", dict(frequencies)),
        ("LRU Cache", dict(cache.store)),
        ("Queue", queue.dequeue()),
        ("Inventory", dict(inventory.items)),
        ("Task Order", [task.name for task in scheduler.sorted_tasks()]),
    ]
    for name, value in results:
        print(f"{name}: {value}")
    return [{"name": name, "value": value} for name, value in results]


if __name__ == "__main__":
    demo()
