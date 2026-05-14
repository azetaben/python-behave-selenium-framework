"""Inventory page object."""

import re
import time

from selenium.webdriver.common.by import By

from core.base_page import BasePage
from utils.logger import get_logger

logger = get_logger(__name__)


class InventoryPage(BasePage):
    INVENTORY_ITEMS = (By.CLASS_NAME, "inventory_item")
    PRODUCT_NAME = (By.CLASS_NAME, "inventory_item_name")
    PRODUCT_PRICE = (By.CLASS_NAME, "inventory_item_price")
    ADD_TO_CART_BUTTON = (By.CLASS_NAME, "btn_inventory")
    CART_BADGE = (By.CLASS_NAME, "shopping_cart_badge")

    @staticmethod
    def _slugify_product_name(name: str) -> str:
        slug = name.strip().lower().replace(" ", "-")
        slug = re.sub(r"[^a-z0-9\-]", "", slug)
        slug = re.sub(r"-+", "-", slug)
        return slug

    def get_product_count(self) -> int:
        products = self.find_elements(self.INVENTORY_ITEMS)
        logger.debug("Inventory count: %d", len(products))
        return len(products)

    def add_product_to_cart(self, product_index: int) -> None:
        logger.info("Adding product at inventory index %d to cart", product_index)
        buttons = self.find_elements((By.CSS_SELECTOR, "button[id^='add-to-cart-']"))
        if product_index < 0 or product_index >= len(buttons):
            raise IndexError(f"Product index out of range: {product_index}. Available products: {len(buttons)}")

        button_id = buttons[product_index].get_attribute("id")
        remove_id = button_id.replace("add-to-cart-", "remove-", 1)
        add_locator = (By.ID, button_id)
        remove_locator = (By.ID, remove_id)

        self.scroll_to_element(add_locator)
        time.sleep(0.3)
        try:
            self.click(add_locator)
        except Exception as e:
            logger.warning("Regular click failed for product at index %d, attempting JS click: %s", product_index, e)
            if self.element_exists(add_locator, timeout=1):
                self.js_click(add_locator)
            else:
                raise

        if not self.is_element_visible(remove_locator, timeout=3):
            logger.debug("Remove button not visible after click at index %d, checking add button", product_index)
            if self.element_exists(add_locator, timeout=1):
                logger.info("Add button still exists, trying JS click as fallback")
                self.js_click(add_locator)

        assert self.is_element_visible(remove_locator, timeout=5), (
            f"Add to cart did not complete for product index {product_index}. Remove button not visible after 5 seconds."
        )
        logger.info("Product index %d added to cart", product_index)

    def get_product_name(self, product_index: int) -> str:
        products = self.find_elements(self.PRODUCT_NAME)
        return products[product_index].text if product_index < len(products) else ""

    def click_product_by_name(self, name: str) -> None:
        locator = (By.XPATH, f"//div[contains(@class,'inventory_item_name') and text()='{name}']")
        self.click(locator)

    def is_product_displayed(self, name: str) -> bool:
        return any(el.text.strip() == name.strip() for el in self.find_elements(self.PRODUCT_NAME))

    def get_all_product_names(self) -> list[str]:
        return [el.text.strip() for el in self.find_elements(self.PRODUCT_NAME)]

    def add_product_by_name(self, name: str) -> None:
        logger.info("Adding product '%s' to cart", name)
        product_xpath = f"//div[contains(@class, 'inventory_item') and contains(., '{name}')]"
        product_locator = (By.XPATH, product_xpath)
        if not self.element_exists(product_locator, timeout=3):
            available = self.get_all_product_names()
            logger.error("Product '%s' not found on page. Available: %s", name, available)
            raise ValueError(f"Product '{name}' not found on the page. Available: {available}")

        add_locator = (By.XPATH, f"{product_xpath}//button[contains(@id, 'add-to-cart')]")
        remove_locator = (By.XPATH, f"{product_xpath}//button[contains(@id, 'remove')]")
        self.scroll_to_element(product_locator)
        time.sleep(0.3)
        try:
            self.click(add_locator)
        except Exception as e:
            logger.warning("Regular click failed for '%s', attempting JS click: %s", name, e)
            if self.element_exists(add_locator, timeout=1):
                self.js_click(add_locator)
            else:
                raise

        if not self.is_element_visible(remove_locator, timeout=3):
            logger.debug("Remove button not visible after click, checking if add button still exists")
            if self.element_exists(add_locator, timeout=1):
                logger.info("Add button still exists, trying JS click as fallback")
                self.js_click(add_locator)

        assert self.is_element_visible(remove_locator, timeout=5), (
            f"Add to cart did not complete for '{name}'. Remove button not visible after 5 seconds."
        )
        logger.info("Product '%s' added to cart", name)

    def is_remove_button_visible_for(self, name: str) -> bool:
        product_xpath = f"//div[contains(@class, 'inventory_item') and contains(., '{name}')]"
        remove_locator = (By.XPATH, f"{product_xpath}//button[contains(@id, 'remove')]")
        return self.is_element_visible(remove_locator, timeout=5)

    def remove_product_by_name(self, name: str) -> None:
        slug = self._slugify_product_name(name)
        remove_locator = (By.ID, f"remove-{slug}")
        if self.element_exists(remove_locator, timeout=2):
            self.click(remove_locator)
            return

        product_xpath = f"//div[contains(@class, 'inventory_item') and contains(., '{name}')]"
        fallback_locator = (By.XPATH, f"{product_xpath}//button[contains(@id, 'remove')]")
        if not self.element_exists(fallback_locator, timeout=2):
            raise ValueError(f"Remove button not found for product '{name}'")
        self.click(fallback_locator)

    def get_cart_count(self) -> int:
        from exceptions import safe_int
        return safe_int(lambda: int(self.get_text(self.CART_BADGE)))

