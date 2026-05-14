"""Backward-compatible shim to canonical integration helpers."""

from config.integration import ConfigBundle, attach_config_to_context, build_config_bundle

__all__ = ["ConfigBundle", "attach_config_to_context", "build_config_bundle"]
