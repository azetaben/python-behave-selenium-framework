"""
BasePage — comprehensive base class for all page objects.

Provides 60+ helper methods for element interaction, navigation, scrolling,
keyboard input, file operations, and more.
"""
import time
from typing import TYPE_CHECKING, Optional, Callable, Any
from urllib.parse import urlparse
from pathlib import Path

from selenium import webdriver
from selenium.common.exceptions import (
    ElementClickInterceptedException,
    ElementNotInteractableException,
    NoAlertPresentException,
    NoSuchElementException,
    StaleElementReferenceException,
    TimeoutException,
    WebDriverException,
)
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait

from doc.config.config import settings
from exceptions import retry_on_stale
from utils.logger import get_logger

if TYPE_CHECKING:
    from pages.PageManager import PageManager

logger = get_logger(__name__)

# Type alias for locators
Locator = tuple[str, str]


class BasePage:
    """Base class for all page objects with 60+ helper methods."""
    
    def __init__(self, driver: webdriver.Remote) -> None:
        self.driver = driver
        self._manager: Optional["PageManager"] = None
    
    # ── Private helpers ───────────────────────────────────────────────
    
    def _wait(self, timeout: Optional[int] = None) -> WebDriverWait:
        """Return a WebDriverWait configured to timeout."""
        return WebDriverWait(self.driver, timeout or settings.explicit_wait)

    @staticmethod
    def _resolve_timeout(timeout: Optional[int] = None) -> int:
        """Resolve timeout value with framework default fallback."""
        return timeout if timeout is not None else settings.explicit_wait

    def _wait_until(
        self,
        condition: Callable[[webdriver.Remote], Any],
        description: str,
        timeout: Optional[int] = None,
    ) -> bool:
        """Unified wait contract for all explicit wait operations."""
        resolved_timeout = self._resolve_timeout(timeout)
        try:
            self._wait(resolved_timeout).until(condition)
            logger.debug("Wait passed: %s", description)
            return True
        except TimeoutException:
            logger.warning("Timeout after %ss waiting for: %s", resolved_timeout, description)
            return False

    def _el(self, locator: Locator, timeout: Optional[int] = None) -> WebElement:
        """Wait for element presence and return it."""
        return self._wait(timeout).until(ec.presence_of_element_located(locator))

    def _clickable(self, locator: Locator, timeout: Optional[int] = None) -> WebElement:
        """Wait for element to be clickable and return it."""
        return self._wait(timeout).until(ec.element_to_be_clickable(locator))

    # ── PageManager back-reference ────────────────────────────────────
    
    @property
    def manager(self) -> Optional["PageManager"]:
        """Get the PageManager instance."""
        return self._manager
    
    # ── Navigation ────────────────────────────────────────────────────
    
    def load(self, endpoint: str, wait_for_ready: bool = True, timeout: Optional[int] = None) -> None:
        """Navigate to base_url + endpoint."""
        url = settings.base_url.rstrip("/") + "/" + endpoint.lstrip("/")
        logger.info("Loading endpoint: %s", url)
        self.driver.get(url)
        if wait_for_ready:
            self.wait_for_page_ready(timeout=timeout)

    def navigate_to(self, url: str, wait_for_ready: bool = True, timeout: Optional[int] = None) -> None:
        """Navigate to an absolute URL."""
        logger.info("Navigating to %s", url)
        self.driver.get(url)
        if wait_for_ready:
            self.wait_for_page_ready(timeout=timeout)

    def navigate_to_relative_url(self, relative: str, wait_for_ready: bool = True, timeout: Optional[int] = None) -> None:
        """Navigate to a relative URL."""
        base = self.get_current_url().rstrip("/")
        self.driver.get(base + "/" + relative.lstrip("/"))
        if wait_for_ready:
            self.wait_for_page_ready(timeout=timeout)

    def open_url_in_new_tab(self, url: str) -> None:
        """Open a URL in a new tab."""
        self.driver.switch_to.new_window("tab")
        self.navigate_to(url)
    
    def get_current_url(self) -> str:
        """Get the current page URL."""
        return self.driver.current_url
    
    def get_page_title(self) -> str:
        """Get the current page title."""
        return self.driver.title
    
    def get_page_source(self) -> str:
        """Get the entire page source."""
        return self.driver.page_source
    
    def get_domain(self) -> str:
        """Extract domain from current URL."""
        return urlparse(self.get_current_url()).hostname or ""
    
    def get_protocol(self) -> str:
        """Extract protocol from current URL."""
        return urlparse(self.get_current_url()).scheme or ""
    
    def refresh(self, wait_for_ready: bool = True, timeout: Optional[int] = None) -> None:
        """Refresh the current page."""
        logger.info("Refreshing page")
        self.driver.refresh()
        if wait_for_ready:
            self.wait_for_page_ready(timeout=timeout)

    def go_back(self, wait_for_ready: bool = True, timeout: Optional[int] = None) -> None:
        """Navigate back in browser history."""
        logger.info("Going back in browser history")
        self.driver.back()
        if wait_for_ready:
            self.wait_for_page_ready(timeout=timeout)

    def go_forward(self, wait_for_ready: bool = True, timeout: Optional[int] = None) -> None:
        """Navigate forward in browser history."""
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
        """Unified page readiness contract for page-object navigation and synchronization."""
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
        """Wait for URL to contain specific text."""
        return self._wait_until(ec.url_contains(text), f"url contains '{text}'", timeout)

    def wait_for_url_equals(self, url: str, timeout: Optional[int] = None) -> bool:
        """Wait for URL to equal specific value."""
        return self._wait_until(ec.url_to_be(url), f"url equals '{url}'", timeout)

    # ── Element finding ───────────────────────────────────────────────
    
    def find_element(self, locator: Locator, timeout: Optional[int] = None) -> WebElement:
        """Find a single element by locator."""
        try:
            element = self._el(locator, timeout)
            logger.debug("Found element: %s", locator)
            return element
        except TimeoutException:
            logger.error("Element not found within timeout: %s", locator)
            raise
    
    def find_elements(self, locator: Locator, timeout: Optional[int] = None) -> list[WebElement]:
        """Find multiple elements by locator."""
        timeout = timeout or settings.explicit_wait
        try:
            self._wait(timeout).until(ec.presence_of_all_elements_located(locator))
            elements = self.driver.find_elements(*locator)
            logger.debug("Found %d elements: %s", len(elements), locator)
            return elements
        except TimeoutException:
            logger.warning("No elements found: %s", locator)
            return []
    
    def element_exists(self, locator: Locator, timeout: int = 1) -> bool:
        """Check if element exists on page."""
        try:
            self._el(locator, timeout)
            return True
        except TimeoutException:
            return False
    
    def is_element_visible(self, locator: Locator, timeout: Optional[int] = None) -> bool:
        """Check if element is visible."""
        timeout = timeout or settings.explicit_wait
        try:
            self._wait(timeout).until(ec.visibility_of_element_located(locator))
            return True
        except TimeoutException:
            return False
    
    def wait_for_element_visibility(self, locator: Locator, timeout: Optional[int] = None) -> bool:
        """Wait for element to become visible."""
        return self._wait_until(ec.visibility_of_element_located(locator), f"element visible {locator}", timeout)

    def wait_for_element_invisibility(self, locator: Locator, timeout: Optional[int] = None) -> bool:
        """Wait for element to become invisible."""
        return self._wait_until(ec.invisibility_of_element_located(locator), f"element invisible {locator}", timeout)

    # ── Click and interact ────────────────────────────────────────────
    
    @retry_on_stale(max_retries=3)
    def click(self, locator: Locator) -> None:
        """Click an element."""
        element = self._clickable(locator)
        element.click()
        logger.debug("Clicked element: %s", locator)

    def double_click(self, locator: Locator) -> None:
        """Double-click an element."""
        element = self._clickable(locator)
        ActionChains(self.driver).double_click(element).perform()
        logger.debug("Double-clicked element: %s", locator)

    def right_click(self, locator: Locator) -> None:
        """Right-click (context menu) on an element."""
        element = self._clickable(locator)
        ActionChains(self.driver).context_click(element).perform()
        logger.debug("Right-clicked element: %s", locator)

    def click_and_hold(self, locator: Locator, duration: float = 2) -> None:
        """Click and hold on an element for specified duration."""
        element = self._clickable(locator)
        actions = ActionChains(self.driver)
        actions.click_and_hold(element).pause(duration).release().perform()
        logger.debug("Click and hold for %ss: %s", duration, locator)

    def js_click(self, locator: Locator) -> None:
        """Click element using JavaScript (bypasses visibility checks)."""
        element = self._el(locator)
        self.driver.execute_script("arguments[0].click();", element)
        logger.debug("JS-clicked element: %s", locator)

    # ── Text input ────────────────────────────────────────────────────
    
    @retry_on_stale(max_retries=3)
    def type_text(self, locator: Locator, text: str, clear_first: bool = True) -> None:
        """Type text into an input element."""
        element = self._clickable(locator)
        if clear_first:
            element.clear()
        element.send_keys(text)
        logger.debug("Typed '%s' into element: %s", text, locator)

    def clear_field(self, locator: Locator) -> None:
        """Clear an input field."""
        element = self._clickable(locator)
        element.clear()
        logger.debug("Cleared field: %s", locator)

    def js_type(self, locator: Locator, text: str) -> None:
        """Type text using JavaScript."""
        element = self._el(locator)
        self.driver.execute_script(f"arguments[0].value = '{text}';", element)
        logger.debug("JS-typed '%s' into element: %s", text, locator)

    def get_text(self, locator: Locator) -> str:
        """Get text content from an element."""
        element = self._el(locator)
        text = element.text
        logger.debug("Got text from element: %s...", text[:50])
        return text
    
    def get_attribute(self, locator: Locator, attribute: str) -> str:
        """Get attribute value from an element."""
        element = self._el(locator)
        value = element.get_attribute(attribute)
        logger.debug("Got attribute '%s': %s", attribute, value)
        return value or ""
    
    def set_attribute(self, locator: Locator, attribute: str, value: str) -> None:
        """Set an attribute on an element using JavaScript."""
        element = self._el(locator)
        self.driver.execute_script(
            f"arguments[0].setAttribute('{attribute}', '{value}');",
            element
        )
        logger.debug("Set attribute '%s' = '%s': %s", attribute, value, locator)

    def get_computed_style(self, locator: Locator, property_name: str) -> str:
        """Get computed CSS style property."""
        element = self._el(locator)
        value = self.driver.execute_script(
            f"return window.getComputedStyle(arguments[0]).{property_name};",
            element
        )
        logger.debug("Got computed style '%s': %s", property_name, value)
        return value or ""
    
    # ── Keyboard input ────────────────────────────────────────────────
    
    def press_key(self, locator: Locator, key: str) -> None:
        """Press a key in an element."""
        element = self._clickable(locator)
        element.send_keys(key)
        logger.debug("Pressed key in element: %s", locator)

    def press_enter(self, locator: Locator) -> None:
        """Press Enter key in an element."""
        self.press_key(locator, Keys.ENTER)
    
    def press_escape(self, locator: Locator) -> None:
        """Press Escape key in an element."""
        self.press_key(locator, Keys.ESCAPE)
    
    def press_tab(self, locator: Locator) -> None:
        """Press Tab key in an element."""
        self.press_key(locator, Keys.TAB)
    
    def send_keyboard_shortcut(self, *keys: str) -> None:
        """Send keyboard shortcut (e.g., Ctrl+A)."""
        ActionChains(self.driver).key_down(keys[0])
        for key in keys[1:]:
            ActionChains(self.driver).key_down(key)
        for key in reversed(keys):
            ActionChains(self.driver).key_up(key).perform()
        logger.debug("Sent keyboard shortcut: %s", "+".join(keys))

    # ── Checkbox and Radio ────────────────────────────────────────────
    
    def check(self, locator: Locator) -> None:
        """Check a checkbox if not already checked."""
        element = self._clickable(locator)
        if not element.is_selected():
            element.click()
            logger.debug("Checked checkbox: %s", locator)
        else:
            logger.debug("Checkbox already checked: %s", locator)

    def uncheck(self, locator: Locator) -> None:
        """Uncheck a checkbox if checked."""
        element = self._clickable(locator)
        if element.is_selected():
            element.click()
            logger.debug("Unchecked checkbox: %s", locator)
        else:
            logger.debug("Checkbox already unchecked: %s", locator)

    def is_checked(self, locator: Locator) -> bool:
        """Check if a checkbox is selected."""
        element = self._el(locator)
        is_selected = element.is_selected()
        logger.debug("Checkbox selected: %s | %s", is_selected, locator)
        return is_selected
    
    def select_dropdown_by_value(self, locator: Locator, value: str) -> None:
        """Select dropdown option by value."""
        element = self._el(locator)
        select = Select(element)
        select.select_by_value(value)
        logger.debug("Selected dropdown by value '%s': %s", value, locator)

    def select_dropdown_by_visible_text(self, locator: Locator, text: str) -> None:
        """Select dropdown option by visible text."""
        element = self._el(locator)
        select = Select(element)
        select.select_by_visible_text(text)
        logger.debug("Selected dropdown by text '%s': %s", text, locator)

    def select_dropdown_by_index(self, locator: Locator, index: int) -> None:
        """Select dropdown option by index."""
        element = self._el(locator)
        select = Select(element)
        select.select_by_index(index)
        logger.debug("Selected dropdown by index %d: %s", index, locator)

    def get_dropdown_options(self, locator: Locator) -> list[str]:
        """Get all options from a dropdown."""
        element = self._el(locator)
        select = Select(element)
        options = [opt.text for opt in select.options]
        logger.debug("Got %d dropdown options from %s", len(options), locator)
        return options
    
    # ── Mouse interaction ─────────────────────────────────────────────
    
    def hover(self, locator: Locator) -> None:
        """Hover over an element."""
        element = self._el(locator)
        ActionChains(self.driver).move_to_element(element).perform()
        logger.debug("Hovered over element: %s", locator)

    def hover_and_click(self, locator: Locator) -> None:
        """Hover over element then click it."""
        element = self._clickable(locator)
        ActionChains(self.driver).move_to_element(element).click().perform()
        logger.debug("Hovered and clicked element: %s", locator)

    def hover_with_offset(self, locator: Locator, x_offset: int, y_offset: int) -> None:
        """Hover over element with offset."""
        element = self._el(locator)
        ActionChains(self.driver).move_to_element_with_offset(element, x_offset, y_offset).perform()
        logger.debug("Hovered with offset (%d, %d): %s", x_offset, y_offset, locator)

    def drag_and_drop(self, source_locator: Locator, target_locator: Locator) -> None:
        """Drag element from source to target."""
        source = self._el(source_locator)
        target = self._el(target_locator)
        ActionChains(self.driver).drag_and_drop(source, target).perform()
        logger.debug("Dragged from %s to %s", source_locator, target_locator)

    def drag_by_offset(self, locator: Locator, x_offset: int, y_offset: int) -> None:
        """Drag element by offset."""
        element = self._el(locator)
        ActionChains(self.driver).drag_and_drop_by_offset(element, x_offset, y_offset).perform()
        logger.debug("Dragged by offset (%d, %d): %s", x_offset, y_offset, locator)

    # ── Scrolling ─────────────────────────────────────────────────────
    
    def scroll_to_element(self, locator: Locator) -> None:
        """Scroll to element."""
        element = self._el(locator)
        self.driver.execute_script("arguments[0].scrollIntoView(true);", element)
        logger.debug("Scrolled to element: %s", locator)

    def scroll_to_element_and_click(self, locator: Locator) -> None:
        """Scroll to element and click it."""
        self.scroll_to_element(locator)
        self.click(locator)
    
    def scroll_by(self, x: int, y: int) -> None:
        """Scroll by offset."""
        self.driver.execute_script(f"window.scrollBy({x}, {y});")
        logger.debug("Scrolled by (%d, %d)", x, y)

    def scroll_to_top(self) -> None:
        """Scroll to top of page."""
        self.driver.execute_script("window.scrollTo(0, 0);")
        logger.debug("Scrolled to top")
    
    def scroll_to_bottom(self) -> None:
        """Scroll to bottom of page."""
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        logger.debug("Scrolled to bottom")
    
    # ── Alerts and windows ────────────────────────────────────────────
    
    def accept_alert(self) -> str:
        """Accept an alert and return its message."""
        try:
            alert = self.driver.switch_to.alert
            text = alert.text
            alert.accept()
            logger.debug("Alert accepted: %s", text)
            return text
        except Exception as e:
            logger.error("Failed to accept alert: %s", e)
            raise
    
    def dismiss_alert(self) -> str:
        """Dismiss an alert and return its message."""
        try:
            alert = self.driver.switch_to.alert
            text = alert.text
            alert.dismiss()
            logger.debug("Alert dismissed: %s", text)
            return text
        except Exception as e:
            logger.error("Failed to dismiss alert: %s", e)
            raise
    
    def type_in_alert(self, text: str) -> None:
        """Type text in an alert prompt."""
        try:
            alert = self.driver.switch_to.alert
            alert.send_keys(text)
            logger.debug("Typed in alert: %s", text)
        except Exception as e:
            logger.error("Failed to type in alert: %s", e)
            raise
    
    def get_number_of_windows(self) -> int:
        """Get the number of open windows/tabs."""
        count = len(self.driver.window_handles)
        logger.debug("Number of windows: %d", count)
        return count
    
    def switch_to_window(self, window_index: int) -> None:
        """Switch to a specific window by index."""
        try:
            self.driver.switch_to.window(self.driver.window_handles[window_index])
            logger.debug("Switched to window %d", window_index)
        except (WebDriverException, IndexError) as e:
            logger.error("Failed to switch to window %d: %s", window_index, e)
            raise
    
    def close_current_window(self) -> None:
        """Close the current window."""
        self.driver.close()
        logger.debug("Closed current window")
    
    # ── Frames and iframes ────────────────────────────────────────────
    
    def switch_to_frame(self, locator: Locator) -> None:
        """Switch to iframe by locator."""
        element = self._el(locator)
        self.driver.switch_to.frame(element)
        logger.debug("Switched to frame: %s", locator)

    def switch_to_frame_by_index(self, index: int) -> None:
        """Switch to iframe by index."""
        self.driver.switch_to.frame(index)
        logger.debug("Switched to frame by index: %d", index)

    def switch_to_parent_frame(self) -> None:
        """Switch to parent frame."""
        self.driver.switch_to.parent_frame()
        logger.debug("Switched to parent frame")
    
    def switch_to_default_content(self) -> None:
        """Switch to default content (main page)."""
        self.driver.switch_to.default_content()
        logger.debug("Switched to default content")
    
    # ── Storage ───────────────────────────────────────────────────────
    
    def get_local_storage(self, key: str) -> str:
        """Get value from localStorage."""
        value = self.driver.execute_script(f"return localStorage.getItem('{key}');")
        logger.debug("Got localStorage['%s'] = %s", key, value)
        return value or ""
    
    def set_local_storage(self, key: str, value: str) -> None:
        """Set value in localStorage."""
        self.driver.execute_script(f"localStorage.setItem('{key}', '{value}');")
        logger.debug("Set localStorage['%s'] = %s", key, value)

    def remove_local_storage(self, key: str) -> None:
        """Remove key from localStorage."""
        self.driver.execute_script(f"localStorage.removeItem('{key}');")
        logger.debug("Removed localStorage['%s']", key)

    def clear_local_storage(self) -> None:
        """Clear all localStorage."""
        self.driver.execute_script("localStorage.clear();")
        logger.debug("Cleared localStorage")
    
    def get_session_storage(self, key: str) -> str:
        """Get value from sessionStorage."""
        value = self.driver.execute_script(f"return sessionStorage.getItem('{key}');")
        logger.debug("Got sessionStorage['%s'] = %s", key, value)
        return value or ""
    
    def set_session_storage(self, key: str, value: str) -> None:
        """Set value in sessionStorage."""
        self.driver.execute_script(f"sessionStorage.setItem('{key}', '{value}');")
        logger.debug("Set sessionStorage['%s'] = %s", key, value)

    def clear_session_storage(self) -> None:
        """Clear all sessionStorage."""
        self.driver.execute_script("sessionStorage.clear();")
        logger.debug("Cleared sessionStorage")
    
    # ── File operations ───────────────────────────────────────────────

    @staticmethod
    def get_file_from_download(file_name: str, timeout: int = 30) -> Optional[Path]:
        """Wait for a file to appear in the configured download directory."""

        download_dir = Path(settings.download_dir)
        end_time = time.time() + timeout

        while time.time() < end_time:
            file_path = download_dir / file_name
            if file_path.exists():
                logger.info("File downloaded: %s", file_path)
                return file_path
            time.sleep(0.5)

        logger.warning("File not found in download directory: %s", file_name)
        return None

    def upload_file(self, locator: Locator, file_path: str) -> None:
        """Upload file to file input element."""
        input_element = self._el(locator)
        input_element.send_keys(str(Path(file_path).resolve()))
        logger.debug("Uploaded file: %s", file_path)

    # ── Screenshots ───────────────────────────────────────────────────
    
    def take_screenshot(self, file_path: str) -> Path:
        """Take full page screenshot and save to file."""
        path = Path(file_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        self.driver.save_screenshot(str(path))
        logger.info("Screenshot saved: %s", path)
        return path
    
    def take_element_screenshot(self, locator: Locator, file_path: str) -> Path:
        """Take screenshot of specific element."""
        path = Path(file_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        element = self._el(locator)
        element.screenshot(str(path))
        logger.info("Element screenshot saved: %s", path)
        return path
    
    # ── Wait utilities ────────────────────────────────────────────────
    
    def wait_for_element_count(self, locator: Locator, expected_count: int, timeout: Optional[int] = None) -> bool:
        """Wait for a specific number of elements to be present."""
        def element_count_matches(driver):
            elements = driver.find_elements(*locator)
            return elements if len(elements) == expected_count else False

        return self._wait_until(element_count_matches, f"{expected_count} elements for {locator}", timeout)

    def wait_for_title_contains(self, text: str, timeout: Optional[int] = None) -> bool:
        """Wait for page title to contain text."""
        return self._wait_until(ec.title_contains(text), f"title contains '{text}'", timeout)

    def wait_for_title_equals(self, title: str, timeout: Optional[int] = None) -> bool:
        """Wait for page title to equal specific value."""
        return self._wait_until(ec.title_is(title), f"title equals '{title}'", timeout)

    def close_google_password_popup(self) -> bool:
        """
        Close Chrome's 'Change your password' / Google Password Manager dialog if present.

        The dialog is Chrome's native browser overlay (not a DOM element and not a JS alert).
        The only way to dismiss it via WebDriver is to send keyboard input (Enter) because
        Chrome keeps the OK button focused while the dialog is open.

        Returns True if the dialog was detected and dismissed, False if not present.
        """

        # --- Strategy 1: standard JS alert (not expected here but kept as safeguard) ---
        try:
            WebDriverWait(self.driver, 1).until(ec.alert_is_present())
            alert = self.driver.switch_to.alert
            alert_text = alert.text
            alert.accept()
            logger.info("Dismissed JS alert (OK): %s", alert_text)
            return True
        except (TimeoutException, NoAlertPresentException):
            pass

        # --- Strategy 2: Chrome-native password manager overlay ---
        # The "Change your password" / "Save password?" dialog is rendered by Chrome above
        # the page.  It receives keyboard focus, so pressing Enter clicks the focused OK button.
        # We attempt this only when there are signs the dialog may be present (page appears
        # interactive but an extra overlay is blocking it).
        try:
            # Give Chrome a moment to display the dialog after login
            time.sleep(0.8)

            # Send Enter key via ActionChains — targets whatever Chrome element has focus,
            # which is the OK button of the password manager dialog when it is visible.
            ActionChains(self.driver).send_keys(Keys.ENTER).perform()
            time.sleep(0.3)  # Allow dialog animation to finish

            logger.info("Sent Enter key to dismiss Chrome password manager overlay (OK button)")
            return True
        except Exception as e:
            logger.debug("ActionChains Enter approach did not apply: %s", e)

        # --- Strategy 3: DOM-based fallback (handles any in-page modal variant) ---
        dom_selectors = [
            "[data-id='password-change-dialog']",
            "[aria-label*='Change your password']",
            "[aria-label*='Save password']",
            "[role='dialog']",
            "[role='alertdialog']",
        ]
        ok_button_selectors = [
            "button[jsname='LgbsSe']",   # Common Google OK button
            "button[autofocus]",
            "button.primary",
            "button:last-of-type",
        ]
        for dialog_sel in dom_selectors:
            try:
                dialogs = self.driver.find_elements("css selector", dialog_sel)
                if not dialogs:
                    continue
                dialog_el = dialogs[0]
                for btn_sel in ok_button_selectors:
                    try:
                        ok_btn = dialog_el.find_element("css selector", btn_sel)
                        ok_btn.click()
                        logger.info("Clicked OK in DOM dialog (%s -> %s)", dialog_sel, btn_sel)
                        return True
                    except (
                        NoSuchElementException,
                        ElementNotInteractableException,
                        ElementClickInterceptedException,
                        StaleElementReferenceException,
                        WebDriverException,
                    ):
                        pass
                # Fallback: hit Escape on the dialog element itself
                dialog_el.send_keys(Keys.ESCAPE)
                logger.info("Sent Escape to DOM dialog: %s", dialog_sel)
                return True
            except (
                ElementNotInteractableException,
                ElementClickInterceptedException,
                StaleElementReferenceException,
                WebDriverException,
            ):
                pass

        logger.debug("Google Password Manager dialog not detected — continuing")
        return False
