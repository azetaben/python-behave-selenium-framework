"""Product detail page object."""

from selenium.webdriver.common.by import By

from core.base_page import BasePage
from utils.logger import get_logger

logger = get_logger(__name__)


class ProductDetailPage(BasePage):
    PRODUCT_NAME = (By.CSS_SELECTOR, ".inventory_details_name")
    PRODUCT_DESC = (By.CSS_SELECTOR, ".inventory_details_desc")
    PRODUCT_PRICE = (By.CSS_SELECTOR, ".inventory_details_price")
    ADD_TO_CART = (By.CSS_SELECTOR, ".btn_primary.btn_inventory")
    REMOVE_BUTTON = (By.CSS_SELECTOR, ".btn_secondary.btn_inventory")
    BACK_BUTTON = (By.ID, "back-to-products")

    def get_product_name(self) -> str:
        return self.get_text(self.PRODUCT_NAME)

    def is_product_visible(self) -> bool:
        return self.is_element_visible(self.PRODUCT_NAME, timeout=5)

    def add_to_cart(self) -> None:
        logger.info("Adding product from detail page to cart")
        self.click(self.ADD_TO_CART)

    def remove_from_cart(self) -> None:
        logger.info("Removing product from detail page cart")
        self.click(self.REMOVE_BUTTON)

    def is_remove_button_visible(self) -> bool:
        return self.is_element_visible(self.REMOVE_BUTTON, timeout=3)

    def is_back_button_visible(self) -> bool:
        return self.is_element_visible(self.BACK_BUTTON, timeout=3)

    def go_back_to_products(self) -> None:
        logger.debug("Navigating back to products from detail page")
        self.click(self.BACK_BUTTON)

