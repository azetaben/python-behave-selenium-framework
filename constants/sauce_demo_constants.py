"""Sauce Demo constants integrated with runtime config defaults."""

from dataclasses import dataclass

from constants.AppConstants import AppConstants
from doc.config.integration import build_config_bundle


@dataclass(frozen=True)
class SauceDemoConstants:
    """Constants used by login and inventory assertions."""

    LOGIN_USERNAME_FIELD_ID: str = "user-name"
    LOGIN_PASSWORD_FIELD_ID: str = "password"
    LOGIN_BUTTON_ID: str = "login-button"

    ERR_LOCKED_OUT: str = AppConstants.Errors.LOCKED_OUT_USER
    ERR_WRONG_CREDENTIALS: str = AppConstants.Errors.WRONG_CREDENTIALS
    ERR_USERNAME_REQUIRED: str = AppConstants.Errors.USERNAME_REQUIRED
    ERR_PASSWORD_REQUIRED: str = AppConstants.Errors.PASSWORD_REQUIRED

    USER_STANDARD: str = AppConstants.Users.STANDARD
    USER_LOCKED_OUT: str = AppConstants.Users.LOCKED
    USER_PROBLEM: str = AppConstants.Users.PROBLEM
    USER_PERFORMANCE_GLITCH: str = AppConstants.Users.GLITCH
    USER_VISUAL: str = AppConstants.Users.VISUAL
    USER_PASSWORD: str = AppConstants.Users.PASSWORD

    APP_TITLE: str = AppConstants.Pages.LOGIN_TITLE
    DEFAULT_BASE_URL: str = AppConstants.Urls.BASE

    @staticmethod
    def from_config() -> "SauceDemoConstants":
        """Build constants with optional overrides from integrated config services."""
        bundle = build_config_bundle()
        reader = bundle.property_reader

        return SauceDemoConstants(
            ERR_WRONG_CREDENTIALS=reader.get_property("login_error_message")
            or SauceDemoConstants.ERR_WRONG_CREDENTIALS,
            USER_STANDARD=reader.get_property("standard_user") or SauceDemoConstants.USER_STANDARD,
            USER_LOCKED_OUT=reader.get_property("locked_out_user") or SauceDemoConstants.USER_LOCKED_OUT,
            USER_PASSWORD=reader.get_property("password") or SauceDemoConstants.USER_PASSWORD,
            DEFAULT_BASE_URL=bundle.settings.base_url or SauceDemoConstants.DEFAULT_BASE_URL,
        )

