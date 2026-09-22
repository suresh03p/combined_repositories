from collections.abc import Generator, Iterable


def filter_by_date(logs: Iterable[str], date: str) -> Generator[str, None, None]:
    for log in logs:
        if log.startswith(date):
            yield log


def filter_by_level(logs: Iterable[str], level: str) -> Generator[str, None, None]:
    for log in logs:
        if f" {level} " in log:
            yield log


def filter_by_module(logs: Iterable[str], module: str) -> Generator[str, None, None]:
    for log in logs:
        if module in log:
            yield log


def filter_by_keyword(logs: Iterable[str], keyword: str) -> Generator[str, None, None]:
    for log in logs:
        if keyword.lower() in log.lower():
            yield log
