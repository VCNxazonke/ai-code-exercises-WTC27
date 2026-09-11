"""
Activity 3: Understanding Language Feature - Python Decorators
Demonstrates custom decorators, execution timing, and argument type validation.
"""

import time
import functools
from typing import Callable, Any


def log_execution_time(func: Callable[..., Any]) -> Callable[..., Any]:
    """
    Decorator that logs function execution time and arguments.
    Demonstrates higher-order functions, closures, and functools.wraps.
    """
    @functools.wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        start_time = time.perf_counter()
        result = func(*args, **kwargs)
        elapsed = (time.perf_counter() - start_time) * 1000
        print(f"[LOG] {func.__name__} executed in {elapsed:.4f} ms")
        return result
    return wrapper


def validate_positive_args(func: Callable[..., Any]) -> Callable[..., Any]:
    """
    Decorator that enforces positive numerical arguments.
    """
    @functools.wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        for arg in args:
            if isinstance(arg, (int, float)) and arg <= 0:
                raise ValueError(f"Argument {arg} must be positive.")
        return func(*args, **kwargs)
    return wrapper


@log_execution_time
@validate_positive_args
def calculate_compound_interest(principal: float, rate: float, years: int) -> float:
    """Calculates compound interest for positive financial parameters."""
    time.sleep(0.01)  # Simulate small calculation delay
    return principal * ((1 + rate) ** years)


if __name__ == "__main__":
    print("Testing valid input:")
    amount = calculate_compound_interest(1000.0, 0.05, 5)
    print(f"Final Amount: ${amount:.2f}\n")

    print("Testing invalid input validation:")
    try:
        calculate_compound_interest(-500.0, 0.05, 3)
    except ValueError as err:
        print(f"Caught expected error: {err}")
