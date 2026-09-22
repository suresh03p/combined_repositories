from typing import Generic, TypeVar

T = TypeVar("T")


class InMemoryStorage(Generic[T]):
    def __init__(self) -> None:
        self._values: dict[str, T] = {}

    def get(self, key: str) -> T | None:
        return self._values.get(key)

    def set(self, key: str, value: T) -> None:
        self._values[key] = value
