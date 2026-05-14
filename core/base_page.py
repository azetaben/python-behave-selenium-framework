"""
BasePage for page objects.

Provides shared driver state, timeout helpers, and composition over the focused
navigation, element, interaction, and browser-context mixins.
"""

from __future__ import annotations

from typing import Any, Callable, Optional, TYPE_CHECKING

from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait

from config.config import settings as framework_settings
from core.page_context_mixin import PageContextMixin
from core.page_element_mixin import PageElementMixin
from core.page_interaction_mixin import PageInteractionMixin
from core.page_navigation_mixin import PageNavigationMixin
from utils.logger import get_logger

if TYPE_CHECKING:
    from pages.page_manager import PageManager

logger = get_logger(__name__)


class BasePage(PageNavigationMixin, PageElementMixin, PageInteractionMixin, PageContextMixin):
    """Base class for all page objects."""

    settings = framework_settings

    def __init__(self, driver: webdriver.Remote) -> None:
        self.driver = driver
        self._manager: Optional["PageManager"] = None

    @property
    def manager(self) -> Optional["PageManager"]:
        return self._manager

    def _wait(self, timeout: Optional[int] = None) -> WebDriverWait:
        return WebDriverWait(self.driver, timeout or self.settings.explicit_wait)

    @staticmethod
    def _resolve_timeout(timeout: Optional[int] = None) -> int:
        return timeout if timeout is not None else framework_settings.explicit_wait

    def _wait_until(
        self,
        condition: Callable[[webdriver.Remote], Any],
        description: str,
        timeout: Optional[int] = None,
    ) -> bool:
        resolved_timeout = self._resolve_timeout(timeout)
        try:
            self._wait(resolved_timeout).until(condition)
            logger.debug("Wait passed: %s", description)
            return True
        except TimeoutException:
            logger.warning("Timeout after %ss waiting for: %s", resolved_timeout, description)
            return False

    def is_logo_displayed(self) -> bool:
        logo_locator = getattr(self, "LOGO", None)
        if logo_locator is None:
            logger.debug("%s does not define LOGO locator", self.__class__.__name__)
            return False
        return self.is_element_visible(logo_locator, timeout=3)

