"""Checkout step one page object."""

from selenium.webdriver.common.by import By

from constants.app_constants import AppConstants
from core.base_page import BasePage
from utils.logger import get_logger

logger = get_logger(__name__)


class CheckoutStepOnePage(BasePage):
    FIRST_NAME = (By.ID, "first-name")
    LAST_NAME = (By.ID, "last-name")
    POSTAL_CODE = (By.ID, "postal-code")
    CONTINUE_BUTTON = (By.ID, "continue")
    ERROR_MESSAGE = (By.CSS_SELECTOR, "[data-test='error']")

    def fill_checkout_info(self, first_name: str, last_name: str, postal_code: str) -> None:
        logger.info("Filling checkout information")
        self.wait_for_url_contains(AppConstants.Pages.CHECKOUT_STEP_ONE_URL_FRACTION)
        self.type_text(self.FIRST_NAME, first_name)
        self.type_text(self.LAST_NAME, last_name)
        self.type_text(self.POSTAL_CODE, postal_code)

    def click_continue(self) -> None:
        logger.debug("Clicking checkout continue")
        self.click(self.CONTINUE_BUTTON)

    def is_error_displayed(self) -> bool:
        return self.is_element_visible(self.ERROR_MESSAGE, timeout=3)

    def get_error_message(self) -> str:
        return self.get_text(self.ERROR_MESSAGE)

