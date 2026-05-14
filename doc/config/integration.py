"""Integration helpers for using config modules together."""

from dataclasses import dataclass
from typing import Any

from doc.config.config import settings
from doc.config.config_reader import ConfigReader
from doc.config.framework_config import FrameworkConfig
from doc.config.property_file_reader import PropertyFileReader


@dataclass
class ConfigBundle:
    """Single object exposing all config entry points."""

    settings: Any
    framework: FrameworkConfig
    config_reader: ConfigReader
    property_reader: PropertyFileReader

    def resolve(self, value: str) -> str:
        """Resolve tokenized values like ${faker:email} or user:STANDARD_USERNAME."""
        return self.property_reader.resolve_value(value)

    def get_timeouts(self) -> dict[str, int]:
        """Return merged timeout values used by Selenium interactions."""
        return {
            "page_load": self.property_reader.get_page_load_timeout(),
            "implicit": self.property_reader.get_implicit_wait(),
            "explicit": self.property_reader.get_explicit_wait(),
        }


def build_config_bundle() -> ConfigBundle:
    """Build a ready-to-use configuration bundle."""
    framework = FrameworkConfig.get_instance()
    return ConfigBundle(
        settings=settings,
        framework=framework,
        config_reader=ConfigReader(),
        property_reader=PropertyFileReader(),
    )


def attach_config_to_context(context: Any) -> ConfigBundle:
    """Attach config services to Behave context for step-level usage."""
    bundle = build_config_bundle()
    context.config_bundle = bundle
    context.framework_config = bundle.framework
    context.config_reader = bundle.config_reader
    context.property_reader = bundle.property_reader
    return bundle

