"""Framework configuration singleton that loads properties from files and environment."""

import os
import threading
from configparser import ConfigParser
from pathlib import Path
from typing import Optional

from utils.logger import get_logger

logger = get_logger(__name__)


class FrameworkConfig:
    """Singleton configuration loader for framework properties."""

    _instance: Optional["FrameworkConfig"] = None
    _lock = threading.Lock()

    def __init__(self):
        if FrameworkConfig._instance is not None:
            raise RuntimeError("Use FrameworkConfig.get_instance() instead")
        self._properties: dict[str, str] = {}
        self._load_properties()

    @classmethod
    def get_instance(cls) -> "FrameworkConfig":
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = cls()
        return cls._instance

    def _load_properties(self) -> None:
        config_path = self._get_config_properties_path()
        if not config_path.exists():
            logger.warning("Configuration file not found at %s, using defaults", config_path)
            return

        try:
            if str(config_path).endswith(".properties"):
                parser = ConfigParser()
                parser.read(config_path, encoding="utf-8")
                for section in parser.sections():
                    for key, value in parser.items(section):
                        self._properties[key] = value
            else:
                for line in config_path.read_text(encoding="utf-8").splitlines():
                    line = line.strip()
                    if line and not line.startswith("#") and "=" in line:
                        key, value = line.split("=", 1)
                        self._properties[key.strip()] = value.strip()
            logger.info("Loaded %d properties from %s", len(self._properties), config_path)
        except Exception as e:
            logger.warning("Unable to load framework configuration from %s: %s", config_path, e)

    def _get_config_properties_path(self) -> Path:
        config_file = Path(__file__).parent / "config.properties"
        if config_file.exists():
            return config_file
        return Path(__file__).resolve().parents[1] / "env" / ".env"

    def get_string(self, key: str, default_value: Optional[str] = None) -> Optional[str]:
        if key in os.environ:
            return os.environ[key].strip()
        env_key = self._to_environment_key(key)
        if env_key in os.environ:
            return os.environ[env_key].strip()
        if key in self._properties:
            return self._properties[key].strip()
        return default_value

    def get_int(self, key: str, default_value: int) -> int:
        value = self.get_string(key)
        if value is None or value.strip() == "":
            return default_value
        try:
            return int(value)
        except ValueError:
            logger.warning("Could not parse '%s' as integer: %s, using default %s", key, value, default_value)
            return default_value

    def get_boolean(self, key: str, default_value: bool) -> bool:
        value = self.get_string(key)
        if value is None or value.strip() == "":
            return default_value
        return value.lower() in ("true", "1", "yes", "on")

    def as_properties(self) -> dict[str, str]:
        return self._properties.copy()

    @staticmethod
    def _to_environment_key(key: str) -> str:
        return key.replace(".", "_").replace("-", "_").replace(" ", "_").upper()
