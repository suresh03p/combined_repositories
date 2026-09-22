from collections.abc import Generator
from context_manager import FileManager


def read_log_file(file_path: str) -> Generator[str, None, None]:
    with FileManager(file_path) as file:
        for line in file:
            yield line.strip()


def read_multiple_files(files: list[str]) -> Generator[str, None, None]:
    for file in files:
        yield from read_log_file(file)
