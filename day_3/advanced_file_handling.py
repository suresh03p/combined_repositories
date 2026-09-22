## advanced_file_handling.py

import os
import shutil
import zipfile
from datetime import datetime


class FileManager:

    @staticmethod
    def write_file(filename, content):
        """Write content to a file."""
        with open(filename, "w", encoding="utf-8") as file:
            file.write(content)

        print("File written successfully.")

    @staticmethod
    def read_file(filename):
        """Read file content."""
        try:
            with open(filename, "r", encoding="utf-8") as file:
                return file.read()

        except FileNotFoundError:
            return "File not found."

    @staticmethod
    def append_file(filename, content):
        """Append content to a file."""
        with open(filename, "a", encoding="utf-8") as file:
            file.write(content)

        print("Content appended successfully.")

    @staticmethod
    def search_in_file(filename, keyword):
        ""