"""Checkout step two page object."""

from selenium.webdriver.common.by import By

from core.base_page import BasePage
from utils.logger import get_logger

logger = get_logger(__name__)


class CheckoutStepTwoPage(BasePage):
    FINISH_BUTTON = (By.ID, "finish")
    CART_ITEMS = (By.CLASS_NAME, "cart_item")
    ITEM_TOTAL = (By.CLASS_NAME, "summary_subtotal_label")

    def click_finish(self) -> None:
        logger.info("Completing checkout")
        self.click(self.FINISH_BUTTON)

    def get_items_count(self) -> int:
        items = self.find_elements(self.CART_ITEMS)
        return len(items)

