"""
Exception handlers and decorators for safer operations.

Includes retry_on_stale decorator and safe value extraction helpers.
"""
import functools
import logging
from typing import Callable, TypeVar, Any

from selenium.common.exceptions import (
    StaleElementReferenceException,
    WebDriverException,
)

from exceptions.custom import StaleElementError

logger = logging.getLogger(__name__)

T = TypeVar('T')


def retry_on_stale(max_retries: int = 3) -> Callable:
    """
    Decorator to retry a method if StaleElementReferenceException is raised.
    
    Args:
        max_retries: Maximum number of retry attempts
        
    Returns:
        Decorator function
    """
    def decorator(func: Callable[..., T]) -> Callable[..., T]:
        @functools.wraps(func)
        def wrapper(*args, **kwargs) -> T:
            last_exception = None
            for attempt in range(1, max_retries + 1):
                try:
                    return func(*args, **kwargs)
                except StaleElementReferenceException as e:
                    last_exception = e
                    if attempt < max_retries:
                        logger.debug(
                            f"Stale element in {func.__name__}, retrying... "
                            f"(attempt {attempt}/{max_retries})"
                        )
                    else:
                        logger.error(
                            f"Stale element in {func.__name__} after {max_retries} retries"
                        )
            
            # All retries exhausted
            raise StaleElementError(
                f"Element became stale after {max_retries} retries in {func.__name__}"
            ) from last_exception
        
        return wrapper
    return decorator


def safe_int(func: Callable[[], Any], default: int = 0) -> int:
    """
    Safely extract an integer from a function call.
    
    Args:
        func: Callable that returns an integer-convertible value
        default: Default value if extraction fails
        
    Returns:
        Integer value or default
    """
    try:
        return int(func())
    except (WebDriverException, ValueError, TypeError, AttributeError) as e:
        logger.debug(f"Failed to extract int: {str(e)}")
        return default


def safe_str(func: Callable[[], Any], default: str = "") -> str:
    """
    Safely extract a string from a function call.
    
    Args:
        func: Callable that returns a string-convertible value
        default: Default value if extraction fails
        
    Returns:
        String value or default
    """
    try:
        return str(func())
    except (WebDriverException, ValueError, TypeError, AttributeError) as e:
        logger.debug(f"Failed to extract str: {str(e)}")
        return default


def safe_bool(func: Callable[[], Any], default: bool = False) -> bool:
    """
    Safely extract a boolean from a function call.
    
    Args:
        func: Callable that returns a boolean-convertible value
        default: Default value if extraction fails
        
    Returns:
        Boolean value or default
    """
    try:
        result = func()
        if isinstance(result, bool):
            return result
        return bool(result)
    except (WebDriverException, ValueError, TypeError, AttributeError) as e:
        logger.debug(f"Failed to extract bool: {str(e)}")
        return default


class suppress:
    """
    Context manager to suppress and log specific exceptions.
    
    Similar to contextlib.suppress but logs at DEBUG level.
    
    Usage:
        with suppress(TimeoutException):
            page.wait_for_element(locator)
    """
    
    def __init__(self, *exceptions: type[Exception]) -> None:
        self.exceptions = exceptions
    
    def __enter__(self) -> None:
        return self
    
    def __exit__(self, exctype, excinst, exctb) -> bool:
        if exctype is None:
            return False
        
        if issubclass(exctype, self.exceptions):
            logger.debug(f"Suppressed exception: {exctype.__name__}: {str(excinst)}")
            return True
        
        return False
