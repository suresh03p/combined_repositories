from typing import TextIO


class FileManager:
    def __init__(self, filepath: str):
        self.filepath = filepath
        self.file: TextIO | None = None

    def __enter__(self):
        self.file = open(
            self.filepath,
            mode="r",
            encoding="utf-8"
        )
        return self.file

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.file:
            self.file.close()
        return False
