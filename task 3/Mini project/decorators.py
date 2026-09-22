import time
from functools import wraps
from logger import logger


def execution_time(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        logger.info(
            f"{func.__name__} executed in {end - start:.4f} seconds"
        )
        return result
    return wrapper
