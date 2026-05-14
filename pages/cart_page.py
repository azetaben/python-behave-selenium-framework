"""Cart page object."""

from selenium.webdriver.common.by import By

from constants.app_constants import AppConstants
from core.base_page import BasePage
from utils.logger import get_logger

logger = get_logger(__name__)


class CartPage(BasePage):
    CART_ITEMS = (By.CLASS_NAME, "cart_item")
    REMOVE_BUTTON = (By.CSS_SELECTOR, "button[id^='remove-']")
    CHECKOUT_BUTTON = (By.ID, "checkout")
    CART_ITEM_NAME = (By.CLASS_NAME, "inventory_item_name")

    def get_cart_items_count(self) -> int:
        items = self.find_elements(self.CART_ITEMS)
        logger.debug("Cart items count: %d", len(items))
        return len(items)

    def remove_item_from_cart(self, item_index: int = 0) -> None:
        logger.info("Attempting to remove item at index %d from cart", item_index)
        self.click(self.REMOVE_BUTTON)

    def proceed_to_checkout(self) -> None:
        logger.info("Proceeding from cart to checkout step one")
        self.click(self.CHECKOUT_BUTTON)
        self.wait_for_url_contains(AppConstants.Pages.CHECKOUT_STEP_ONE_URL_FRACTION)

    def get_item_name(self, item_index: int) -> str:
        names = self.find_elements(self.CART_ITEM_NAME)
        return names[item_index].text if item_index < len(names) else ""

    def is_item_in_cart(self, name: str) -> bool:
        return any(el.text.strip() == name.strip() for el in self.find_elements(self.CART_ITEM_NAME))

    def get_all_item_names(self) -> list[str]:
        return [el.text.strip() for el in self.find_elements(self.CART_ITEM_NAME)]

