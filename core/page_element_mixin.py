"""Element lookup and read helpers for page objects."""

from typing import Optional, TypeAlias

from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as ec

from core.page_contract import PageContract
from utils.logger import get_logger

logger = get_logger(__name__)

Locator: TypeAlias = tuple[str, str]


class PageElementMixin(PageContract):
    """Shared element lookup and read operations."""

    def _el(self, locator: Locator, timeout: Optional[int] = None) -> WebElement:
        resolved_timeout = self._resolve_timeout(timeout)
        return self._wait(resolved_timeout).until(ec.presence_of_element_located(locator))

    def _clickable(self, locator: Locator, timeout: Optional[int] = None) -> WebElement:
        resolved_timeout = self._resolve_timeout(timeout)
        return self._wait(resolved_timeout).until(ec.element_to_be_clickable(locator))

    def find_element(self, locator: Locator, timeout: Optional[int] = None) -> WebElement:
        try:
            element = self._el(locator, timeout)
            logger.debug("Found element: %s", locator)
            return element
        except TimeoutException:
            logger.error("Element not found within timeout: %s", locator)
            raise

    def find_elements(self, locator: Locator, timeout: Optional[int] = None) -> list[WebElement]:
        resolved_timeout = self._resolve_timeout(timeout)
        try:
            self._wait(resolved_timeout).until(ec.presence_of_all_elements_located(locator))
            elements = self.driver.find_elements(*locator)
            logger.debug("Found %d elements: %s", len(elements), locator)
            return elements
        except TimeoutException:
            logger.warning("No elements found: %s", locator)
            return []

    def element_exists(self, locator: Locator, timeout: int = 1) -> bool:
        try:
            self._el(locator, timeout)
            return True
        except TimeoutException:
            return False

    def is_element_visible(self, locator: Locator, timeout: Optional[int] = None) -> bool:
        resolved_timeout = self._resolve_timeout(timeout)
        try:
            self._wait(resolved_timeout).until(ec.visibility_of_element_located(locator))
            return True
        except TimeoutException:
            return False

    def wait_for_element_visibility(self, locator: Locator, timeout: Optional[int] = None) -> bool:
        return self._wait_until(ec.visibility_of_element_located(locator), f"element visible {locator}", timeout)

    def wait_for_element_invisibility(self, locator: Locator, timeout: Optional[int] = None) -> bool:
        return self._wait_until(ec.invisibility_of_element_located(locator), f"element invisible {locator}", timeout)

    def wait_for_element_count(
        self,
        locator: Locator,
        expected_count: int,
        timeout: Optional[int] = None,
    ) -> bool:
        def element_count_matches(driver: webdriver.Remote):
            elements = driver.find_elements(*locator)
            return elements if len(elements) == expected_count else False

        return self._wait_until(element_count_matches, f"{expected_count} elements for {locator}", timeout)

    def get_text(self, locator: Locator) -> str:
        element = self._el(locator)
        text = element.text
        logger.debug("Got text from element: %s...", text[:50])
        return text

    def get_attribute(self, locator: Locator, attribute: str) -> str:
        element = self._el(locator)
        value = element.get_attribute(attribute)
        logger.debug("Got attribute '%s': %s", attribute, value)
        return value or ""

    def set_attribute(self, locator: Locator, attribute: str, value: str) -> None:
        element = self._el(locator)
        self.driver.execute_script(
            "arguments[0].setAttribute(arguments[1], arguments[2]);",
            element,
            attribute,
            value,
        )
        logger.debug("Set attribute '%s' = '%s': %s", attribute, value, locator)

    def get_computed_style(self, locator: Locator, property_name: str) -> str:
        element = self._el(locator)
        value = self.driver.execute_script(
            "return window.getComputedStyle(arguments[0]).getPropertyValue(arguments[1]);",
            element,
            property_name,
        )
        logger.debug("Got computed style '%s': %s", property_name, value)
        return value or ""

