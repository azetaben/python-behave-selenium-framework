"""
PageManager — central manager for all page objects.

Owns all page instances and injects back-references so pages can cross-navigate.
"""
from selenium import webdriver

from pages.cart_page import CartPage
from pages.checkout_complete_page import CheckoutCompletePage
from pages.checkout_step_one_page import CheckoutStepOnePage
from pages.checkout_step_two_page import CheckoutStepTwoPage
from pages.inventory_page import InventoryPage
from pages.login_page import LoginPage
from pages.product_detail_page import ProductDetailPage
from pages.top_navigation_page import TopNavigationPage
from utils.logger import get_logger


logger = get_logger(__name__)


class PageManager:
    """Manager for all page objects in the application."""
    
    def __init__(self, driver: webdriver.Remote) -> None:
        """Initialize PageManager with WebDriver instance."""
        self.driver = driver
        logger.info("Initializing PageManager and page objects")

        # Initialize all page objects
        self.login = LoginPage(driver)
        self.inventory = InventoryPage(driver)
        self.cart = CartPage(driver)
        self.checkout = CheckoutStepOnePage(driver)
        self.checkout_two = CheckoutStepTwoPage(driver)
        self.complete = CheckoutCompletePage(driver)
        self.product_detail = ProductDetailPage(driver)
        self.nav = TopNavigationPage(driver)

        # Inject manager back-references
        for page in [self.login, self.inventory, self.cart, self.checkout,
                     self.checkout_two, self.complete, self.product_detail, self.nav]:
            page._manager = self
        logger.debug("PageManager ready with %d page objects", 8)
