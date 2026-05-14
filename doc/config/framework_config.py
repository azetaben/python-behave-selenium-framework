"""
Framework configuration singleton that loads properties from files and environment.

Equivalent to Java FrameworkConfig class.
Implements singleton pattern and loads configuration with environment override support.
"""

import os
import threading
from configparser import ConfigParser
from pathlib import Path
from typing import Optional

from utils.logger import get_logger

logger = get_logger(__name__)


class FrameworkConfig:
    """
    Singleton configuration loader for framework properties.

    Loads configuration from:
    1. System properties (highest priority)
    2. Environment variables
    3. Configuration file (lowest priority)

    Equivalent to Java FrameworkConfig with singleton pattern.
    """

    _instance: Optional['FrameworkConfig'] = None
    _lock = threading.Lock()

    def __init__(self):
        """Initialize framework configuration by loading properties file."""
        if FrameworkConfig._instance is not None:
            raise RuntimeError("Use FrameworkConfig.get_instance() instead")

        self._properties: dict[str, str] = {}
        self._load_properties()

    @classmethod
    def get_instance(cls) -> 'FrameworkConfig':
        """
        Get singleton instance of FrameworkConfig.

        Returns:
            Singleton instance
        """
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = cls()
        return cls._instance

    def _load_properties(self) -> None:
        """Load properties from configuration file."""
        config_path = self._get_config_properties_path()

        if not config_path.exists():
            logger.warning(f"Configuration file not found at {config_path}, using defaults")
            return

        try:
            # Try to read as INI format first (for .properties files)
            if str(config_path).endswith('.properties'):
                parser = ConfigParser()
                parser.read(config_path, encoding='utf-8')

                # Flatten all sections into properties dict
                for section in parser.sections():
                    for key, value in parser.items(section):
                        self._properties[key] = value

                logger.info(f"Loaded {len(self._properties)} properties from {config_path}")
            else:
                # For .env files, parse as key=value pairs
                with open(config_path, 'r', encoding='utf-8') as f:
                    for line in f:
                        line = line.strip()
                        if line and not line.startswith('#'):
                            if '=' in line:
                                key, value = line.split('=', 1)
                                self._properties[key.strip()] = value.strip()

                logger.info(f"Loaded {len(self._properties)} properties from {config_path}")
        except Exception as e:
            logger.warning(f"Unable to load framework configuration from {config_path}: {e}")
            # Don't raise, just warn - framework should work with defaults

    def _get_config_properties_path(self) -> Path:
        """
        Get path to configuration properties file.

        Checks in order:
        1. config/config.properties
        2. .env file in env/ directory

        Returns:
            Path to configuration file
        """
        # Try config/config.properties
        config_file = Path(__file__).parent / "config.properties"
        if config_file.exists():
            return config_file

        # Try env/.env in repo root.
        project_root = Path(__file__).resolve().parents[2]
        env_file = project_root / "env" / ".env"
        return env_file

    def get_string(self, key: str, default_value: Optional[str] = None) -> Optional[str]:
        """
        Get string property with fallback chain.

        Priority:
        1. System property (os.environ during test)
        2. Environment variable
        3. Properties file
        4. Default value

        Args:
            key: Property key
            default_value: Default value if not found

        Returns:
            Property value or default_value if not found
        """
        # Check system properties (simulated via environment)
        if key in os.environ:
            return os.environ[key].strip()

        # Check environment variable (with key conversion)
        env_key = self._to_environment_key(key)
        if env_key in os.environ:
            return os.environ[env_key].strip()

        # Check properties file
        if key in self._properties:
            return self._properties[key].strip()

        # Return default
        return default_value

    def get_int(self, key: str, default_value: int) -> int:
        """
        Get integer property.

        Args:
            key: Property key
            default_value: Default value if not found or invalid

        Returns:
            Integer property value or default
        """
        value = self.get_string(key)

        if value is None or value.strip() == "":
            return default_value

        try:
            return int(value)
        except ValueError:
            logger.warning(f"Could not parse '{key}' as integer: {value}, using default {default_value}")
            return default_value

    def get_boolean(self, key: str, default_value: bool) -> bool:
        """
        Get boolean property.

        Args:
            key: Property key
            default_value: Default value if not found

        Returns:
            Boolean property value or default
        """
        value = self.get_string(key)

        if value is None or value.strip() == "":
            return default_value

        return value.lower() in ("true", "1", "yes", "on")

    def as_properties(self) -> dict[str, str]:
        """
        Get a copy of all properties.

        Returns:
            Dictionary of all properties
        """
        return self._properties.copy()

    @staticmethod
    def _to_environment_key(key: str) -> str:
        """
        Convert property key to environment variable key format.

        Replaces . - and spaces with _ and converts to uppercase.
        Example: "page.load.timeout" -> "PAGE_LOAD_TIMEOUT"

        Args:
            key: Property key

        Returns:
            Environment variable key
        """
        return key.replace(".", "_").replace("-", "_").replace(" ", "_").upper()

