"""Checkout complete page object."""

from selenium.webdriver.common.by import By

from core.base_page import BasePage


class CheckoutCompletePage(BasePage):
    COMPLETE_HEADER = (By.CLASS_NAME, "complete-header")
    COMPLETE_TEXT = (By.CLASS_NAME, "complete-text")

    def is_checkout_complete(self) -> bool:
        return self.is_element_visible(self.COMPLETE_HEADER, timeout=5)

    def get_completion_message(self) -> str:
        return self.get_text(self.COMPLETE_TEXT)

