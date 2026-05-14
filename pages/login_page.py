"""Login page object."""

from selenium.webdriver.common.by import By

from core.base_page import BasePage
from utils.logger import get_logger

logger = get_logger(__name__)


class LoginPage(BasePage):
    USERNAME = (By.ID, "user-name")
    PASSWORD = (By.ID, "password")
    LOGIN_BUTTON = (By.ID, "login-button")
    ERROR_MESSAGE = (By.CSS_SELECTOR, "[data-test='error']")

    def login(self, username: str, password: str) -> None:
        logger.info("Attempting login for user '%s'", username)
        self.type_text(self.USERNAME, username)
        self.type_text(self.PASSWORD, password)
        self.click(self.LOGIN_BUTTON)

    def is_error_displayed(self) -> bool:
        return self.is_element_visible(self.ERROR_MESSAGE, timeout=3)

    def get_error_message(self) -> str:
        return self.get_text(self.ERROR_MESSAGE)

