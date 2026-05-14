"""Exceptions module for the framework."""

from exceptions.custom import (
    FrameworkError,
    BrowserInitError,
    RemoteConnectionError,
    UnsupportedBrowserError,
    ConfigurationError,
    ElementNotFoundError,
    ElementNotInteractableError,
    PageLoadError,
    NavigationError,
    StaleElementError,
    FileOperationError,
    ScreenshotError,
    PerformanceThresholdError,
)

from exceptions.handlers import (
    retry_on_stale,
    safe_int,
    safe_str,
    safe_bool,
    suppress,
)

__all__ = [
    "FrameworkError",
    "BrowserInitError",
    "RemoteConnectionError",
    "UnsupportedBrowserError",
    "ConfigurationError",
    "ElementNotFoundError",
    "ElementNotInteractableError",
    "PageLoadError",
    "NavigationError",
    "StaleElementError",
    "FileOperationError",
    "ScreenshotError",
    "PerformanceThresholdError",
    "retry_on_stale",
    "safe_int",
    "safe_str",
    "safe_bool",
    "suppress",
]
