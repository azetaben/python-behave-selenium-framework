"""
Configuration package for Behave Selenium Framework.

Exports configuration classes for loading properties, reading config,
and generating test data.
"""

from .config import Settings, BrowserType, PageLoadStrategy, settings
from .config_reader import ConfigReader
from .faker_utils import FakerUtils
from .framework_config import FrameworkConfig
from .integration import ConfigBundle, build_config_bundle, attach_config_to_context
from .property_file_reader import PropertyFileReader
from . import test_data

__all__ = [
    # Pydantic settings
    "Settings",
    "BrowserType",
    "PageLoadStrategy",
    "settings",

    # Configuration readers
    "ConfigReader",
    "PropertyFileReader",
    "FrameworkConfig",

    # Utilities
    "FakerUtils",

    # Test data
    "test_data",

    # Integration helpers
    "ConfigBundle",
    "build_config_bundle",
    "attach_config_to_context",
]
