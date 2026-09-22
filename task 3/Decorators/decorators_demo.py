import time
import logging
from functools import wraps

# ---------------------------------------------------------
# Configure Logging
# ---------------------------------------------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# =========================================================
# 1. Logging Decorator
# =========================================================
def log_decorator(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        logging.info(f"Calling: {func.__name__}")
        result = func(*args, **kwargs)
        logging.info(f"Finished: {func.__name__}")
        return result
    return wrapper


# =========================================================
# 2. Execution Time Logger Decorator
# =========================================================
def execution_time(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()

        result = func(*args, **kwargs)

        end = time.time()
        print(f"[TIME] {func.__name__} took {end-start:.4f} seconds")

        return result
    return wrapper


# =========================================================
# 3. Authentication Decorator
# =========================================================
def authenticate(func):
    @wraps(func)
    def wrapper(user, *args, **kwargs):
        if not user.get("authenticated"):
            raise PermissionError("User is not authenticated!")

        return func(user, *args, **kwargs)

    return wrapper


# =========================================================
# 4. Retry Decorator (Parameterized)
# =========================================================
def retry(max_attempts=3):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):

            for attempt in range(1, max_attempts + 1):
                try:
                    return func(*args, **kwargs)

                except Exception as e:
                    print(
                        f"Attempt {attempt}/{max_attempts} failed: {e}"
                    )

                    if attempt == max_attempts:
                        raise

        return wrapper
    return decorator


# =========================================================
# 5. Cache Decorator
# =========================================================
def cache_result(func):
    cache = {}

    @wraps(func)
    def wrapper(*args):

        if args in cache:
            print("Returning cached result...")
            return cache[args]

        result = func(*args)
        cache[args] = result

        return result

    return wrapper


# =========================================================
# 6. Validation Decorator
# =========================================================
def validate_positive(func):
    @wraps(func)
    def wrapper(*args, **kwargs):

        for value in args:
            if isinstance(value, (int, float)) and value < 0:
                raise ValueError(
                    "Negative values are not allowed!"
                )

        return func(*args, **kwargs)

    return wrapper


# =========================================================
# Multiple Decorators Example
# =========================================================
@log_decorator
@execution_time
def process_data():
    time.sleep(1)
    print("Processing data...")


# =========================================================
# Authentication Example
# =========================================================
@authenticate
def view_dashboard(user):
    print(f"Welcome {user['name']} to Dashboard")


# =========================================================
# Retry Example
# =========================================================
counter = 0

@retry(max_attempts=3)
def unstable_service():
    global counter
    counter += 1

    if counter < 3:
        raise ConnectionError("Service unavailable")

    return "Service Connected"


# =========================================================
# Cache Example
# =========================================================
@cache_result
def fibonacci(n):

    if n <= 1:
        return n

    return fibonacci(n - 1) + fibonacci(n - 2)


# =========================================================
# Validation Example
# =========================================================
@validate_positive
def calculate_square(num):
    return num * num


# =========================================================
# Combined Enterprise Example
# =========================================================
@log_decorator
@execution_time
@validate_positive
def calculate_salary(hours, rate):
    time.sleep(1)
    return hours * rate


# =========================================================
# Main Program
# =========================================================
if __name__ == "__main__":

    print("\n=== Logging + Execution Time ===")
    process_data()

    print("\n=== Authentication ===")

    user = {
        "name": "Suresh",
        "authenticated": True
    }

    view_dashboard(user)

    print("\n=== Retry ===")
    print(unstable_service())

    print("\n=== Cache ===")
    print(fibonacci(10))

    print("\nSecond Call:")
    print(fibonacci(10))

    print("\n=== Validation ===")
    print(calculate_square(5))

    print("\n=== Multiple Decorators ===")
    salary = calculate_salary(8, 1000)
    print("Salary:", salary)