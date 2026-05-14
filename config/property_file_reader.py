"""Property file reader with token resolution support."""

from typing import Optional

from config import test_data as UserTestData
from config.faker_utils import FakerUtils
from config.framework_config import FrameworkConfig


class PropertyFileReader:
	"""Reads properties from configuration and resolves special tokens."""

	def __init__(self):
		self._config = FrameworkConfig.get_instance()

	def get_username(self) -> Optional[str]:
		return self._config.get_string("username")

	def get_password(self) -> Optional[str]:
		return self._config.get_string("password")

	def get_website(self) -> Optional[str]:
		return self._config.get_string("url")

	def get_property(self, key: str) -> Optional[str]:
		return self._config.get_string(key, "")

	def get_file_property(self, key: str) -> str:
		props = self._config.as_properties()
		value = props.get(key)
		return value.strip() if value else ""

	def get_required_property(self, key: str) -> str:
		value = self._config.get_string(key, "")
		if not value or not value.strip():
			raise ValueError(f"Required config key is missing or blank: {key}")
		return value

	def resolve_value(self, raw_value: Optional[str]) -> str:
		if raw_value is None:
			return ""

		trimmed = raw_value.strip()
		if not trimmed:
			return ""

		normalized = self._unwrap_token(trimmed)
		lowered = normalized.lower()

		if lowered.startswith("config:") or lowered.startswith("config."):
			separator_pos = max(normalized.find(":"), normalized.find("."))
			key = normalized[separator_pos + 1 :].strip()
			file_value = self.get_file_property(key)
			return file_value if file_value else self.get_property(key)

		if lowered.startswith("faker:") or lowered.startswith("faker."):
			separator_pos = max(normalized.find(":"), normalized.find("."))
			token = normalized[separator_pos + 1 :].strip()
			return FakerUtils.resolve_token(token)

		if (
			lowered.startswith("user:")
			or lowered.startswith("user.")
			or lowered.startswith("userdata:")
			or lowered.startswith("userdata.")
		):
			separator_pos = max(normalized.find(":"), normalized.find("."))
			token = normalized[separator_pos + 1 :].strip()
			return self._resolve_user_test_data_token(token)

		return trimmed

	def get_page_load_timeout(self) -> int:
		return self._config.get_int("pageLoadTimeOut", 30)

	def get_implicit_wait(self) -> int:
		return self._config.get_int("implicitWaitTimeout", 10)

	def get_explicit_wait(self) -> int:
		return self._config.get_int("explicitWaitTimeout", 15)

	def get_logger_level(self) -> str:
		level = self._config.get_string("Logger.Level", "ALL")
		valid_levels = {"DEBUG", "INFO", "WARN", "WARNING", "ERROR", "FATAL", "ALL"}
		return level.upper() if level.upper() in valid_levels else "ALL"

	@staticmethod
	def _resolve_user_test_data_token(token: str) -> str:
		if token is None or not token.strip():
			return ""

		token_upper = token.strip().upper()
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
		if token.startswith("${") and token.endswith("}"):
			return token[2:-1].strip()
		return token
