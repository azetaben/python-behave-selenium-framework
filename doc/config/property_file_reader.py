"""
Property file reader with token resolution support.

Equivalent to Java PropertyFileReader class.
Reads configuration properties and resolves special tokens (config, faker, user data).
"""

from typing import Optional

from doc.config.faker_utils import FakerUtils
from doc.config.framework_config import FrameworkConfig
from doc.config import test_data as UserTestData
from utils.logger import get_logger

logger = get_logger(__name__)


class PropertyFileReader:
    """
    Reads properties from configuration and resolves special tokens.

    Supports token resolution for:
    - config: config:key or config.key (load from config file)
    - faker: faker:email or faker.random_name (generate random data)
    - user: user:USERNAME or userdata.PASSWORD (load from test data)

    Equivalent to Java PropertyFileReader.
    """

    def __init__(self):
        """Initialize property file reader with framework config singleton."""
        self._config = FrameworkConfig.get_instance()

    def get_username(self) -> Optional[str]:
        """
        Get default test username.

        Returns:
            Username from config
        """
        return self._config.get_string("username")

    def get_password(self) -> Optional[str]:
        """
        Get default test password.

        Returns:
            Password from config
        """
        return self._config.get_string("password")

    def get_website(self) -> Optional[str]:
        """
        Get website URL.

        Returns:
            URL from config
        """
        return self._config.get_string("url")

    def get_property(self, key: str) -> Optional[str]:
        """
        Get property by key with empty string default.

        Args:
            key: Property key

        Returns:
            Property value or empty string if not found
        """
        return self._config.get_string(key, "")

    def get_file_property(self, key: str) -> str:
        """
        Get property directly from properties file (bypass environment variables).

        Args:
            key: Property key

        Returns:
            Property value from file or empty string if not found
        """
        props = self._config.as_properties()
        value = props.get(key)
        return value.strip() if value else ""

    def get_required_property(self, key: str) -> str:
        """
        Get required property, raise error if not found or blank.

        Args:
            key: Property key

        Returns:
            Property value

        Raises:
            ValueError: If property is missing or blank
        """
        value = self._config.get_string(key, "")

        if not value or not value.strip():
            raise ValueError(f"Required config key is missing or blank: {key}")

        return value

    def resolve_value(self, raw_value: Optional[str]) -> str:
        """
        Resolve value with special token support.

        Supports:
        - config:key or config.key - load from config properties
        - faker:email or faker.random_name - generate random data
        - user:USERNAME or userdata.CONSTANT - load from test data
        - Plain values are returned as-is

        Args:
            raw_value: Raw value that may contain tokens

        Returns:
            Resolved value
        """
        if raw_value is None:
            return ""

        trimmed = raw_value.strip()
        if not trimmed:
            return ""

        # Unwrap ${...} format if present
        normalized = self._unwrap_token(trimmed)
        lowered = normalized.lower()

        # Determine token type and separator position
        if lowered.startswith("config:") or lowered.startswith("config."):
            separator_pos = max(
                normalized.find(":"),
                normalized.find(".")
            )
            key = normalized[separator_pos + 1:].strip()
            file_value = self.get_file_property(key)
            return file_value if file_value else self.get_property(key)

        if lowered.startswith("faker:") or lowered.startswith("faker."):
            separator_pos = max(
                normalized.find(":"),
                normalized.find(".")
            )
            token = normalized[separator_pos + 1:].strip()
            return FakerUtils.resolve_token(token)

        if (lowered.startswith("user:") or lowered.startswith("user.") or
            lowered.startswith("userdata:") or lowered.startswith("userdata.")):
            separator_pos = max(
                normalized.find(":"),
                normalized.find(".")
            )
            token = normalized[separator_pos + 1:].strip()
            return self._resolve_user_test_data_token(token)

        return trimmed

    def get_page_load_timeout(self) -> int:
        """
        Get page load timeout in seconds.

        Returns:
            Timeout in seconds (default 30)
        """
        return self._config.get_int("pageLoadTimeOut", 30)

    def get_implicit_wait(self) -> int:
        """
        Get implicit wait timeout in seconds.

        Returns:
            Timeout in seconds (default 10)
        """
        return self._config.get_int("implicitWaitTimeout", 10)

    def get_explicit_wait(self) -> int:
        """
        Get explicit wait timeout in seconds.

        Returns:
            Timeout in seconds (default 15)
        """
        return self._config.get_int("explicitWaitTimeout", 15)

    def get_logger_level(self) -> str:
        """
        Get logger level from config.

        Returns:
            Logger level (DEBUG, INFO, WARN, ERROR, FATAL or ALL)
        """
        level = self._config.get_string("Logger.Level", "ALL")

        valid_levels = {"DEBUG", "INFO", "WARN", "WARNING", "ERROR", "FATAL", "ALL"}
        return level.upper() if level.upper() in valid_levels else "ALL"

    @staticmethod
    def _resolve_user_test_data_token(token: str) -> str:
        """
        Resolve test data tokens mapped to UserTestData constants.

        Args:
            token: Token to resolve

        Returns:
            Resolved value from UserTestData constants
        """
        if token is None or not token.strip():
            return ""

        token_upper = token.strip().upper()

        # Create mapping of token names to UserTestData attributes
        token_map = {
            "STANDARD_USERNAME": UserTestData.STANDARD_USERNAME,
            "LOCKED_OUT_USERNAME": UserTestData.LOCKED_OUT_USERNAME,
            "PERFORMANCE_GLITCH_USERNAME": UserTestData.PERFORMANCE_GLITCH_USERNAME,
            "PROBLEM_USERNAME": UserTestData.PROBLEM_USERNAME,
            "INVALID_USERNAME": UserTestData.INVALID_USERNAME,
            "VISUAL_USERNAME": UserTestData.VISUAL_USERNAME,
            "PASSWORD_FOR_ALL_USERS": UserTestData.PASSWORD_FOR_ALL_USERS,
            "PASSWORD": UserTestData.PASSWORD,
            "LOGIN_ERROR_MESSAGE": UserTestData.LOGIN_ERROR_MESSAGE,
            "LOGIN_PAGE_URL": UserTestData.LOGIN_PAGE_URL,
            "LOGIN_BUTTON": UserTestData.LOGIN_BUTTON,
            "CONTINUE_BUTTON": UserTestData.CONTINUE_BUTTON,
            "INVENTORY_PAGE_TITLE": UserTestData.INVENTORY_PAGE_TITLE,
            "INVENTORY_PAGE_URL": UserTestData.INVENTORY_PAGE_URL,
            "CART_PAGE_URL": UserTestData.CART_PAGE_URL,
            "CART_PAGE_TITLE": UserTestData.CART_PAGE_TITLE,
            "CHECKOUT_STEP_ONE_PAGE_URL": UserTestData.CHECKOUT_STEP_ONE_PAGE_URL,
            "CHECKOUT_STEP_ONE_PAGE_TITLE": UserTestData.CHECKOUT_STEP_ONE_PAGE_TITLE,
            "CHECKOUT_STEP_TWO_PAGE_URL": UserTestData.CHECKOUT_STEP_TWO_PAGE_URL,
            "CHECKOUT_STEP_TWO_PAGE_TITLE": UserTestData.CHECKOUT_STEP_TWO_PAGE_TITLE,
            "CHECKOUT_COMPLETE_PAGE_URL": UserTestData.CHECKOUT_COMPLETE_PAGE_URL,
            "CHECKOUT_COMPLETE_PAGE_TITLE": UserTestData.CHECKOUT_COMPLETE_PAGE_TITLE,
        }

        return token_map.get(token_upper, token)

    @staticmethod
    def _unwrap_token(token: str) -> str:
        """
        Remove ${...} wrapper from token if present.

        Args:
            token: Token string possibly wrapped

        Returns:
            Unwrapped token
        """
        if token.startswith("${") and token.endswith("}"):
            return token[2:-1].strip()
        return token

