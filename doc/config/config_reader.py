"""
Configuration reader with property validation.

Equivalent to Java ConfigReader class.
Provides methods to get required and optional configuration properties with logging.
"""

from typing import Optional

from doc.config.framework_config import FrameworkConfig
from utils.logger import get_logger


logger = get_logger(__name__)


class ConfigReader:
    """
    Configuration reader with logging and validation.

    Logs warnings for missing optional properties and raises errors for missing required properties.

    Equivalent to Java ConfigReader.
    """

    def __init__(self):
        """Initialize config reader with framework config singleton."""
        self._config = FrameworkConfig.get_instance()

    def get_property(self, key: str) -> Optional[str]:
        """
        Get optional configuration property.

        Logs a warning if the property is not found.

        Args:
            key: Property key

        Returns:
            Property value or None if not found
        """
        value = self._config.get_string(key)

        if value is None:
            config_path = "config.properties or .env"
            logger.warning(
                f"Optional property not found: '{key}' in {config_path}"
            )

        return value

    def get_required_property(self, key: str) -> str:
        """
        Get required configuration property.

        Raises an error if the property is missing or empty.

        Args:
            key: Property key

        Returns:
            Property value

        Raises:
            RuntimeError: If property is missing or empty
        """
        value = self._config.get_string(key)

        if value is None or not value.strip():
            config_path = "config.properties or .env"
            raise RuntimeError(
                f"Required config property '{key}' is missing or empty in {config_path}"
            )

        return value

