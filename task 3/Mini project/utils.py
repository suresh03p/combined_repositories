import re


def extract_response_time(log: str) -> int:
    match = re.search(r"response_time=(\d+)", log)
    return int(match.group(1)) if match else 0
