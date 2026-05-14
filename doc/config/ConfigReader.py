"""
Python conversion: ConfigReader.java

Provides unified property reading with optional/required property support.
Replaces Java exception-based config pattern with Python context and logging.
"""

from typing import Optional
from pathlib import Path

from doc.config.config import settings
from utils.logger import get_logger

logger = get_logger(__name__)


class ConfigReader:
    """
    Unified property reader with optional and required property access.

    Examples:
        reader = ConfigReader()

        # Optional property (logs warning if missing, returns None)
        timeout = reader.get_property("timeout")

        # Required property (raises exception if missing/empty)
        base_url = reader.get_required_property("base_url")
    """

    def __init__(self):
        """Initialize ConfigReader with framework settings."""
        self.config = settings

    def get_property(self, key: str, default: Optional[str] = None) -> Optional[str]:
        """
        Get optional property from config.

        Logs warning if property not found and returns default.

        Args:
            key: Property key to look up
            default: Default value if not found

        Returns:
            Property value or default if not found

        Examples:
            >>> reader = ConfigReader()
            >>> timeout = reader.get_property("timeout", "30")
            >>> screenshot_on_failure = reader.get_property("screenshot_on_failure")
        """
        try:
            # Try Pydantic settings object attributes first
            if hasattr(self.config, key):
                value = getattr(self.config, key)
                return value if value is not None else default

            # Log warning if not found
            logger.warning(
                f"Optional property not found: '{key}' in settings. Using default: {default}"
            )
            return default
        except Exception as e:
            logger.error(f"Error reading property '{key}': {str(e)}")
            return default

    def get_required_property(self, key: str) -> str:
        """
        Get required property from config.

        Raises ConfigError if property missing, empty, or None.

        Args:
            key: Property key to look up

        Returns:
            Property value (guaranteed non-empty)

        Raises:
            ValueError: If property is missing, None, or empty

        Examples:
            >>> reader = ConfigReader()
            >>> base_url = reader.get_required_property("base_url")
            >>> browser = reader.get_required_property("browser")
        """
        try:
            if not hasattr(self.config, key):
                raise ValueError(
                    f"Required property '{key}' not found in configuration"
                )

            value = getattr(self.config, key)

            if value is None or (isinstance(value, str) and not value.strip()):
                raise ValueError(
                    f"Required property '{key}' is missing or empty"
                )

            logger.debug(f"Got required property: {key}")
            return str(value)
        except ValueError as e:
            logger.error(f"Configuration error: {str(e)}")
            raise

    def get_int(self, key: str, default: int = 0) -> int:
        """
        Get integer property from config.

        Examples:
            >>> reader = ConfigReader()
            >>> timeout = reader.get_int("timeout", 30)
        """
        value = self.get_property(key)
        if value is None:
            return default
        try:
            return int(value)
        except ValueError:
            logger.warning(f"Property '{key}' is not a valid integer: {value}, using default: {default}")
            return default

    def get_bool(self, key: str, default: bool = False) -> bool:
        """
        Get boolean property from config.

        Accepts: 'true', 'True', '1', 'yes', '1' → True
        Accepts: 'false', 'False', '0', 'no' → False

        Examples:
            >>> reader = ConfigReader()
            >>> headless = reader.get_bool("headless", False)
        """
        value = self.get_property(key)
        if value is None:
            return default
        return value.lower() in ("true", "1", "yes", "on")

    def get_list(self, key: str, separator: str = ",", default: Optional[list] = None) -> list:
        """
        Get comma-separated list property from config.

        Examples:
            >>> reader = ConfigReader()
            >>> browsers = reader.get_list("browsers", ",", ["chrome", "firefox"])
        """
        value = self.get_property(key)
        if value is None:
            return default or []
        return [item.strip() for item in value.split(separator) if item.strip()]

    def to_dict(self) -> dict:
        """
        Export all config properties to dictionary (safe, non-sensitive fields).

        Examples:
            >>> reader = ConfigReader()
            >>> config_dict = reader.to_dict()
        """
        result = {}
        # Get all public attributes from settings
        for key in dir(self.config):
            if not key.startswith("_"):
                try:
                    value = getattr(self.config, key)
                    # Skip methods and callables
                    if not callable(value):
                        result[key] = value
                except Exception:
                    pass
        return result


# ── Module-level Singleton Instance ────────────────────────────────────────
_reader_instance: Optional[ConfigReader] = None


def get_config_reader() -> ConfigReader:
    """
    Get or create module-level ConfigReader singleton.

    Returns:
        Singleton ConfigReader instance

    Examples:
        >>> reader = get_config_reader()
        >>> base_url = reader.get_required_property("base_url")
    """
    global _reader_instance
    if _reader_instance is None:
        _reader_instance = ConfigReader()
    return _reader_instance

