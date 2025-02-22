import asyncio
import functools
import time
from typing import Any, Callable, TypeVar

T = TypeVar("T", bound=Callable[..., Any])


def timed_async(name: str = "") -> Callable[[T], T]:
    """Decorator for timing async functions."""

    def decorator(func: T) -> T:
        @functools.wraps(func)
        async def wrapper(*args: Any, **kwargs: Any) -> Any:
            start_time = asyncio.get_event_loop().time()
            try:
                result = await func(*args, **kwargs)
                return result
            finally:
                end_time = asyncio.get_event_loop().time()
                operation_name = name or func.__name__
                print(f"{operation_name} took {end_time - start_time:.2f} seconds")

        return wrapper  # type: ignore

    return decorator


def timed_sync(name: str = "") -> Callable[[T], T]:
    """Decorator for timing synchronous functions."""

    def decorator(func: T) -> T:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            start_time = time.time()
            try:
                result = func(*args, **kwargs)
                return result
            finally:
                end_time = time.time()
                operation_name = name or func.__name__
                print(f"{operation_name} took {end_time - start_time:.2f} seconds")

        return wrapper  # type: ignore

    return decorator
