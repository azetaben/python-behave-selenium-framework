"""Top navigation page object."""

from selenium.webdriver.common.by import By

from constants.app_constants import AppConstants
from core.base_page import BasePage
from utils.logger import get_logger

logger = get_logger(__name__)


class TopNavigationPage(BasePage):

    MENU_BUTTON = (By.ID, "react-burger-menu-btn")
    LOGOUT_LINK = (By.ID, "logout_sidebar_link")
    CART_LINK = (By.CLASS_NAME, "shopping_cart_link")
    CART_BADGE = (By.CLASS_NAME, "shopping_cart_badge")

    def open_menu(self) -> None:
        logger.debug("Opening top navigation menu")
        self.click(self.MENU_BUTTON)

    def logout(self) -> None:
        logger.info("Logging out via top navigation menu")
        self.open_menu()
        self.click(self.LOGOUT_LINK)

    def go_to_cart(self) -> None:
        logger.debug("Navigating to cart from top navigation")
        self.click(self.CART_LINK)
        if not self.wait_for_url_contains(AppConstants.Pages.CART_URL_FRACTION, timeout=5):
            logger.warning("Cart URL not reached via click; falling back to direct load")
            self.load(AppConstants.Pages.CART_URL_FRACTION)

