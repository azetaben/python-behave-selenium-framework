"""Configuration reader with property validation."""

from typing import Optional

from config.framework_config import FrameworkConfig
from utils.logger import get_logger

logger = get_logger(__name__)


class ConfigReader:
    """Configuration reader with logging and validation."""

    def __init__(self):
        self._config = FrameworkConfig.get_instance()

    def get_property(self, key: str) -> Optional[str]:
        value = self._config.get_string(key)
        if value is None:
            logger.warning("Optional property not found: '%s' in config.properties or .env", key)
        return value

    def get_required_property(self, key: str) -> str:
        value = self._config.get_string(key)
        if value is None or not value.strip():
            raise RuntimeError(
                f"Required config property '{key}' is missing or empty in config.properties or .env"
            )
        return value
