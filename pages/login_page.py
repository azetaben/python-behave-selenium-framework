"""Login page object."""

import re

from selenium.webdriver.common.by import By

from core.base_page import BasePage
from utils.logger import get_logger

logger = get_logger(__name__)


class LoginPage(BasePage):
    LOGO = (By.CLASS_NAME, "login_logo")
    USERNAME = (By.ID, "user-name")
    PASSWORD = (By.ID, "password")
    LOGIN_BUTTON = (By.ID, "login-button")
    ERROR_MESSAGE = (By.CSS_SELECTOR, "[data-test='error']")
    LOGIN_CREDENTIALS_PANEL = (By.CLASS_NAME, "login_credentials_wrap-inner")
    LOGIN_CREDENTIALS = (By.ID, "login_credentials")
    LOGIN_PASSWORD_HINT = (By.CSS_SELECTOR, "[data-test='login-password']")

    ACCEPTED_USERNAMES_TEXT = "Accepted usernames are:"
    SHARED_PASSWORD_TEXT = "Password for all users:"


    def login(self, username: str, password: str) -> None:
        logger.info("Attempting login for user '%s'", username)
        self.type_text(self.USERNAME, username)
        self.type_text(self.PASSWORD, password)
        self.click(self.LOGIN_BUTTON)

    def is_error_displayed(self) -> bool:
        return self.is_element_visible(self.ERROR_MESSAGE, timeout=3)

    def get_error_message(self) -> str:
        return self.get_text(self.ERROR_MESSAGE)

    @staticmethod
    def _xpath_literal(value: str) -> str:
        if "'" not in value:
            return f"'{value}'"
        if '"' not in value:
            return f'"{value}"'

        parts = value.split("'")
        # Build an XPath concat(...) literal for strings containing both quote types.
        return "concat(" + ", \"'\", ".join(f"'{part}'" for part in parts) + ")"

    def is_text_displayed(self, text: str, timeout: int = 3) -> bool:
        locator = (By.XPATH, f"//*[contains(normalize-space(.), {self._xpath_literal(text)})]")
        return self.is_element_visible(locator, timeout=timeout)

    def is_accepted_usernames_hint_displayed(self) -> bool:
        return self.is_text_displayed(self.ACCEPTED_USERNAMES_TEXT, timeout=3)

    def is_password_hint_displayed(self) -> bool:
        return self.is_text_displayed(self.SHARED_PASSWORD_TEXT, timeout=3)

    def get_accepted_usernames(self) -> list[str]:
        outer_html = self.get_attribute(self.LOGIN_CREDENTIALS, "outerHTML")
        if not outer_html:
            return []

        body = re.sub(r"(?is)^.*?</h4>", "", outer_html, count=1)
        body = re.sub(r"(?is)</div>.*$", "", body, count=1)
        body = re.sub(r"(?is)<br\s*/?>", "\n", body)
        body = re.sub(r"(?is)<[^>]+>", "", body)

        usernames = [line.strip() for line in body.splitlines() if line.strip()]
        logger.debug("Extracted %d accepted usernames", len(usernames))
        return usernames

    def get_shared_password(self) -> str:
        outer_html = self.get_attribute(self.LOGIN_PASSWORD_HINT, "outerHTML")
        if not outer_html:
            return ""

        body = re.sub(r"(?is)^.*?</h4>", "", outer_html, count=1)
        body = re.sub(r"(?is)</div>.*$", "", body, count=1)
        password = re.sub(r"(?is)<[^>]+>", "", body).strip()
        logger.debug("Extracted shared password from login hint")
        return password

    def login_with_shared_password(self, username: str) -> None:
        shared_password = self.get_shared_password()
        if not shared_password:
            raise ValueError("Could not extract shared password from login page")
        self.login(username, shared_password)

    def login_with_accepted_username(self, username: str) -> None:
        accepted_usernames = self.get_accepted_usernames()
        if username not in accepted_usernames:
            raise ValueError(f"Username '{username}' is not listed in accepted usernames")
        self.login_with_shared_password(username)

    def login_with_accepted_username_by_index(self, index: int = 0) -> str:
        accepted_usernames = self.get_accepted_usernames()
        if not accepted_usernames:
            raise ValueError("No accepted usernames could be extracted from login page")
        if index < 0 or index >= len(accepted_usernames):
            raise IndexError(f"Accepted username index {index} out of range")

        username = accepted_usernames[index]
        self.login_with_shared_password(username)
        return username

