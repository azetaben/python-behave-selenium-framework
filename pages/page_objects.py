"""
Page Objects for the Sauce Demo application.

All pages extend BasePage and define locators as class constants.
"""
import re
import time

from selenium.webdriver.common.by import By

from constants.AppConstants import AppConstants
from core.base_page import BasePage
from utils.logger import get_logger


logger = get_logger(__name__)


class LoginPage(BasePage):
    """Login page object."""
    
    USERNAME = (By.ID, "user-name")
    PASSWORD = (By.ID, "password")
    LOGIN_BUTTON = (By.ID, "login-button")
    ERROR_MESSAGE = (By.CSS_SELECTOR, "[data-test='error']")
    
    def login(self, username: str, password: str) -> None:
        """Perform login with credentials."""
        logger.info("Attempting login for user '%s'", username)
        self.type_text(self.USERNAME, username)
        self.type_text(self.PASSWORD, password)
        self.click(self.LOGIN_BUTTON)
    
    def is_error_displayed(self) -> bool:
        """Check if error message is displayed."""
        return self.is_element_visible(self.ERROR_MESSAGE, timeout=3)
    
    def get_error_message(self) -> str:
        """Get error message text."""
        return self.get_text(self.ERROR_MESSAGE)


class InventoryPage(BasePage):
    """Products inventory page object."""
    
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
        """Get number of products displayed."""
        products = self.find_elements(self.INVENTORY_ITEMS)
        logger.debug("Inventory count: %d", len(products))
        return len(products)
    
    def add_product_to_cart(self, product_index: int) -> None:
        """Add product to cart by index (0-based)."""
        logger.info("Adding product at inventory index %d to cart", product_index)

        buttons = self.find_elements((By.CSS_SELECTOR, "button[id^='add-to-cart-']"))
        if product_index < 0 or product_index >= len(buttons):
            raise IndexError(f"Product index out of range: {product_index}. Available products: {len(buttons)}")
        
        button_id = buttons[product_index].get_attribute("id")
        remove_id = button_id.replace("add-to-cart-", "remove-", 1)
        add_locator = (By.ID, button_id)
        remove_locator = (By.ID, remove_id)
        
        # Scroll to the button to ensure visibility
        self.scroll_to_element(add_locator)
        
        # Wait a brief moment for any animations
        time.sleep(0.3)
        
        # Attempt to click the add button
        try:
            self.click(add_locator)
        except Exception as e:
            logger.warning(
                "Regular click failed for product at index %d, attempting JS click: %s",
                product_index,
                e,
            )
            if self.element_exists(add_locator, timeout=1):
                self.js_click(add_locator)
            else:
                raise
        
        # Wait for the remove button to appear
        if not self.is_element_visible(remove_locator, timeout=3):
            logger.debug("Remove button not visible after click at index %d, checking add button", product_index)
            if self.element_exists(add_locator, timeout=1):
                logger.info("Add button still exists, trying JS click as fallback")
                self.js_click(add_locator)
        
        # Final assertion
        assert self.is_element_visible(remove_locator, timeout=5), (
            f"Add to cart did not complete for product index {product_index}. Remove button not visible after 5 seconds."
        )
        logger.info("Product index %d added to cart", product_index)

    def get_product_name(self, product_index: int) -> str:
        """Get product name by index."""
        products = self.find_elements(self.PRODUCT_NAME)
        return products[product_index].text if product_index < len(products) else ""

    def click_product_by_name(self, name: str) -> None:
        """Click the product link with the given name."""
        locator = (By.XPATH, f"//div[contains(@class,'inventory_item_name') and text()='{name}']")
        self.click(locator)

    def is_product_displayed(self, name: str) -> bool:
        """Return True if a product with this exact name is visible on the page."""
        return any(
            el.text.strip() == name.strip()
            for el in self.find_elements(self.PRODUCT_NAME)
        )

    def get_all_product_names(self) -> list[str]:
        """Return all product names currently shown on the inventory page."""
        return [el.text.strip() for el in self.find_elements(self.PRODUCT_NAME)]
    
    def add_product_by_name(self, name: str) -> None:
        """Click 'Add to cart' for the product card matching name."""
        logger.info("Adding product '%s' to cart", name)

        # Find the product item by name using a more robust XPath
        # This XPath finds the inventory_item that contains the product name
        product_xpath = f"//div[contains(@class, 'inventory_item') and contains(., '{name}')]"
        product_locator = (By.XPATH, product_xpath)

        # Check if the product item exists on the page
        if not self.element_exists(product_locator, timeout=3):
            available = self.get_all_product_names()
            logger.error("Product '%s' not found on page. Available: %s", name, available)
            raise ValueError(f"Product '{name}' not found on the page. Available: {available}")

        # Get the add-to-cart button within this product item
        # Use a relative XPath to find the button inside the product container
        add_button_xpath = f"{product_xpath}//button[contains(@id, 'add-to-cart')]"
        add_locator = (By.XPATH, add_button_xpath)
        remove_button_xpath = f"{product_xpath}//button[contains(@id, 'remove')]"
        remove_locator = (By.XPATH, remove_button_xpath)

        # Scroll to the product to ensure visibility
        self.scroll_to_element(product_locator)

        # Wait a brief moment for any animations to complete
        time.sleep(0.3)

        # Attempt to click the add button
        try:
            self.click(add_locator)
        except Exception as e:
            # If regular click fails, try JS click as fallback
            logger.warning("Regular click failed for '%s', attempting JS click: %s", name, e)
            if self.element_exists(add_locator, timeout=1):
                self.js_click(add_locator)
            else:
                raise

        # Wait for the remove button to appear (indicating successful add)
        if not self.is_element_visible(remove_locator, timeout=3):
            logger.debug("Remove button not visible after click, checking if add button still exists")
            if self.element_exists(add_locator, timeout=1):
                logger.info("Add button still exists, trying JS click as fallback")
                self.js_click(add_locator)

        # Final assertion - must see remove button
        assert self.is_element_visible(remove_locator, timeout=5), \
            f"Add to cart did not complete for '{name}'. Remove button not visible after 5 seconds."
        logger.info("Product '%s' added to cart", name)

    def is_remove_button_visible_for(self, name: str) -> bool:
        """Return True if the Remove button is visible for the named product."""
        # Find the product item by name and check if remove button exists
        product_xpath = f"//div[contains(@class, 'inventory_item') and contains(., '{name}')]"
        remove_button_xpath = f"{product_xpath}//button[contains(@id, 'remove')]"
        remove_locator = (By.XPATH, remove_button_xpath)
        return self.is_element_visible(remove_locator, timeout=5)

    def remove_product_by_name(self, name: str) -> None:
        """Remove a named product from cart from the inventory page."""
        slug = self._slugify_product_name(name)
        remove_locator = (By.ID, f"remove-{slug}")

        if self.element_exists(remove_locator, timeout=2):
            self.click(remove_locator)
            return

        # Fallback for minor DOM differences: find remove button inside the matching card.
        product_xpath = f"//div[contains(@class, 'inventory_item') and contains(., '{name}')]"
        remove_button_xpath = f"{product_xpath}//button[contains(@id, 'remove')]"
        fallback_locator = (By.XPATH, remove_button_xpath)
        if not self.element_exists(fallback_locator, timeout=2):
            raise ValueError(f"Remove button not found for product '{name}'")
        self.click(fallback_locator)

    def get_cart_count(self) -> int:
        """Get cart item count from badge."""
        from exceptions import safe_int
        return safe_int(lambda: int(self.get_text(self.CART_BADGE)))


class CartPage(BasePage):
    """Shopping cart page object."""
    
    CART_ITEMS = (By.CLASS_NAME, "cart_item")
    REMOVE_BUTTON = (By.CSS_SELECTOR, "button[id^='remove-']")
    CHECKOUT_BUTTON = (By.ID, "checkout")
    CART_ITEM_NAME = (By.CLASS_NAME, "inventory_item_name")
    
    def get_cart_items_count(self) -> int:
        """Get number of items in cart."""
        items = self.find_elements(self.CART_ITEMS)
        logger.debug("Cart items count: %d", len(items))
        return len(items)
    
    def remove_item_from_cart(self, item_index: int = 0) -> None:
        """Remove item from cart. Clicks the first visible Remove button."""
        logger.info("Attempting to remove item at index %d from cart", item_index)
        self.click(self.REMOVE_BUTTON)
    
    def proceed_to_checkout(self) -> None:
        """Click checkout button and wait for checkout step-one page to load."""
        logger.info("Proceeding from cart to checkout step one")
        self.click(self.CHECKOUT_BUTTON)
        self.wait_for_url_contains(AppConstants.Pages.CHECKOUT_STEP_ONE_URL_FRACTION)

    def get_item_name(self, item_index: int) -> str:
        """Get cart item name by index."""
        names = self.find_elements(self.CART_ITEM_NAME)
        return names[item_index].text if item_index < len(names) else ""

    def is_item_in_cart(self, name: str) -> bool:
        """Return True if an item with this exact name is in the cart."""
        return any(
            el.text.strip() == name.strip()
            for el in self.find_elements(self.CART_ITEM_NAME)
        )

    def get_all_item_names(self) -> list[str]:
        """Return the names of all items currently in the cart."""
        return [el.text.strip() for el in self.find_elements(self.CART_ITEM_NAME)]


class CheckoutStepOnePage(BasePage):
    """Checkout Step One (shipping info) page."""
    FIRST_NAME = (By.ID, "first-name")
    LAST_NAME = (By.ID, "last-name")
    POSTAL_CODE = (By.ID, "postal-code")
    CONTINUE_BUTTON = (By.ID, "continue")
    ERROR_MESSAGE = (By.CSS_SELECTOR, "[data-test='error']")
    
    def fill_checkout_info(self, first_name: str, last_name: str, postal_code: str) -> None:
        """Fill checkout information form."""
        logger.info("Filling checkout information")
        self.wait_for_url_contains(AppConstants.Pages.CHECKOUT_STEP_ONE_URL_FRACTION)
        self.type_text(self.FIRST_NAME, first_name)
        self.type_text(self.LAST_NAME, last_name)
        self.type_text(self.POSTAL_CODE, postal_code)
    
    def click_continue(self) -> None:
        """Click continue button."""
        logger.debug("Clicking checkout continue")
        self.click(self.CONTINUE_BUTTON)
    
    def is_error_displayed(self) -> bool:
        """Check if error message is displayed."""
        return self.is_element_visible(self.ERROR_MESSAGE, timeout=3)
    
    def get_error_message(self) -> str:
        """Get error message text."""
        return self.get_text(self.ERROR_MESSAGE)


class CheckoutStepTwoPage(BasePage):
    """Checkout Step Two (review order) page."""
    
    FINISH_BUTTON = (By.ID, "finish")
    CART_ITEMS = (By.CLASS_NAME, "cart_item")
    ITEM_TOTAL = (By.CLASS_NAME, "summary_subtotal_label")
    
    def click_finish(self) -> None:
        """Click finish button to complete checkout."""
        logger.info("Completing checkout")
        self.click(self.FINISH_BUTTON)
    
    def get_items_count(self) -> int:
        """Get number of items in order summary."""
        items = self.find_elements(self.CART_ITEMS)
        return len(items)


class CheckoutCompletePage(BasePage):
    """Order completion confirmation page."""
    
    COMPLETE_HEADER = (By.CLASS_NAME, "complete-header")
    COMPLETE_TEXT = (By.CLASS_NAME, "complete-text")
    
    def is_checkout_complete(self) -> bool:
        """Check if checkout is complete."""
        return self.is_element_visible(self.COMPLETE_HEADER, timeout=5)
    
    def get_completion_message(self) -> str:
        """Get completion message text."""
        return self.get_text(self.COMPLETE_TEXT)


class ProductDetailPage(BasePage):
    """Product detail / inventory-item page object."""

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


class TopNavigationPage(BasePage):
    """Top navigation/header page object."""
    
    MENU_BUTTON = (By.ID, "react-burger-menu-btn")
    LOGOUT_LINK = (By.ID, "logout_sidebar_link")
    CART_LINK = (By.CLASS_NAME, "shopping_cart_link")
    CART_BADGE = (By.CLASS_NAME, "shopping_cart_badge")
    
    def open_menu(self) -> None:
        """Open hamburger menu."""
        logger.debug("Opening top navigation menu")
        self.click(self.MENU_BUTTON)
    
    def logout(self) -> None:
        """Click logout link."""
        logger.info("Logging out via top navigation menu")
        self.open_menu()
        self.click(self.LOGOUT_LINK)
    
    def go_to_cart(self) -> None:
        """Navigate to the cart page via header link with direct-load fallback."""
        logger.debug("Navigating to cart from top navigation")
        self.click(self.CART_LINK)
        if not self.wait_for_url_contains(AppConstants.Pages.CART_URL_FRACTION, timeout=5):
            logger.warning("Cart URL not reached via click; falling back to direct load")
            self.load(AppConstants.Pages.CART_URL_FRACTION)
