"""Shared typing contract for page mixins.

This class is intentionally lightweight and defines only the members mixins
expect `BasePage` to provide.
"""

from __future__ import annotations

from typing import Any, Callable, Optional

from selenium import webdriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import WebDriverWait


class PageContract:
    """Typed contract used by page mixins for static analysis and readability."""

    driver: webdriver.Remote
    settings: Any

    def _el(self, locator: tuple[str, str], timeout: Optional[int] = None) -> WebElement:
        raise NotImplementedError

    def _clickable(self, locator: tuple[str, str], timeout: Optional[int] = None) -> WebElement:
        raise NotImplementedError

    def _wait(self, timeout: Optional[int] = None) -> WebDriverWait:
        raise NotImplementedError

    @staticmethod
    def _resolve_timeout(timeout: Optional[int] = None) -> int:
        raise NotImplementedError

    def _wait_until(
        self,
        condition: Callable[[webdriver.Remote], Any],
        description: str,
        timeout: Optional[int] = None,
    ) -> bool:
        raise NotImplementedError

