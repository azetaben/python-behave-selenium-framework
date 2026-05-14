"""Backward-compatible shim to canonical config settings module."""

from config.config import BrowserType, PageLoadStrategy, Settings, settings

__all__ = ["BrowserType", "PageLoadStrategy", "Settings", "settings"]
