"""
Pydantic configuration for the Behave Selenium Framework.

Loads settings from environment variables, .env file, and CLI overrides.
Priority: CLI > Environment variable > .env file > defaults
"""
from enum import Enum
from pathlib import Path
from typing import Optional

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class BrowserType(str, Enum):
    """Supported browser types."""
    CHROME = "chrome"
    FIREFOX = "firefox"
    EDGE = "edge"
    SAFARI = "safari"
    REMOTE = "remote"


class PageLoadStrategy(str, Enum):
    """Page load strategies."""
    NORMAL = "normal"
    EAGER = "eager"
    NONE = "none"


class Settings(BaseSettings):
    """Application settings loaded from .env and environment variables."""
    
    model_config = SettingsConfigDict(
        env_file="env/.env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore"
    )
    
    # ── Browser ──────────────────────────────────────────────────────────
    browser: BrowserType = Field(default=BrowserType.CHROME, description="Browser type")
    headless: bool = Field(default=False, description="Run browser in headless mode")
    window_width: int = Field(default=1920, description="Browser window width")
    window_height: int = Field(default=1080, description="Browser window height")
    
    # ── Browser Options ──────────────────────────────────────────────────
    incognito: bool = Field(default=False, description="Run in incognito/private mode")
    disable_images: bool = Field(default=False, description="Disable image loading")
    disable_javascript: bool = Field(default=False, description="Disable JavaScript")
    disable_gpu: bool = Field(default=True, description="Disable GPU acceleration")
    disable_extensions: bool = Field(default=True, description="Disable extensions")
    disable_notifications: bool = Field(default=True, description="Disable notifications")
    ignore_certificate_errors: bool = Field(default=True, description="Ignore SSL certificate errors")
    page_load_strategy: PageLoadStrategy = Field(default=PageLoadStrategy.NORMAL, description="Page load strategy")
    
    # ── Custom Options ───────────────────────────────────────────────────
    user_agent: Optional[str] = Field(default=None, description="Custom user agent")
    proxy_server: Optional[str] = Field(default=None, description="Proxy server URL")
    mobile_emulation_device: Optional[str] = Field(default=None, description="Mobile device emulation")
    
    download_dir: str = Field(default="downloads", description="Download directory")
    
    # ── Remote / Selenium Grid ───────────────────────────────────────────
    remote_url: Optional[str] = Field(default=None, description="Selenium Grid URL")
    
    # ── Application ──────────────────────────────────────────────────────
    base_url: str = Field(default="https://www.saucedemo.com", description="Application base URL")
    environment: str = Field(default="dev", description="Environment (dev, qa, staging, prod)")
    timeout: int = Field(default=10, description="General timeout in seconds")
    implicit_wait: int = Field(default=5, description="Implicit wait in seconds")
    explicit_wait: int = Field(default=15, description="Explicit wait in seconds")
    
    # ── Test Data ────────────────────────────────────────────────────────
    test_username: str = Field(default="standard_user", description="Test username")
    test_password: str = Field(default="secret_sauce", description="Test password")
    
    # ── Logging ──────────────────────────────────────────────────────────
    log_level: str = Field(default="INFO", description="Logging level")
    log_format: str = Field(
        default="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        description="Log format"
    )
    
    # ── Reporting ────────────────────────────────────────────────────────
    report_path: str = Field(default="reports", description="Reports directory")
    screenshot_on_failure: bool = Field(default=True, description="Take screenshot on test failure")
    screenshot_on_success: bool = Field(default=False, description="Take screenshot on test success")
    video_recording: bool = Field(default=False, description="Record test videos")
    
    # ── Performance ──────────────────────────────────────────────────────
    performance_threshold: int = Field(default=3000, description="Performance threshold in ms")
    network_throttling: bool = Field(default=False, description="Enable network throttling")


# Initialize settings singleton
settings = Settings()
