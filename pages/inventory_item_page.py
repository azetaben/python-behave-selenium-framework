"""Inventory item (product detail) page object.

Built from the Sauce Demo inventory-item HTML structure.
Supports:
- element presence/visibility checks
- text-based element verification
- text-based click actions for all clickable controls
"""

from __future__ import annotations

from selenium.webdriver.common.by import By

from core.base_page import BasePage
from core.page_element_mixin import Locator
from utils.logger import get_logger

logger = get_logger(__name__)


class InventoryItemPage(BasePage):
    """Page object for the inventory item detail page."""

    # ── Containers ────────────────────────────────────────────────────────────
    SECONDARY_HEADER: Locator = (By.CSS_SELECTOR, "div.header_secondary_container[data-test='secondary-header']")
    LEFT_COMPONENT: Locator = (By.CSS_SELECTOR, "div.header_secondary_container .left_component")
    INVENTORY_DETAILS: Locator = (By.CSS_SELECTOR, "div.inventory_details")
    INVENTORY_ITEM_CONTAINER: Locator = (By.CSS_SELECTOR, "div.inventory_details_container[data-test='inventory-item']")
    ITEM_IMAGE_CONTAINER: Locator = (By.CSS_SELECTOR, "div.inventory_details_img_container")
    ITEM_DESC_CONTAINER: Locator = (By.CSS_SELECTOR, "div.inventory_details_desc_container")

    # ── Primary item elements ────────────────────────────────────────────────
    BACK_TO_PRODUCTS_BUTTON: Locator = (By.ID, "back-to-products")
    BACK_TO_PRODUCTS_IMAGE: Locator = (By.CSS_SELECTOR, "#back-to-products .back-image")

    ITEM_IMAGE: Locator = (By.CSS_SELECTOR, "img.inventory_details_img")
    ITEM_NAME: Locator = (By.CSS_SELECTOR, "div.inventory_details_name[data-test='inventory-item-name']")
    ITEM_DESCRIPTION: Locator = (By.CSS_SELECTOR, "div.inventory_details_desc[data-test='inventory-item-desc']")
    ITEM_PRICE: Locator = (By.CSS_SELECTOR, "div.inventory_details_price[data-test='inventory-item-price']")

    ADD_TO_CART_BUTTON: Locator = (By.CSS_SELECTOR, "button[data-test^='add-to-cart']")
    ADD_TO_CART_BUTTON_FALLBACK: Locator = (By.CSS_SELECTOR, "button[id^='add-to-cart']")
    REMOVE_BUTTON: Locator = (By.ID, "remove")
    REMOVE_BUTTON_BY_DATA_TEST: Locator = (By.CSS_SELECTOR, "button[data-test='remove']")
    REMOVE_BUTTON_FALLBACK: Locator = (By.CSS_SELECTOR, "button[id^='remove']")

    # ── Clickable elements by text ───────────────────────────────────────────
    _CLICKABLE_BY_TEXT: dict[str, Locator] = {
        "add to cart": ADD_TO_CART_BUTTON,
        "back to products": BACK_TO_PRODUCTS_BUTTON,
        "remove": REMOVE_BUTTON,
    }

    # ── Verifiable elements by text key ──────────────────────────────────────
    _ELEMENT_BY_TEXT_KEY: dict[str, Locator] = {
        "secondary header": SECONDARY_HEADER,
        "left component": LEFT_COMPONENT,
        "inventory details": INVENTORY_DETAILS,
        "inventory item": INVENTORY_ITEM_CONTAINER,
        "item image container": ITEM_IMAGE_CONTAINER,
        "item description container": ITEM_DESC_CONTAINER,
        "back to products": BACK_TO_PRODUCTS_BUTTON,
        "back to products button": BACK_TO_PRODUCTS_BUTTON,
        "back image": BACK_TO_PRODUCTS_IMAGE,
        "item image": ITEM_IMAGE,
        "item name": ITEM_NAME,
        "item description": ITEM_DESCRIPTION,
        "item price": ITEM_PRICE,
        "add to cart": ADD_TO_CART_BUTTON,
        "add to cart button": ADD_TO_CART_BUTTON,
        "remove": REMOVE_BUTTON,
        "remove button": REMOVE_BUTTON,
    }

    _ALL_CORE_ELEMENTS: list[Locator] = [
        SECONDARY_HEADER,
        LEFT_COMPONENT,
        INVENTORY_DETAILS,
        INVENTORY_ITEM_CONTAINER,
        ITEM_IMAGE_CONTAINER,
        ITEM_DESC_CONTAINER,
        BACK_TO_PRODUCTS_BUTTON,
        ITEM_IMAGE,
        ITEM_NAME,
        ITEM_DESCRIPTION,
        ITEM_PRICE,
    ]

    # ── Generic presence/visibility helpers ──────────────────────────────────

    def is_element_visible_by_text(self, element_key: str, timeout: int = 5) -> bool:
        """Check visibility of a page element using a text key (case-insensitive)."""
        normalized_key = element_key.strip().lower()

        if normalized_key in {"add to cart", "add to cart button"}:
            return (
                self.is_element_visible(self.ADD_TO_CART_BUTTON, timeout=1)
                or self.is_element_visible(self.ADD_TO_CART_BUTTON_FALLBACK, timeout=1)
            )

        if normalized_key in {"remove", "remove button"}:
            return (
                self.is_element_visible(self.REMOVE_BUTTON_BY_DATA_TEST, timeout=1)
                or self.is_element_visible(self.REMOVE_BUTTON_FALLBACK, timeout=1)
            )

        locator = self._ELEMENT_BY_TEXT_KEY.get(normalized_key)
        if locator is None:
            logger.warning("Unknown element key for visibility check: '%s'", element_key)
            return False
        return self.is_element_visible(locator, timeout=timeout)

    def is_element_present_by_text(self, element_key: str, timeout: int = 1) -> bool:
        """Check DOM presence of a page element using a text key (case-insensitive)."""
        normalized_key = element_key.strip().lower()

        if normalized_key in {"add to cart", "add to cart button"}:
            return (
                self.element_exists(self.ADD_TO_CART_BUTTON, timeout=1)
                or self.element_exists(self.ADD_TO_CART_BUTTON_FALLBACK, timeout=1)
            )

        if normalized_key in {"remove", "remove button"}:
            return (
                self.element_exists(self.REMOVE_BUTTON_BY_DATA_TEST, timeout=1)
                or self.element_exists(self.REMOVE_BUTTON_FALLBACK, timeout=1)
            )

        locator = self._ELEMENT_BY_TEXT_KEY.get(normalized_key)
        if locator is None:
            logger.warning("Unknown element key for presence check: '%s'", element_key)
            return False
        return self.element_exists(locator, timeout=timeout)

    def verify_all_core_elements_visible(self, timeout: int = 5) -> bool:
        """Verify all key inventory-item elements are visible."""
        for locator in self._ALL_CORE_ELEMENTS:
            if not self.is_element_visible(locator, timeout=timeout):
                logger.warning("Core element not visible: %s", locator)
                return False

        # Product action button is stateful: it can be either Add to cart or Remove.
        action_visible = (
            self.is_element_visible(self.REMOVE_BUTTON_BY_DATA_TEST, timeout=1)
            or self.is_element_visible(self.REMOVE_BUTTON_FALLBACK, timeout=1)
            or self.is_element_visible(self.ADD_TO_CART_BUTTON, timeout=1)
            or self.is_element_visible(self.ADD_TO_CART_BUTTON_FALLBACK, timeout=1)
        )
        if not action_visible:
            logger.warning("Core action button not visible: neither add-to-cart nor remove found")
            return False

        logger.info("All core inventory item elements are visible")
        return True

    def verify_all_core_elements_present(self, timeout: int = 1) -> bool:
        """Verify all key inventory-item elements are present in DOM."""
        for locator in self._ALL_CORE_ELEMENTS:
            if not self.element_exists(locator, timeout=timeout):
                logger.warning("Core element not present: %s", locator)
                return False

        action_present = (
            self.element_exists(self.REMOVE_BUTTON_BY_DATA_TEST, timeout=1)
            or self.element_exists(self.REMOVE_BUTTON_FALLBACK, timeout=1)
            or self.element_exists(self.ADD_TO_CART_BUTTON, timeout=1)
            or self.element_exists(self.ADD_TO_CART_BUTTON_FALLBACK, timeout=1)
        )
        if not action_present:
            logger.warning("Core action button not present: neither add-to-cart nor remove found")
            return False

        logger.info("All core inventory item elements are present")
        return True

    # ── Value getters ─────────────────────────────────────────────────────────

    def get_item_name(self) -> str:
        return self.get_text(self.ITEM_NAME).strip()

    def get_item_description(self) -> str:
        return self.get_text(self.ITEM_DESCRIPTION).strip()

    def get_item_price(self) -> str:
        return self.get_text(self.ITEM_PRICE).strip()

    def get_item_image_alt(self) -> str:
        return self.get_attribute(self.ITEM_IMAGE, "alt").strip()

    # ── Verify by expected text/value ─────────────────────────────────────────

    def verify_item_name(self, expected_name: str) -> bool:
        actual = self.get_item_name()
        ok = actual == expected_name.strip()
        if not ok:
            logger.warning("Item name mismatch. Expected='%s', Actual='%s'", expected_name, actual)
        return ok

    def verify_item_description_contains(self, expected_part: str) -> bool:
        actual = self.get_item_description()
        ok = expected_part.strip() in actual
        if not ok:
            logger.warning("Item description does not contain '%s'. Actual='%s'", expected_part, actual)
        return ok

    def verify_item_price(self, expected_price: str) -> bool:
        actual = self.get_item_price()
        ok = actual == expected_price.strip()
        if not ok:
            logger.warning("Item price mismatch. Expected='%s', Actual='%s'", expected_price, actual)
        return ok

    # ── Click actions ─────────────────────────────────────────────────────────

    def click_by_text(self, text: str) -> None:
        """Click a supported button/control by visible text key."""
        locator = self._CLICKABLE_BY_TEXT.get(text.strip().lower())
        if locator is None:
            raise ValueError("Unsupported clickable text '%s'. Supported: %s" % (text, ", ".join(self._CLICKABLE_BY_TEXT)))
        logger.info("Clicking inventory-item control by text: '%s'", text)
        self.click(locator)

    def click_back_to_products(self) -> None:
        logger.info("Clicking 'Back to products'")
        self.click(self.BACK_TO_PRODUCTS_BUTTON)

    def click_add_to_cart(self) -> None:
        logger.info("Clicking 'Add to cart'")
        if self.element_exists(self.ADD_TO_CART_BUTTON, timeout=1):
            self.click(self.ADD_TO_CART_BUTTON)
            return
        if self.element_exists(self.ADD_TO_CART_BUTTON_FALLBACK, timeout=1):
            self.click(self.ADD_TO_CART_BUTTON_FALLBACK)
            return
        raise AssertionError("Add to cart button is not present on inventory item page")

    def click_remove(self) -> None:
        logger.info("Clicking 'Remove'")
        if self.element_exists(self.REMOVE_BUTTON_BY_DATA_TEST, timeout=1):
            self.click(self.REMOVE_BUTTON_BY_DATA_TEST)
            return
        if self.element_exists(self.REMOVE_BUTTON_FALLBACK, timeout=1):
            self.click(self.REMOVE_BUTTON_FALLBACK)
            return
        raise AssertionError("Remove button is not present on inventory item page")

    # ── Convenience visibility helpers ────────────────────────────────────────

    def is_back_to_products_visible(self) -> bool:
        return self.is_element_visible(self.BACK_TO_PRODUCTS_BUTTON, timeout=3)

    def is_remove_visible(self) -> bool:
        return (
            self.is_element_visible(self.REMOVE_BUTTON_BY_DATA_TEST, timeout=1)
            or self.is_element_visible(self.REMOVE_BUTTON_FALLBACK, timeout=1)
        )

    def is_item_image_visible(self) -> bool:
        return self.is_element_visible(self.ITEM_IMAGE, timeout=3)

    def is_item_name_visible(self) -> bool:
        return self.is_element_visible(self.ITEM_NAME, timeout=3)

    def is_item_description_visible(self) -> bool:
        return self.is_element_visible(self.ITEM_DESCRIPTION, timeout=3)

    def is_item_price_visible(self) -> bool:
        return self.is_element_visible(self.ITEM_PRICE, timeout=3)

