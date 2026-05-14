"""Navigation and page readiness helpers for page objects."""

from typing import Optional, TypeAlias
from urllib.parse import urljoin, urlparse

from selenium.webdriver.support import expected_conditions as ec

from core.page_contract import PageContract
from utils.logger import get_logger

logger = get_logger(__name__)

Locator: TypeAlias = tuple[str, str]


class PageNavigationMixin(PageContract):
    """Shared navigation and page readiness operations."""

    def load(self, endpoint: str, wait_for_ready: bool = True, timeout: Optional[int] = None) -> None:
        base_url = self.settings.base_url.rstrip("/") + "/"
        url = urljoin(base_url, endpoint.lstrip("/"))
        logger.info("Loading endpoint: %s", url)
        self.driver.get(url)
        if wait_for_ready:
            self.wait_for_page_ready(timeout=timeout)

    def navigate_to(self, url: str, wait_for_ready: bool = True, timeout: Optional[int] = None) -> None:
        logger.info("Navigating to %s", url)
        self.driver.get(url)
        if wait_for_ready:
            self.wait_for_page_ready(timeout=timeout)

    def navigate_to_relative_url(self, relative: str, wait_for_ready: bool = True, timeout: Optional[int] = None) -> None:
        current_url = self.get_current_url().rstrip("/") + "/"
        url = urljoin(current_url, relative.lstrip("/"))
        logger.info("Navigating to relative URL: %s", url)
        self.driver.get(url)
        if wait_for_ready:
            self.wait_for_page_ready(timeout=timeout)

    def open_url_in_new_tab(self, url: str, wait_for_ready: bool = True, timeout: Optional[int] = None) -> None:
        self.driver.switch_to.new_window("tab")
        self.navigate_to(url, wait_for_ready=wait_for_ready, timeout=timeout)

    def get_current_url(self) -> str:
        return self.driver.current_url

    def get_page_title(self) -> str:
        return self.driver.title

    def get_page_source(self) -> str:
        return self.driver.page_source

    def get_domain(self) -> str:
        return urlparse(self.get_current_url()).hostname or ""

    def get_protocol(self) -> str:
        return urlparse(self.get_current_url()).scheme or ""

    def refresh(self, wait_for_ready: bool = True, timeout: Optional[int] = None) -> None:
        logger.info("Refreshing page")
        self.driver.refresh()
        if wait_for_ready:
            self.wait_for_page_ready(timeout=timeout)

    def go_back(self, wait_for_ready: bool = True, timeout: Optional[int] = None) -> None:
        logger.info("Going back in browser history")
        self.driver.back()
        if wait_for_ready:
            self.wait_for_page_ready(timeout=timeout)

    def go_forward(self, wait_for_ready: bool = True, timeout: Optional[int] = None) -> None:
        logger.info("Going forward in browser history")
        self.driver.forward()
        if wait_for_ready:
            self.wait_for_page_ready(timeout=timeout)

    def wait_for_page_ready(
        self,
        timeout: Optional[int] = None,
        url_contains: Optional[str] = None,
        url_equals: Optional[str] = None,
        title_contains: Optional[str] = None,
        title_equals: Optional[str] = None,
        visible_locator: Optional[Locator] = None,
    ) -> bool:
        if not self._wait_until(
            lambda d: d.execute_script("return document.readyState") == "complete",
            "document readyState == complete",
            timeout,
        ):
            return False

        if url_contains and not self._wait_until(ec.url_contains(url_contains), f"url contains '{url_contains}'", timeout):
            return False
        if url_equals and not self._wait_until(ec.url_to_be(url_equals), f"url equals '{url_equals}'", timeout):
            return False
        if title_contains and not self._wait_until(ec.title_contains(title_contains), f"title contains '{title_contains}'", timeout):
            return False
        if title_equals and not self._wait_until(ec.title_is(title_equals), f"title equals '{title_equals}'", timeout):
            return False
        if visible_locator and not self._wait_until(
            ec.visibility_of_element_located(visible_locator),
            f"visible locator {visible_locator}",
            timeout,
        ):
            return False

        return True

    def wait_for_url_contains(self, text: str, timeout: Optional[int] = None) -> bool:
        return self._wait_until(ec.url_contains(text), f"url contains '{text}'", timeout)

    def wait_for_url_equals(self, url: str, timeout: Optional[int] = None) -> bool:
        return self._wait_until(ec.url_to_be(url), f"url equals '{url}'", timeout)

    def wait_for_title_contains(self, text: str, timeout: Optional[int] = None) -> bool:
        return self._wait_until(ec.title_contains(text), f"title contains '{text}'", timeout)

    def wait_for_title_equals(self, title: str, timeout: Optional[int] = None) -> bool:
        return self._wait_until(ec.title_is(title), f"title equals '{title}'", timeout)

