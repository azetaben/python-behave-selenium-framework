"""
Custom exception hierarchy for the Behave Selenium Framework.

All framework exceptions inherit from ``FrameworkError``.
"""

from __future__ import annotations

from typing import Any


class FrameworkError(Exception):
    """Base exception for all framework errors with optional structured details."""

    def __init__(self, message: str = "", *, details: Any | None = None) -> None:
        self.message = message
        self.details = details
        super().__init__(message)

    def __str__(self) -> str:
        if self.message and self.details is not None:
            return f"{self.message} | details={self.details}"
        if self.message:
            return self.message
        if self.details is not None:
            return f"details={self.details}"
        return self.__class__.__name__


class BrowserInitError(FrameworkError):
    """Raised when WebDriver initialization fails."""


class RemoteConnectionError(FrameworkError):
    """Raised when connection to Selenium Grid fails."""


class UnsupportedBrowserError(FrameworkError):
    """Raised when an unsupported browser type is requested."""


class ConfigurationError(FrameworkError):
    """Raised when configuration is missing or invalid."""


class ElementNotFoundError(FrameworkError):
    """Raised when an element cannot be found within timeout."""


class ElementNotInteractableError(FrameworkError):
    """Raised when an element cannot be interacted with."""


class PageLoadError(FrameworkError):
    """Raised when a page does not load within the expected time."""


class NavigationError(FrameworkError):
    """Raised when navigation to a URL fails."""


class StaleElementError(FrameworkError):
    """Raised when a stale element is encountered after all retries."""


class FileOperationError(FrameworkError):
    """Raised when a file operation fails."""


class ScreenshotError(FrameworkError):
    """Raised when screenshot capture fails."""


class PerformanceThresholdError(FrameworkError):
    """Raised when an operation exceeds the performance threshold."""


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
]
