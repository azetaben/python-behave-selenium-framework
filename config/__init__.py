"""Canonical configuration package for framework runtime settings and config helpers."""

from config.config import BrowserType, PageLoadStrategy, Settings, settings
from config.config_reader import ConfigReader
from config.faker_utils import FakerUtils
from config.framework_config import FrameworkConfig
from config.integration import ConfigBundle, attach_config_to_context, build_config_bundle
from config.property_file_reader import PropertyFileReader
from config import test_data

__all__ = [
    "BrowserType",
    "ConfigBundle",
    "ConfigReader",
    "FakerUtils",
    "FrameworkConfig",
    "PageLoadStrategy",
    "PropertyFileReader",
    "Settings",
    "attach_config_to_context",
    "build_config_bundle",
    "settings",
    "test_data",
]

