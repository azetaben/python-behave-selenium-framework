"""Backward-compatible shim for legacy CamelCase ConfigReader module."""

from typing import Optional

from config.config_reader import ConfigReader

_reader_instance: Optional[ConfigReader] = None


def get_config_reader() -> ConfigReader:
    global _reader_instance
    if _reader_instance is None:
        _reader_instance = ConfigReader()
    return _reader_instance


__all__ = ["ConfigReader", "get_config_reader"]

