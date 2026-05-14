"""
Python conversion: AppConstants.java

Module-level constants with lazy-loading from the Pydantic settings singleton.
Also exposes an ``AppConstants`` class whose nested groups mirror Java-style
static inner-class access (e.g. ``AppConstants.Timeouts.DEFAULT``).

Usage
-----
# Module-level (flat) – preferred for simple scripts / steps
from constants.AppConstants import DEFAULT_TIME_OUT, STANDARD_USER

# Class-level (grouped) – matches Java import style
from constants.AppConstants import AppConstants
timeout = AppConstants.Timeouts.DEFAULT
user    = AppConstants.Users.STANDARD
"""

from typing import Final

from doc.config.config import settings

# ── Timeout Constants ──────────────────────────────────────────────────────
DEFAULT_TIME_OUT: Final[int] = settings.implicit_wait or 5
SHORT_TIME_OUT: Final[int] = settings.explicit_wait or 10
MEDIUM_TIME_OUT: Final[int] = 15
MAX_TIME_OUT: Final[int] = 20

# ── Page Identifiers ───────────────────────────────────────────────────────
LOGIN_PAGE_TITLE: Final[str] = "Swag Labs"
LOGIN_PAGE_URL_FRACTION: Final[str] = "/"
LOGIN_PAGE_LOGO: Final[str] = "Swag Labs"
INVENTORY_PAGE_URL_FRACTION: Final[str] = "inventory.html"
CART_PAGE_URL_FRACTION: Final[str] = "cart.html"
CHECKOUT_STEP_ONE_URL_FRACTION: Final[str] = "checkout-step-one"
CHECKOUT_STEP_TWO_URL_FRACTION: Final[str] = "checkout-step-two"
CHECKOUT_COMPLETE_URL_FRACTION: Final[str] = "checkout-complete"
PRODUCT_DETAIL_URL_FRACTION: Final[str] = "inventory-item"
LOGIN_PAGE_ACCEPTED_USERS: Final[list[str]] = [
    "standard_user",
    "locked_out_user",
    "problem_user",
    "performance_glitch_user",
    "error_user",
    "visual_user",
]

# ── Excel / CSV Sheet Names ────────────────────────────────────────────────
PRODUCT_SHEET_NAME: Final[str] = "product"
USER_SHEET_NAME: Final[str] = "users"
LOGIN_SHEET_NAME: Final[str] = "login_data"

# ── Application URLs ───────────────────────────────────────────────────────
BASE_URL: Final[str] = settings.base_url
INVENTORY_URL: Final[str] = f"{settings.base_url}/inventory.html"
CART_URL: Final[str] = f"{settings.base_url}/cart.html"
CHECKOUT_URL: Final[str] = f"{settings.base_url}/checkout-step-one.html"
CHECKOUT_STEP_TWO_URL: Final[str] = f"{settings.base_url}/checkout-step-two.html"
CHECKOUT_COMPLETE_URL: Final[str] = f"{settings.base_url}/checkout-complete.html"

# ── Credentials (sourced from settings so .env overrides work) ────────────
STANDARD_USER: Final[str] = settings.test_username or "standard_user"
STANDARD_PASSWORD: Final[str] = settings.test_password or "secret_sauce"
LOCKED_USER: Final[str] = "locked_out_user"
PROBLEM_USER: Final[str] = "problem_user"
PERFORMANCE_GLITCH_USER: Final[str] = "performance_glitch_user"
ERROR_USER: Final[str] = "error_user"
VISUAL_USER: Final[str] = "visual_user"

# ── Assertion / Error Messages ─────────────────────────────────────────────
ERROR_LOGIN_FAILED: Final[str] = "Login failed"
ERROR_PAGE_NOT_FOUND: Final[str] = "Page not found"
ERROR_ELEMENT_NOT_FOUND: Final[str] = "Element not found"
ERROR_LOCKED_OUT_USER: Final[str] = "Epic sadface: Sorry, this user has been locked out."
ERROR_WRONG_CREDENTIALS: Final[str] = "Epic sadface: Username and password do not match any user in this service"
ERROR_USERNAME_REQUIRED: Final[str] = "Epic sadface: Username is required"
ERROR_PASSWORD_REQUIRED: Final[str] = "Epic sadface: Password is required"
ERROR_LOGO_NOT_FOUND: Final[str] = "==logo not found=="
ERROR_TITLE_NOT_MATCHED: Final[str] = "==title is not matched=="
ERROR_URL_NOT_MATCHED: Final[str] = "==url is not matched=="

# ── Performance ────────────────────────────────────────────────────────────
PERFORMANCE_THRESHOLD_MS: Final[int] = settings.performance_threshold or 3000


# ── Grouped class (Java-style static inner-class access) ──────────────────
class AppConstants:
    """
    Grouped access to all framework constants.

    Examples::

        AppConstants.Timeouts.DEFAULT       # → 5
        AppConstants.Users.STANDARD         # → "standard_user"
        AppConstants.Urls.INVENTORY         # → "https://…/inventory.html"
        AppConstants.Errors.LOGO_NOT_FOUND  # → "==logo not found=="
        AppConstants.Sheets.LOGIN           # → "login_data"
        AppConstants.Performance.THRESHOLD  # → 3000
    """

    class Timeouts:
        DEFAULT = DEFAULT_TIME_OUT
        SHORT = SHORT_TIME_OUT
        MEDIUM = MEDIUM_TIME_OUT
        MAX = MAX_TIME_OUT

    class Pages:
        LOGIN_TITLE = LOGIN_PAGE_TITLE
        LOGIN_LOGO = LOGIN_PAGE_LOGO
        LOGIN_URL_FRACTION = LOGIN_PAGE_URL_FRACTION
        INVENTORY_URL_FRACTION = INVENTORY_PAGE_URL_FRACTION
        CART_URL_FRACTION = CART_PAGE_URL_FRACTION
        CHECKOUT_STEP_ONE_URL_FRACTION = CHECKOUT_STEP_ONE_URL_FRACTION
        CHECKOUT_STEP_TWO_URL_FRACTION = CHECKOUT_STEP_TWO_URL_FRACTION
        CHECKOUT_COMPLETE_URL_FRACTION = CHECKOUT_COMPLETE_URL_FRACTION
        PRODUCT_DETAIL_URL_FRACTION = PRODUCT_DETAIL_URL_FRACTION

    class Users:
        STANDARD = STANDARD_USER
        LOCKED = LOCKED_USER
        PROBLEM = PROBLEM_USER
        GLITCH = PERFORMANCE_GLITCH_USER
        ERROR = ERROR_USER
        VISUAL = VISUAL_USER
        PASSWORD = STANDARD_PASSWORD
        ACCEPTED_USERS = LOGIN_PAGE_ACCEPTED_USERS
        ALL_USERS = LOGIN_PAGE_ACCEPTED_USERS  # alias

    class Urls:
        BASE = BASE_URL
        INVENTORY = INVENTORY_URL
        CART = CART_URL
        CHECKOUT = CHECKOUT_URL
        CHECKOUT_STEP_TWO = CHECKOUT_STEP_TWO_URL
        CHECKOUT_COMPLETE = CHECKOUT_COMPLETE_URL

    class Errors:
        LOGIN_FAILED = ERROR_LOGIN_FAILED
        PAGE_NOT_FOUND = ERROR_PAGE_NOT_FOUND
        ELEMENT_NOT_FOUND = ERROR_ELEMENT_NOT_FOUND
        LOCKED_OUT_USER = ERROR_LOCKED_OUT_USER
        WRONG_CREDENTIALS = ERROR_WRONG_CREDENTIALS
        USERNAME_REQUIRED = ERROR_USERNAME_REQUIRED
        PASSWORD_REQUIRED = ERROR_PASSWORD_REQUIRED
        LOGO_NOT_FOUND = ERROR_LOGO_NOT_FOUND
        TITLE_NOT_MATCHED = ERROR_TITLE_NOT_MATCHED
        URL_NOT_MATCHED = ERROR_URL_NOT_MATCHED

    class Sheets:
        PRODUCT = PRODUCT_SHEET_NAME
        USER = USER_SHEET_NAME
        LOGIN = LOGIN_SHEET_NAME

    class Performance:
        THRESHOLD = PERFORMANCE_THRESHOLD_MS
