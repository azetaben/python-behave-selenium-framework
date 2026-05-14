"""Page object for Saucelabs demo app hamburger menu / toggle sidebar.

Covers:
- Sidebar menu navigation (All Items, About, Logout, Reset App State)
- Close menu button
- Presence and visibility verification of menu items
- Clicking menu items by text
"""

from __future__ import annotations

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement

from core.base_page import BasePage
from core.page_element_mixin import Locator
from utils.logger import get_logger

logger = get_logger(__name__)


class TogglePage(BasePage):
    """Page object for the hamburger menu sidebar."""

    # ── Toggle / hamburger trigger ────────────────────────────────────────────
    MENU_BUTTON: Locator = (By.ID, "react-burger-menu-btn")

    # ── Sidebar container ─────────────────────────────────────────────────────
    SIDEBAR_WRAPPER: Locator = (By.CLASS_NAME, "bm-menu-wrap")
    SIDEBAR_MENU: Locator = (By.CLASS_NAME, "bm-menu")
    SIDEBAR_ITEM_LIST: Locator = (By.CLASS_NAME, "bm-item-list")
    MENU_ITEMS: Locator = (By.CSS_SELECTOR, "a.bm-item.menu-item")

    # ── Menu items (by ID and data-test attribute) ────────────────────────────
    ALL_ITEMS_LINK: Locator = (By.ID, "inventory_sidebar_link")
    ABOUT_LINK: Locator = (By.ID, "about_sidebar_link")
    LOGOUT_LINK: Locator = (By.ID, "logout_sidebar_link")
    RESET_APP_LINK: Locator = (By.ID, "reset_sidebar_link")

    # ── Close menu button ─────────────────────────────────────────────────────
    CLOSE_BUTTON: Locator = (By.ID, "react-burger-cross-btn")
    CLOSE_BUTTON_IMG: Locator = (By.CSS_SELECTOR, ".bm-cross")

    # ── Text-based locators for menu items ────────────────────────────────────
    _MENU_ITEMS_BY_TEXT: dict[str, Locator] = {
        "all items": ALL_ITEMS_LINK,
        "about": ABOUT_LINK,
        "logout": LOGOUT_LINK,
        "reset app state": RESET_APP_LINK,
        "close menu": CLOSE_BUTTON,
    }

    # ── All menu item locators ────────────────────────────────────────────────
    _ALL_MENU_ITEMS: list[Locator] = [
        ALL_ITEMS_LINK,
        ABOUT_LINK,
        LOGOUT_LINK,
        RESET_APP_LINK,
    ]

    # ── Public methods ────────────────────────────────────────────────────────

    def is_sidebar_visible(self) -> bool:
        """Check if the sidebar menu is visible."""
        return self.is_element_visible(self.SIDEBAR_WRAPPER)

    def is_menu_button_visible(self) -> bool:
        """Check if the hamburger toggle button is visible."""
        return self.is_element_visible(self.MENU_BUTTON)

    def is_sidebar_displayed(self) -> bool:
        """Check if the sidebar container is displayed."""
        return self.is_element_visible(self.SIDEBAR_WRAPPER)

    def is_menu_item_visible(self, text: str) -> bool:
        """Check if a menu item is visible by its text label (case-insensitive)."""
        locator = self._get_menu_item_locator(text)
        if locator is None:
            logger.warning("Menu item not found: '%s'", text)
            return False
        return self.is_element_visible(locator)

    def is_menu_item_present(self, text: str) -> bool:
        """Check if a menu item is present in the DOM by its text label (case-insensitive)."""
        locator = self._get_menu_item_locator(text)
        if locator is None:
            logger.warning("Menu item not found: '%s'", text)
            return False
        return self.element_exists(locator)

    def is_menu_item_enabled(self, text: str) -> bool:
        """Check if a menu item is enabled (clickable) by its text label (case-insensitive)."""
        locator = self._get_menu_item_locator(text)
        if locator is None:
            logger.warning("Menu item not found: '%s'", text)
            return False
        try:
            element = self.find_element(locator)
            return element.is_enabled()
        except Exception as exc:
            logger.error("Error checking if menu item '%s' is enabled: %s", text, exc)
            return False

    def get_menu_item_text(self, text: str) -> str:
        """Get the text content of a menu item (case-insensitive)."""
        locator = self._get_menu_item_locator(text)
        if locator is None:
            logger.warning("Menu item not found: '%s'", text)
            return ""
        return self.get_text(locator)

    def get_all_menu_items_count(self) -> int:
        """Get the total number of menu items in the sidebar."""
        try:
            items = self.find_elements(self.MENU_ITEMS)
            return len(items)
        except Exception as exc:
            logger.error("Error counting menu items: %s", exc)
            return 0

    def get_all_menu_items_text(self) -> list[str]:
        """Get the text content of all menu items."""
        texts = []
        for locator in self._ALL_MENU_ITEMS:
            try:
                text = self.get_text(locator).strip()
                if text:
                    texts.append(text)
            except Exception:
                pass
        return texts

    # ── Click methods ─────────────────────────────────────────────────────────

    def click_toggle_menu_button(self) -> None:
        """Click the hamburger toggle button to open the sidebar."""
        logger.info("Clicking toggle menu button")
        self.click(self.MENU_BUTTON)

    def click_menu_item(self, text: str) -> None:
        """Click a menu item by its text label (case-insensitive)."""
        locator = self._get_menu_item_locator(text)
        if locator is None:
            raise ValueError("Unknown menu item: '%s'" % text)

        logger.info("Clicking menu item: '%s'", text)
        self.click(locator)

    def click_close_menu(self) -> None:
        """Click the Close Menu button."""
        logger.info("Clicking close menu button")
        self.click(self.CLOSE_BUTTON)

    def click_all_items(self) -> None:
        """Click the 'All Items' menu link."""
        logger.info("Clicking 'All Items' link")
        self.click(self.ALL_ITEMS_LINK)

    def click_about(self) -> None:
        """Click the 'About' menu link."""
        logger.info("Clicking 'About' link")
        self.click(self.ABOUT_LINK)

    def click_logout(self) -> None:
        """Click the 'Logout' menu link."""
        logger.info("Clicking 'Logout' link")
        self.click(self.LOGOUT_LINK)

    def click_reset_app_state(self) -> None:
        """Click the 'Reset App State' menu link."""
        logger.info("Clicking 'Reset App State' link")
        self.click(self.RESET_APP_LINK)

    # ── Verification methods ──────────────────────────────────────────────────

    def verify_all_menu_items_visible(self) -> bool:
        """Verify that all menu items are visible."""
        for item_text in ["All Items", "About", "Logout", "Reset App State"]:
            if not self.is_menu_item_visible(item_text):
                logger.warning("Menu item not visible: '%s'", item_text)
                return False
        logger.info("All menu items are visible")
        return True

    def verify_all_menu_items_present(self) -> bool:
        """Verify that all menu items are present in the DOM."""
        for item_text in ["All Items", "About", "Logout", "Reset App State"]:
            if not self.is_menu_item_present(item_text):
                logger.warning("Menu item not present: '%s'", item_text)
                return False
        logger.info("All menu items are present")
        return True

    def verify_close_button_visible(self) -> bool:
        """Verify that the close menu button is visible."""
        is_visible = self.is_element_visible(self.CLOSE_BUTTON)
        if is_visible:
            logger.info("Close menu button is visible")
        else:
            logger.warning("Close menu button is not visible")
        return is_visible

    def wait_for_sidebar_visible(self, timeout: int = 10) -> bool:
        """Wait for the sidebar to become visible."""
        try:
            self.wait_for_element_visibility(self.SIDEBAR_WRAPPER, timeout=timeout)
            logger.info("Sidebar is visible after %d seconds", timeout)
            return True
        except Exception as exc:
            logger.error("Sidebar did not become visible within %d seconds: %s", timeout, exc)
            return False

    def wait_for_sidebar_invisible(self, timeout: int = 10) -> bool:
        """Wait for the sidebar to become invisible."""
        try:
            self.wait_for_element_invisibility(self.SIDEBAR_WRAPPER, timeout=timeout)
            logger.info("Sidebar is invisible after %d seconds", timeout)
            return True
        except Exception as exc:
            logger.error("Sidebar did not become invisible within %d seconds: %s", timeout, exc)
            return False

    # ── Private helper methods ────────────────────────────────────────────────

    def _get_menu_item_locator(self, text: str) -> Locator | None:
        """Return the locator tuple for a menu item by text (case-insensitive)."""
        normalized_text = text.strip().lower()
        return self._MENU_ITEMS_BY_TEXT.get(normalized_text, None)

    def _find_element_by_text(self, text: str) -> WebElement | None:
        """Find a menu item element by its visible text."""
        try:
            # XPath to find menu items by visible text (case-insensitive)
            xpath = "//a[@class='bm-item menu-item' and contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), translate('%s', 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'))]" % text
            locator = (By.XPATH, xpath)
            return self.find_element(locator)
        except Exception:
            return None

